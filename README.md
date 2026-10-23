# Alumni Network

Two DBMS mini projects are kept in this repository, each in its own folder.

| Project | Application | Database |
| --- | --- | --- |
| [Project 1](Project%201/README.md) | SQL console with schema browsing and record management | Cloudflare D1 / SQLite |
| [Project 2](Project%202/README.md) | Alumni, mentoring and job discovery using semantic search | Qdrant Cloud |

## Live applications

- [Project 1](https://alumni-sql-console.dakshx.workers.dev/)
- [Project 2](https://alumni-vector-console.dakshx.workers.dev/)

## Run locally

Requires Node.js 22 or later. Open either project folder, install dependencies and start its server:

```sh
cd "Project 1"
npm ci
npm run dev
```

For vector search, use `cd "Project 2"` and follow its README to configure Qdrant credentials and seed the collection first.

Each project has its own source files, README and Wrangler deployment configuration. Run `npm run check` inside a project for syntax and deployment build checks. No automated test code or test tooling is included.
