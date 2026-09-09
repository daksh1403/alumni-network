import { getPool, json, oracleError } from "./db.mjs";

export default async () => {
  const dsn = process.env.ORA_DSN || "";
  const counts = {};
  try {
    const pool = await getPool();
    const conn = await pool.getConnection();
    try {
      for (const [key, sql] of [
        ["alumni", "SELECT COUNT(*) FROM ALUMNI"],
        ["students", "SELECT COUNT(*) FROM STUDENT"],
        ["events", "SELECT COUNT(*) FROM EVENT"],
        ["donations", "SELECT COUNT(*) FROM DONATION"],
      ]) {
        counts[key] = (await conn.execute(sql)).rows[0][0];
      }
    } finally {
      await conn.close();
    }
    return json({ dsn, stats: counts });
  } catch (exc) {
    return json({ dsn, stats: {}, error: oracleError(exc) }, 503);
  }
};
