# Alumni Network and Engagement Platform

> A full-stack web application with an interactive SQL console for managing alumni data — deployed on Cloudflare Workers with full SQL functionality!

## 🚀 Live Demo
**[https://alumni-sql-console.dakshx.workers.dev/](https://alumni-sql-console.dakshx.workers.dev/)**

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
  - [Quick Start (Local Development)](#quick-start-local-development)
  - [Docker Deployment](#docker-deployment)
  - [Cloudflare Workers Deployment](#cloudflare-workers-deployment)
- [Web Console](#web-console)
- [API Reference](#api-reference)
- [SQL Features](#sql-features)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Overview

The **Alumni Network and Engagement Platform** is a web-based SQL console connected to a live database. It allows users to execute SQL queries in real-time, browse the schema, and run preset queries for learning and analysis.

The application features:
- A **browser-based SQL terminal** that executes queries against a live database
- **14 normalized relations** modeling alumni, students, events, donations, mentorship, and jobs
- **100+ preset SQL queries** covering DDL, DML, joins, subqueries, window functions, and analytics
- **Cloudflare Workers deployment** with Cloudflare D1 database for global edge performance
- **Local development** with SQLite for zero-config setup

---

## Features

### Web Console
- Interactive SQL terminal with command history (↑/↓ arrow keys)
- Tab completion for `DESC` commands
- Real-time query execution with elapsed time display
- Schema browser with clickable column insertion
- 100+ categorized preset queries (one-click run)
- Support for all SQL operations: SELECT, INSERT, UPDATE, DELETE, DDL
- Results rendered as formatted tables

### Database Relations
- **ALUMNI** - Alumni profiles with contact info, employment, and department
- **STUDENT** - Current student information
- **DEPARTMENT** - Academic departments
- **BATCH** - Graduation batches
- **COMPANY** - Employer companies
- **SKILL** - Skills catalog
- **EVENT** - Alumni events and reunions
- **DONATION** - Financial contributions
- **JOB** - Job postings
- **MENTORSHIP** - Mentor-mentee relationships
- **ALUMNI_PHONE** - Alumni contact numbers (multi-valued attribute)
- **STUDENT_EMAIL** - Student email addresses (multi-valued attribute)
- **ALUMNI_SKILL** - Junction table for alumni-skill M:N relationship
- **ALUMNI_EVENT** - Junction table for alumni-event M:N relationship

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12+, Flask |
| **Database** | SQLite (default) / PostgreSQL (optional) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **WSGI Server** | Gunicorn |
| **Deployment** | Docker |

---

## Project Structure

```
alumni-network/
├── webapp/                     # Flask application & frontend
│   ├── app.py                  # Main Flask backend
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container configuration
│   └── static/
│       ├── index.html          # Main frontend UI
│       ├── app.js              # Console logic & API client
│       ├── style.css           # Complete styling
│       └── config.js           # API base URL configuration
└── docker-compose.yml          # Docker deployment configuration
```

---

## Database Schema

### Relations (14 Tables)

| Table | Description | Primary Key |
|-------|-------------|-------------|
| DEPARTMENT | Academic departments | DeptID |
| BATCH | Graduation batches | BatchID |
| COMPANY | Employer companies | CompanyID |
| SKILL | Skills catalog | SkillID |
| ALUMNI | Alumni member information | AlumniID |
| ALUMNI_PHONE | Alumni contact numbers | (AlumniID, PhoneNumber) |
| STUDENT | Current student information | StudentID |
| STUDENT_EMAIL | Student email addresses | (StudentID, Email) |
| MENTORSHIP | Mentor-mentee relationships | (AlumniID, MentorshipID) |
| EVENT | Alumni events | EventID |
| DONATION | Financial contributions | DonationID |
| JOB | Job postings | JobID |
| ALUMNI_SKILL | Alumni-skill mapping (M:N) | (AlumniID, SkillID) |
| ALUMNI_EVENT | Alumni-event attendance (M:N) | (AlumniID, EventID) |

### Entity Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| ALUMNI → DEPARTMENT | N:1 | Many alumni belong to one department |
| ALUMNI → BATCH | N:1 | Many alumni belong to one batch |
| ALUMNI → COMPANY | N:1 | Many alumni work at one company |
| ALUMNI ↔ SKILL | M:N | Via ALUMNI_SKILL junction table |
| ALUMNI ↔ EVENT | M:N | Via ALUMNI_EVENT junction table |
| ALUMNI → MENTORSHIP | 1:N | Alumni mentors multiple students |
| ALUMNI → ALUMNI_PHONE | 1:N | Multi-valued attribute (phone numbers) |
| STUDENT → STUDENT_EMAIL | 1:N | Multi-valued attribute (email addresses) |

### Constraints
- Primary keys on all tables
- Foreign keys with ON DELETE CASCADE where appropriate
- CHECK constraints (CGPA 0-10, BatchYear 1990-2100, IsActive 0/1)
- UNIQUE constraints on natural keys (Email, DeptCode, CompanyName, SkillName)
- NOT NULL constraints on essential attributes
- Indexes on foreign key columns for query performance

---

## Getting Started

### Quick Start (Local Development)

The application works out-of-the-box with SQLite — no database installation required.

```bash
# Clone the repository
git clone https://github.com/daksh1403/alumni-network.git
cd alumni-network/webapp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open http://localhost:8000 in your browser.

**That's it!** The SQLite database is automatically created and seeded on first run.

### Docker Deployment

```bash
# Build and run with Docker
docker compose up

# Access the application at http://localhost:8000
```

### Cloudflare Workers Deployment

The application is currently deployed on Cloudflare Workers with Cloudflare D1 database:

**Live URL:** https://alumni-sql-console.dakshx.workers.dev/

To deploy to Cloudflare Workers:

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Navigate to webapp directory
cd webapp

# Deploy static assets
wrangler deploy
```

The deployment uses:
- **Cloudflare Workers** for global edge computing
- **Cloudflare D1** for SQLite database at the edge
- **Static assets** served from Cloudflare's CDN

---

## Web Console

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Execute current SQL statement |
| `↑` / `↓` | Navigate command history |
| `Tab` | Auto-complete `DESC <TABLE>` |
| `Ctrl+L` / `Cmd+L` | Clear terminal output |
| `Ctrl+Enter` / `Cmd+Enter` | Focus input |

### Built-in Commands

| Command | Description |
|---------|-------------|
| `HELP` | Show available commands |
| `TABLES` | List all tables with column counts |
| `DESC <table>` | Describe table columns and types |
| `HISTORY` | Show recent command history |
| `CLEAR` / `CLS` | Clear terminal |
| `EXIT` / `QUIT` | Session info |

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve frontend (index.html) |
| GET | `/api/health` | Database connectivity check |
| GET | `/api/schema` | Get all tables with columns and types |
| GET | `/api/stats` | Get record counts per entity |
| POST | `/api/query` | Execute SQL statement |

### POST /api/query

**Request:**
```json
{
  "sql": "SELECT * FROM ALUMNI WHERE DeptID = 10;"
}
```

**Response (SELECT):**
```json
{
  "ok": true,
  "kind": "query",
  "columns": ["AlumniID", "FirstName", "LastName", "Email", "DeptID", "BatchID", "CompanyID", "CurrentPosition", "IsActive"],
  "rows": [[1, "Aarav", "Mehta", "aarav.mehta@gmail.com", 10, 1, 101, "Systems Engineer", 1]],
  "rowCount": 1,
  "truncated": false,
  "elapsedMs": 5.2
}
```

**Response (DML):**
```json
{
  "ok": true,
  "kind": "execute",
  "message": "Statement executed. 1 row(s) affected.",
  "rowCount": 1,
  "elapsedMs": 3.1
}
```

---

## Preset Queries

The web console includes **100+ preset SQL queries** organized by category:

### Core Queries
- Alumni directory with department, batch, and company
- Alumni phone numbers (multivalued attribute)
- Mentorship pairs (weak entity)
- Donations above average
- Events with attendance count
- Jobs posted by alumni
- Donation totals per donor
- Skills of each alumni (M:N relationship)
- Students with emails (multivalued attribute)

### DDL (Data Definition Language)
- CREATE TABLE with PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT, UNIQUE, NOT NULL
- ALTER TABLE (ADD, MODIFY, DROP COLUMN, RENAME)
- DROP TABLE, TRUNCATE TABLE
- CREATE INDEX, CREATE UNIQUE INDEX, DROP INDEX
- CREATE VIEW, DROP VIEW

### DML (Data Manipulation Language)
- INSERT (single row, multiple rows, specific columns)
- SELECT with WHERE, AND/OR, IN, LIKE, BETWEEN, IS NULL
- UPDATE with conditions
- DELETE with conditions
- ORDER BY, LIMIT, OFFSET, DISTINCT

### Functions
- **Numeric:** SQRT, ABS, CEIL, FLOOR, ROUND
- **String:** SUBSTR, UPPER, LOWER, LENGTH, TRIM, CONCAT, REPLACE
- **Date:** CURRENT_DATE, DATE arithmetic, STRFTIME, JULIANDAY, UNIXEPOCH
- **Aggregate:** COUNT, SUM, AVG, MAX, MIN, GROUP_CONCAT
- **Conversion:** CAST, TYPEOF, HEX, PRINTF

### Joins
- INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN
- CROSS JOIN, SELF JOIN
- Multiple JOINs with aggregation

### Subqueries
- IN, NOT IN, EXISTS, NOT EXISTS
- Correlated subqueries
- Subqueries in FROM clause
- > ALL, > ANY operators
- Nested subqueries

### Analytic Functions
- ROW_NUMBER, RANK, DENSE_RANK, NTILE
- LEAD, LAG, FIRST_VALUE, LAST_VALUE
- PERCENT_RANK, CUME_DIST
- Window PARTITION BY, running totals, moving averages

### Set Operations
- UNION, UNION ALL
- INTERSECT
- EXCEPT

---

## SQL Features

### Cloudflare D1 (Current Deployment)
- ✅ **DQL**: Complete SELECT functionality with complex queries, joins, subqueries
- ✅ **DML**: INSERT, UPDATE, DELETE with full support
- ✅ **DDL**: CREATE, ALTER, DROP tables and indexes
- ✅ **Window Functions**: ROW_NUMBER(), RANK(), LAG(), LEAD(), etc.
- ✅ **CTEs**: Common Table Expressions
- ✅ **Aggregations**: COUNT, SUM, AVG, MAX, MIN, GROUP BY
- ✅ **String Functions**: UPPER, LOWER, LENGTH, SUBSTR, REPLACE, etc.
- ✅ **Numeric Functions**: ABS, ROUND, CEIL, FLOOR, SQRT, etc.
- ✅ **Date Functions**: CURRENT_DATE, date arithmetic, etc.
- ⚠️ **Transactions**: Limited support (requires JavaScript API)
- ❌ **PL/SQL**: No stored procedures, triggers, or procedural blocks

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `8000` | Server port |
| `MAX_ROWS` | `1000` | Maximum rows returned per query |
| `DATABASE_URL` | (empty) | PostgreSQL connection string (enables PostgreSQL mode) |
| `ALLOWED_ORIGIN` | `*` | CORS allowed origin |

---

## Troubleshooting

### Database Connection Issues
- **SQLite**: Ensure write permissions in the application directory
- **Cloudflare D1**: Check D1 database binding in wrangler.jsonc

### Deployment Issues
- **Cloudflare Workers**: Verify wrangler.jsonc configuration
- **Local**: Ensure virtual environment is activated and dependencies installed

### Query Errors
- **Syntax**: Check SQL syntax for SQLite/Cloudflare D1
- **Permissions**: Verify user has required database permissions
- **Constraints**: Foreign key constraints may prevent certain operations

### Performance Issues
- **Large Results**: Use LIMIT clause or reduce MAX_ROWS environment variable
- **Complex Queries**: Consider adding indexes for frequently joined columns
- **Network**: Cloudflare Workers may have latency depending on location
