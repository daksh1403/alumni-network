import { getPool, json, oracleError } from "./db.mjs";

export default async () => {
  try {
    const pool = await getPool();
    const conn = await pool.getConnection();
    try {
      await conn.execute("SELECT 1 FROM DUAL");
    } finally {
      await conn.close();
    }
    return json({ ok: true, database: process.env.ORA_DSN || "" });
  } catch (exc) {
    return json({ ok: false, error: oracleError(exc) }, 503);
  }
};
