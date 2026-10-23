# Project 1

An alumni network SQL console built for our DBMS mini project. The website sends SQL to a Cloudflare Worker, which executes it on Cloudflare D1 and returns rows or operation results.

[Open Project 1](https://alumni-sql-console.dakshx.workers.dev/)

## Features

- SQL editor with history, schema browsing and query presets.
- Add, update and delete forms with SQL previews.
- Joins, aggregates, subqueries, CTEs and window functions supported by D1.
- Database health, schema and record-count APIs.

The migration defines 14 domain tables covering alumni, students, departments, batches, companies, skills, mentoring, events, donations and jobs. Some laboratory presets may need adjustments for the current schema or SQLite syntax.

## Run locally

Requires Node.js 22 or later and access to Cloudflare for deployment.

```sh
cd "Project 1"
npm ci
npx wrangler d1 migrations apply alumni-db --local
npm run dev
```

Open the address printed by Wrangler. The migration is in `migrations/0001_alumni_schema.sql`; the Worker, assets and database binding are configured in `wrangler.jsonc`.

## Build and deploy

```sh
npm run check
npx wrangler login
npx wrangler d1 migrations apply alumni-db --remote
npm run deploy
```

The check command validates JavaScript syntax and builds the Worker without publishing it. Keep Cloudflare credentials outside source files.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Database connectivity |
| GET | `/api/schema` | Tables and column details |
| GET | `/api/stats` | Record counts |
| POST | `/api/query` | Execute SQL, such as `{"sql":"SELECT * FROM ALUMNI;"}` |

The console permits database changes and DDL. It has no user authentication; CORS is not access control. Returned rows are limited by the Worker configuration.

## Optional Flask backend

The Python backend is retained for local SQLite use and PostgreSQL query execution through `DATABASE_URL`. It runs separately from the Cloudflare Worker.

From this folder, initialise local SQLite:

```sh
python3 - <<'PY'
import sqlite3
from pathlib import Path
with sqlite3.connect('alumni.db') as db:
    db.executescript(Path('migrations/0001_alumni_schema.sql').read_text())
PY
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask health, schema and stats routes read local SQLite. Query execution can use PostgreSQL when configured. The Dockerfile builds this Python backend.

## Files

- `worker.js`: Cloudflare API and SQL execution.
- `static/`: Website markup, styles and JavaScript.
- `migrations/`: Database schema and initial records.
- `app.py`, `backend/`: Optional Flask application.
- `wrangler.jsonc`: Deployment and database configuration.
