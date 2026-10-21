# Alumni Network SQL Console

An academic DBMS project for exploring an Alumni Network database through a browser. The hosted application uses Cloudflare Workers and Cloudflare D1 (SQLite), with a vanilla HTML, CSS, and JavaScript frontend.

[Open the live console](https://alumni-sql-console.dakshx.workers.dev/)

## Features

- SQL terminal with history, schema browsing, and preset queries.
- Add, Update, and Delete forms for alumni, students, companies, events, and jobs.
- SQL previews before executing form-generated statements.
- Relational queries including joins, subqueries, aggregates, CTEs, and window functions supported by D1.
- Database health and record-count APIs.

Some laboratory presets require correction for the current schema or SQLite dialect; not every preset is a verified working example.

## Team responsibilities

| Member | Responsibility |
| --- | --- |
| Sagarika Kaistha | CRUD frontend, including Add/Update/Delete forms |
| Praveen G | Modular Flask backend API structure |
| Daksh Agarwal | Remaining database, Worker integration, testing, and documentation work |

## Architecture

```text
Browser (static/index.html, app.js, style.css)
  -> POST /api/query with { "sql": "..." }
  -> Cloudflare Worker (worker.js)
  -> Cloudflare D1 prepared statement
  -> JSON rows or execution metadata
  -> Browser result table or status message
```

The Worker serves the static frontend and APIs. SQL executes directly on D1. Supported syntax follows the SQLite engine available in D1.

The modular Flask backend is retained for local/reference use. It is separate from the Cloudflare runtime.

## Database schema

`webapp/migrations/0001_alumni_schema.sql` creates and seeds 14 domain tables:

| Table | Purpose |
| --- | --- |
| DEPARTMENT | Academic departments |
| BATCH | Graduation batches |
| COMPANY | Employers |
| SKILL | Skills catalog |
| ALUMNI | Alumni profiles |
| ALUMNI_PHONE | Multiple phone numbers per alumnus |
| STUDENT | Student profiles |
| STUDENT_EMAIL | Multiple email addresses per student |
| MENTORSHIP | Alumni/student mentorships |
| EVENT | Events and reunions |
| DONATION | Alumni donations |
| JOB | Job postings |
| ALUMNI_SKILL | Alumni/skill many-to-many mapping |
| ALUMNI_EVENT | Alumni/event attendance mapping |

The migration includes primary keys, foreign keys, composite keys, uniqueness and CHECK constraints, selected cascading deletes, and indexes.

## Cloudflare development

Clone this repository and run the commands from `webapp/`:

```bash
git clone https://github.com/daksh1403/alumni-network.git
cd alumni-network/webapp
npm test
npm run check
```

For local Worker development, authenticate Wrangler as needed and apply the migration:

```bash
npx wrangler d1 migrations apply alumni-db --local
npx wrangler dev
```

`wrangler.jsonc` configures the Worker entry point, static assets, and the `DB` binding. Tests use a fake D1 adapter and require no live database.

To deploy the configured project:

```bash
npx wrangler d1 migrations apply alumni-db --remote
npx wrangler deploy
```

Keep database credentials and API tokens in environment/secret configuration rather than source files.

## API

| Method | Endpoint | Response |
| --- | --- | --- |
| GET | /api/health | Database connectivity and engine |
| GET | /api/schema | Tables, columns, types, and primary keys |
| GET | /api/stats | Alumni, student, event, and donation counts |
| POST | /api/query | SQL rows or execution metadata |

Example request:

```json
{"sql":"SELECT AlumniID, FirstName FROM ALUMNI ORDER BY AlumniID;"}
```

Query responses contain `ok`, `kind: "query"`, `columns`, `rows`, `rowCount`, `truncated`, and `elapsedMs`. Mutation/DDL responses contain `kind: "execute"`, a message, affected-row `rowCount`, and elapsed time. Errors return HTTP 400 with `ok: false`, `error`, and a code.

The Worker accepts statements up to 128 KB and returns up to 1,000 result rows by default. `MAX_ROWS` and `ALLOWED_ORIGIN` can be configured through Worker variables. The row cap limits returned output, not database execution cost. The console intentionally permits SQL mutations and DDL; CORS does not provide authentication.

## Local Flask backend

`app.py` registers modular health, schema, stats, and query Blueprints. `backend/services/query_service.py` executes local SQLite queries, or PostgreSQL queries when `DATABASE_URL` is set.

For local SQLite use, initialize the schema from the repository root:

```bash
python3 - <<'PY'
import sqlite3
from pathlib import Path
with sqlite3.connect('webapp/alumni.db') as db:
    db.executescript(Path('webapp/migrations/0001_alumni_schema.sql').read_text())
PY
```

Then install Python dependencies and start the backend from `webapp/`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask health/schema/stats routes currently inspect local SQLite even when query execution is configured for PostgreSQL. Docker support is retained for the Python backend.

## Project structure

```text
README.md
test/
  migrations.test.js
  worker.test.js
webapp/
  worker.js
  wrangler.jsonc
  migrations/0001_alumni_schema.sql
  package.json
  static/
  app.py
  backend/routes/
  backend/services/
  requirements.txt
  Dockerfile
```

## Validation

```bash
cd webapp
npm test
npm run check
```

The tests cover the domain migration, query response format and row cap, direct D1 mutations/DDL, database error responses, statement-size limits, and CORS preflight. They do not verify the current deployed version or every frontend preset.
