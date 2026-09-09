import oracledb from "oracledb";

const CFG = {
  user: process.env.ORA_USER,
  password: process.env.ORA_PASSWORD,
  dsn: process.env.ORA_DSN,
};

let pool;
export async function getPool() {
  if (!pool) {
    pool = await oracledb.createPool({ ...CFG, min: 0, max: 2, poolTimeout: 60 });
  }
  return pool;
}

export const MAX_ROWS = 500;

export function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

export function stripSql(sql) {
  sql = String(sql || "").trim();
  return sql.endsWith(";") ? sql.slice(0, -1).trim() : sql;
}

export function statementKind(sql) {
  const m = sql.match(/^\s*([A-Za-z]+)/);
  const kw = m ? m[1].toUpperCase() : "";
  return ["SELECT", "WITH", "EXPLAIN"].includes(kw) ? "query" : "execute";
}

export function jsonValue(v) {
  if (v === null || v === undefined) return null;
  if (v instanceof Date) return v.toISOString().slice(0, 19).replace("T", " ");
  if (typeof v === "object" && v.constructor.name === "Lob") return String(v);
  return v;
}

export async function executeSql(sql) {
  const pool = await getPool();
  const conn = await pool.getConnection();
  try {
    conn.callTimeout = 30000;
    const result = await conn.execute(sql, [], { maxRows: MAX_ROWS + 1 });
    if (statementKind(sql) === "query") {
      const rows = result.rows || [];
      const cols = result.metaData.map((d) => d.name);
      return {
        ok: true,
        kind: "query",
        columns: cols,
        rows: rows.map((r) => r.map(jsonValue)),
        rowCount: rows.length,
        truncated: rows.length >= MAX_ROWS,
      };
    }
    await conn.commit();
    const affected = result.rowsAffected || 0;
    return {
      ok: true,
      kind: "execute",
      message: `Statement executed. ${affected} row(s) affected.`,
      rowCount: affected,
    };
  } finally {
    await conn.close();
  }
}

export function oracleError(exc) {
  if (exc && exc.errorNum) return `ORA-${exc.errorNum}: ${exc.message}`;
  return String(exc && exc.message ? exc.message : exc);
}
