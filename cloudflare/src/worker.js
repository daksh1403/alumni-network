const MAX_ROWS = 1000;
const ENGINE = "Cloudflare D1 (SQLite)";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    },
  });

const stripSql = (sql) => {
  sql = String(sql || "").trim();
  return sql.endsWith(";") ? sql.slice(0, -1).trim() : sql;
};

const statementKind = (sql) => {
  const m = sql.match(/^\s*([A-Za-z]+)/);
  const kw = m ? m[1].toUpperCase() : "";
  if (["SELECT", "WITH", "EXPLAIN", "PRAGMA"].includes(kw)) return "query";
  return "execute";
};

async function handleQuery(env, sql) {
  const started = Date.now();
  const kind = statementKind(sql);
  const stmt = env.DB.prepare(sql);
  if (kind === "query") {
    const r = await stmt.all();
    const results = r.results || [];
    const columns = results.length ? Object.keys(results[0]) : [];
    const rows = results.slice(0, MAX_ROWS).map((o) =>
      columns.map((c) => (o[c] === null || o[c] === undefined ? null : o[c])));
    return json({
      ok: true,
      kind: "query",
      columns,
      rows,
      rowCount: rows.length,
      truncated: results.length >= MAX_ROWS,
      elapsedMs: Date.now() - started,
    });
  }
  const r = await stmt.run();
  const affected = r.meta?.changes ?? 0;
  return json({
    ok: true,
    kind: "execute",
    message: `Statement executed. ${affected} row(s) affected.`,
    rowCount: affected,
    elapsedMs: Date.now() - started,
  });
}

function parseCreateTable(sql) {
  const open = sql.indexOf("(");
  const close = sql.lastIndexOf(")");
  if (open === -1 || close === -1) return { columns: [], pkComposite: [] };
  const body = sql.slice(open + 1, close);
  const parts = [];
  let depth = 0, cur = "";
  for (const ch of body) {
    if (ch === "(") depth++;
    else if (ch === ")") depth--;
    if (ch === "," && depth === 0) { parts.push(cur); cur = ""; }
    else cur += ch;
  }
  if (cur.trim()) parts.push(cur);

  const columns = [];
  const pkComposite = [];
  for (const part of parts) {
    const p = part.trim();
    if (/^(PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK|CONSTRAINT)/i.test(p)) {
      const m = p.match(/PRIMARY\s+KEY\s*\(([^)]+)\)/i);
      if (m) pkComposite.push(...m[1].split(",").map((s) => s.trim().replace(/["'`\[\]]/g, "")));
      continue;
    }
    const m = p.match(/^["'`\[]?([A-Za-z_]\w*)["'`\]]?\s+(\w+)/);
    if (m) {
      const col = { name: m[1], type: m[2].toUpperCase(), pk: /\bPRIMARY\s+KEY\b/i.test(p) };
      columns.push(col);
    }
  }
  return { columns, pkComposite };
}

async function handleSchema(env) {
  const tables = {};
  const list = await env.DB.prepare(
    "SELECT name, sql FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' ORDER BY name"
  ).all();
  for (const { name, sql } of list.results) {
    const { columns, pkComposite } = parseCreateTable(sql || "");
    tables[name] = {
      columns: columns.map(({ name: n, type }) => ({ name: n, type })),
      pk: columns.filter((c) => c.pk).map((c) => c.name).concat(pkComposite),
    };
  }
  return json({ tables });
}

async function handleStats(env) {
  const counts = {};
  for (const [key, table] of [
    ["alumni", "ALUMNI"],
    ["students", "STUDENT"],
    ["events", "EVENT"],
    ["donations", "DONATION"],
  ]) {
    const r = await env.DB.prepare(`SELECT COUNT(*) AS n FROM ${table}`).first();
    counts[key] = r?.n ?? 0;
  }
  return json({ engine: ENGINE, database: "D1: alumni-db", stats: counts });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") return new Response("", { status: 204 });

    if (url.pathname === "/api/health") {
      try {
        await env.DB.prepare("SELECT 1").first();
        return json({ ok: true, engine: ENGINE, database: "D1: alumni-db" });
      } catch (err) {
        return json({ ok: false, error: String(err) }, 503);
      }
    }

    if (url.pathname === "/api/schema") {
      try {
        return await handleSchema(env);
      } catch (err) {
        return json({ tables: {}, error: String(err) }, 503);
      }
    }

    if (url.pathname === "/api/stats") {
      try {
        return await handleStats(env);
      } catch (err) {
        return json({ engine: ENGINE, database: "D1: alumni-db", stats: {}, error: String(err) }, 503);
      }
    }

    if (url.pathname === "/api/query" && request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: "Invalid JSON body." }, 400);
      }
      const sql = stripSql(body.sql);
      if (!sql) return json({ error: "Empty statement." }, 400);
      try {
        return await handleQuery(env, sql);
      } catch (err) {
        return json({ error: String(err.message || err) }, 400);
      }
    }

    return env.ASSETS.fetch(request);
  },
};
