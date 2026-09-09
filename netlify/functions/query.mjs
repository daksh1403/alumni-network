import { getPool, executeSql, stripSql, json, oracleError } from "./db.mjs";

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { status: 204 });
  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid JSON body." }, 400);
  }
  const sql = stripSql(body.sql);
  if (!sql) return json({ error: "Empty statement." }, 400);
  try {
    const result = await executeSql(sql);
    const start = Date.now();
    return json({ ...result, elapsedMs: Date.now() - start });
  } catch (exc) {
    return json({ error: oracleError(exc) }, 400);
  }
};
