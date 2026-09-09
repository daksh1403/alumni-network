import { getPool, json, oracleError } from "./db.mjs";

const SCHEMA_SQL = `
  SELECT t.table_name,
         c.column_name,
         c.data_type,
         CASE WHEN cc.column_name IS NOT NULL THEN 1 ELSE 0 END AS is_pk
    FROM user_tables t
    JOIN user_tab_columns c ON c.table_name = t.table_name
    LEFT JOIN (SELECT con.table_name, col.column_name
                 FROM user_constraints con
                 JOIN user_cons_columns col ON col.constraint_name = con.constraint_name
                WHERE con.constraint_type = 'P') cc
      ON cc.table_name = c.table_name AND cc.column_name = c.column_name
   WHERE t.table_name NOT LIKE 'BIN$%'
   ORDER BY t.table_name, c.column_id`;

export default async () => {
  try {
    const pool = await getPool();
    const conn = await pool.getConnection();
    try {
      const result = await conn.execute(SCHEMA_SQL);
      const tables = {};
      for (const [tname, cname, dtype, isPk] of result.rows) {
        const t = (tables[tname] ??= { columns: [], pk: [] });
        t.columns.push({ name: cname, type: dtype });
        if (isPk) t.pk.push(cname);
      }
      return json({ tables });
    } finally {
      await conn.close();
    }
  } catch (exc) {
    return json({ tables: {}, error: oracleError(exc) }, 503);
  }
};
