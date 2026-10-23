# Project 2

An alumni discovery website built for our DBMS mini project using Qdrant and Cloudflare Workers. Students describe what they need and find related alumni, mentoring opportunities or jobs.

[Open Project 2](https://alumni-vector-console.dakshx.workers.dev/)

## How it works

`Website → Cloudflare Worker → Qdrant → Up to five matches`

MiniLM creates 384-dimensional search vectors from record text. Semantic retrieval finds related meanings, BM25 matches keywords, and Reciprocal Rank Fusion combines the rankings. Department, skill, location and source filters narrow the results.

The website supports browsing, record details, linked records and protected admin editing. Saving an edited record regenerates its vectors. Descriptions are entered manually or created from seed templates.

## Data

The deployed collection contains 101 records: 50 alumni, 20 jobs, 15 mentoring records and 16 supporting records. Alumni names are unique; mentoring and batch titles distinguish their track or section.

There are 22 migrated records and 79 generated sample records. Sample content is labelled Sample and does not represent verified profiles or vacancies. A fresh seed without the private migration file creates 85 sample records.

## Run locally

Requires Node.js 22 or later and a Qdrant Cloud cluster with access to the configured inference models.

```sh
cd "Project 2"
npm ci
cp .env.example .dev.vars
```

Set your own values in `.dev.vars`:

```dotenv
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your-database-api-key
VECTOR_ADMIN_TOKEN=your-long-random-admin-token
```

Then run:

```sh
npm run seed
npm run dev
```

Open the URL printed by Wrangler. On Windows PowerShell, use `Copy-Item .env.example .dev.vars` instead of `cp`.

The collection and model are configured in `wrangler.jsonc`. Seeding uses stable IDs but can overwrite edits to seeded records. Credentials and private exports are excluded from Git.

## Build and deploy

```sh
npm run check
npx wrangler login
npx wrangler secret put QDRANT_URL
npx wrangler secret put QDRANT_API_KEY
npx wrangler secret put VECTOR_ADMIN_TOKEN
npm run deploy
```

The check command validates JavaScript syntax and builds the complete site without publishing it. Deployment includes both the frontend and Worker. Keep database keys in local configuration or server-side secrets.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Database connectivity |
| GET | `/api/stats`, `/api/facets` | Counts and filter values |
| POST | `/api/search` | Search using JSON such as `{"query":"Python mentor","kind":"alumni"}` |
| GET | `/api/records`, `/api/records/:uuid` | Browse or read a record |
| POST | `/api/records` | Create a record |
| PUT, DELETE | `/api/records/:uuid` | Update or delete a record |

Writes require `Authorization: Bearer <VECTOR_ADMIN_TOKEN>`. Browse responses include `nextOffset` for pagination. Descriptions must contain 20 to 4000 characters.

## Files and scope

- `frontend/`: Website and licensed fonts.
- `src/`: Worker API, Qdrant client and search validation.
- `scripts/`: Sample dataset and seeding.
- `wrangler.jsonc`: Development and deployment configuration.

The project searches its stored collection, not the internet. It does not include messaging, booking or student sign-in. Migrated connections are metadata references, not native graph traversals. Read APIs are public, so imported data and source properties must be suitable for public display.
