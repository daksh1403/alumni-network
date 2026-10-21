import test from "node:test";
import assert from "node:assert/strict";
import worker from "../webapp/worker.js";

function env() {
  return {
    DB: {
      prepare(sql) {
        return {
          bind() { return this; },
          async first() { return sql.includes("COUNT") ? { count: 5 } : { ok: 1 }; },
          async all() {
            if (sql.includes("sqlite_master")) return { results: [{ name: "ALUMNI", sql: "CREATE TABLE ALUMNI (AlumniID INTEGER PRIMARY KEY, FirstName TEXT)" }] };
            if (sql.includes("COUNT")) return { results: [{ count: 5 }] };
            return { results: [{ AlumniID: 1 }, { AlumniID: 2 }] };
          },
          async run() { return { meta: { changes: 1 } }; },
        };
      },
    },
    ASSETS: { fetch: async () => new Response("ok") },
    MAX_ROWS: "1",
  };
}

test("keeps normal SQL on D1 and preserves query response shape", async () => {
  const response = await worker.fetch(new Request("https://example.test/api/query", { method: "POST", body: JSON.stringify({ sql: "SELECT AlumniID FROM ALUMNI" }) }), env());
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.kind, "query");
  assert.equal(body.rowCount, 1);
  assert.equal(body.truncated, true);
});

test("rejects oversized statements and handles CORS preflight", async () => {
  const oversized = await worker.fetch(new Request("https://example.test/api/query", { method: "POST", body: JSON.stringify({ sql: "x".repeat(131073) }) }), env());
  assert.equal(oversized.status, 413);
  const preflight = await worker.fetch(new Request("https://example.test/api/query", { method: "OPTIONS" }), env());
  assert.equal(preflight.status, 204);
  assert.equal(preflight.headers.get("Access-Control-Allow-Origin"), "*");
});

for (const sql of [
  "INSERT INTO ALUMNI (AlumniID, FirstName, Email) VALUES (99, 'Demo', 'demo@example.com')",
  "UPDATE ALUMNI SET FirstName = 'Demo' WHERE AlumniID = 99",
  "DELETE FROM ALUMNI WHERE AlumniID = 99",
  "CREATE TABLE demo (id INTEGER PRIMARY KEY)",
]) {
  test(`executes SQL directly on D1: ${sql.split(" ")[0]}`, async () => {
    const environment = env();
    const statements = [];
    environment.DB.prepare = (statement) => {
      statements.push(statement);
      return { run: async () => ({ meta: { changes: 1 } }) };
    };
    const response = await worker.fetch(new Request("https://example.test/api/query", {
      method: "POST", body: JSON.stringify({ sql }),
    }), environment);
    const body = await response.json();
    assert.equal(response.status, 200);
    assert.equal(body.kind, "execute");
    assert.equal(body.rowCount, 1);
    assert.deepEqual(statements, [sql]);
  });
}

test("returns database execution errors as SQL errors", async () => {
  const environment = env();
  environment.DB.prepare = () => { throw new Error("syntax error"); };
  const response = await worker.fetch(new Request("https://example.test/api/query", {
    method: "POST", body: JSON.stringify({ sql: "invalid statement" }),
  }), environment);
  const body = await response.json();
  assert.equal(response.status, 400);
  assert.equal(body.code, "SQL_ERROR");
  assert.equal(body.error, "syntax error");
});
