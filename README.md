# Alumni Network and Engagement Platform

> A comprehensive Database Management System project implementing a full-stack alumni tracking platform with interactive SQL console.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
  - [ER Model](#er-model)
  - [EER Model](#eer-model)
  - [Normalization](#normalization)
  - [Relational Schema](#relational-schema)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick Start (SQLite - No Setup)](#quick-start-sqlite---no-setup)
  - [Docker Deployment (Full Stack)](#docker-deployment-full-stack)
  - [Cloud Deployment](#cloud-deployment)
- [Web Console](#web-console)
- [API Reference](#api-reference)
- [SQL Implementation](#sql-implementation)
- [Lab Exercises & Preset Queries](#lab-exercises--preset-queries)
- [Reports & Documentation](#reports--documentation)
- [Team](#team)
- [References](#references)

---

## Overview

The **Alumni Network and Engagement Platform** is a DBMS project designed to manage alumni information, facilitate networking, track donations, organize events, and enable mentorship opportunities between alumni and current students.

The platform features:
- A **web-based SQL console** that executes queries against a live database in real-time
- **14 normalized relations** (tables) modeling the complete alumni ecosystem
- **100+ preset SQL queries** covering DDL, DML, joins, subqueries, window functions, and lab exercises
- Support for both **SQLite** (zero-config local development) and **PostgreSQL/Oracle** (production)

---

## Features

### Core Functionality
- **Alumni Management** - Store and manage detailed alumni profiles with contact info, employment, and department associations
- **Event Management** - Organize reunions, workshops, seminars, and networking events with attendance tracking
- **Donation Tracking** - Record and analyze alumni contributions with multiple payment methods
- **Mentorship Program** - Connect alumni mentors with current students, track goals and progress
- **Job Portal** - Share job opportunities posted by alumni within the network
- **Skills Tracking** - Map alumni skills across programming, soft skills, and domain expertise

### Web Console Capabilities
- Interactive SQL terminal with command history (↑/↓ arrow keys)
- Tab completion for `DESC` commands
- Real-time query execution with elapsed time display
- Schema browser with clickable column insertion
- 100+ categorized preset queries (one-click run)
- Support for all SQL operations: SELECT, INSERT, UPDATE, DELETE, DDL
- Results rendered as formatted tables with pagination

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12+, Flask |
| **Database** | SQLite (local) / PostgreSQL / Oracle |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Docker, Cloudflare Pages, Netlify |
| **WSGI Server** | Gunicorn |

---

## Project Structure

```
alumni-network/
├── webapp/                     # Flask application & frontend
│   ├── app.py                  # Main Flask backend (769 lines)
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container configuration
│   ├── wrangler.jsonc          # Cloudflare Pages config
│   └── static/
│       ├── index.html          # Main frontend UI
│       ├── app.js              # Console logic & API client (789 lines)
│       ├── style.css           # Complete styling (438 lines)
│       └── config.js           # API base URL configuration
├── sql/                        # Oracle SQL implementation (DA2)
│   ├── 00_drop_all.sql         # Clean teardown script
│   ├── 01_schema.sql           # DDL: tables, constraints, indexes
│   ├── 02_plsql.sql            # Sequences, triggers, procedures, functions
│   ├── 03_seed_data.sql        # Sample data insertion
│   ├── 04_demo_queries.sql     # 14 demonstration scenarios
│   └── run_all.sql             # Master execution script
├── docs/                       # Design documentation
│   ├── ER_Model.md             # Entity-Relationship model details
│   ├── EER_Model.md            # Extended ER model with hierarchies
│   ├── Normalization.md        # 1NF through 5NF analysis
│   └── Relational_Schema.md    # Final relational schema
├── diagrams/                   # Visual diagrams (draw.io)
│   ├── ER_Diagram_V2.drawio
│   ├── EER_Diagram_V2.drawio
│   ├── Normalization.drawio
│   └── Relational_Schema.drawio
├── report/                     # Generated reports & presentations
│   ├── Alumni_Network_Presentation.pptx
│   ├── Alumni_Network_Implementation.docx
│   ├── Alumni_Network_Implementation.pdf
│   └── Alumni_Network_Demo_Presentation.pptx
├── src/                        # Report generation scripts
│   ├── generate_implementation_docx.py
│   ├── generate_implementation_pdf.py
│   └── generate_demo_pptx.py
├── logs/                       # Execution evidence
├── docker-compose.yml          # Full stack orchestration
├── DEMO_SCRIPT.md              # Live demonstration runbook
└── PROJECT_SUMMARY.md          # Complete project summary
```

---

## Database Design

### ER Model

**12 Core Entities:**

| Entity | Description | Primary Key |
|--------|-------------|-------------|
| ALUMNI | Alumni member information | AlumniID |
| STUDENT | Current student information | StudentID |
| DEPARTMENT | Academic departments | DeptID |
| BATCH | Graduation batches | BatchID |
| COMPANY | Employer companies | CompanyID |
| SKILL | Skills catalog | SkillID |
| EVENT | Alumni events | EventID |
| DONATION | Financial contributions | DonationID |
| JOB | Job postings | JobID |
| MENTORSHIP | Mentor-mentee relationships | (AlumniID, MentorshipID) |
| ALUMNI_PHONE | Alumni contact numbers | (AlumniID, PhoneNumber) |
| STUDENT_EMAIL | Student email addresses | (StudentID, Email) |

**Relationships:**

| Relationship | Type | Cardinality |
|--------------|------|-------------|
| ALUMNI → DEPARTMENT | N:1 | Many alumni belong to one department |
| ALUMNI → BATCH | N:1 | Many alumni belong to one batch |
| ALUMNI → COMPANY | N:1 | Many alumni work at one company |
| ALUMNI ↔ SKILL | M:N | Via ALUMNI_SKILL junction table |
| ALUMNI ↔ EVENT | M:N | Via ALUMNI_EVENT junction table |
| ALUMNI → MENTORSHIP | 1:N | Alumni mentors multiple students |
| ALUMNI → ALUMNI_PHONE | 1:N | Multi-valued attribute |
| STUDENT → STUDENT_EMAIL | 1:N | Multi-valued attribute |

### EER Model

**Generalization Hierarchies:**
- **PERSON** (superclass) → ALUMNI, STUDENT, ADMIN (subclasses)
- **CONTENT** (superclass) → POST, COMMENT, REPLY (subclasses)
- **EVENT** (superclass) → REUNION, WORKSHOP, SEMINAR, NETWORKING (subclasses)

**Constraints:**
- Disjoint/Overlapping with total/partial participation
- Aggregation for MENTORSHIP relationship

### Normalization

All relations are normalized up to **BCNF** (Boyce-Codd Normal Form):

| Normal Form | Status |
|-------------|--------|
| 1NF (Atomic values, no repeating groups) | ✅ |
| 2NF (No partial dependencies) | ✅ |
| 3NF (No transitive dependencies) | ✅ |
| BCNF (Every determinant is a candidate key) | ✅ |
| 4NF (No multi-valued dependencies) | ✅ (where applicable) |
| 5NF (No join dependencies) | ✅ (where applicable) |

**Key Design Decisions:**
- Multi-valued attributes (Phone, Email) separated into their own tables
- Many-to-many relationships implemented via junction tables
- All functional dependencies preserved through decomposition
- Lossless join decomposition verified

### Relational Schema

**14 Relations with Constraints:**
- Primary keys on all tables
- Foreign keys with CASCADE delete where appropriate
- CHECK constraints for data validation (CGPA 0-10, BatchYear 1990-2100, etc.)
- UNIQUE constraints on natural keys (Email, DeptCode, CompanyName)
- NOT NULL constraints on essential attributes
- Indexes on foreign key columns for query performance

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git
- Docker (optional, for full-stack deployment)

### Quick Start (SQLite - No Setup)

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

### Docker Deployment (Full Stack)

For production-like deployment with PostgreSQL:

```bash
# Start both database and webapp
docker compose up

# Access the application at http://localhost:8000
```

### Cloud Deployment

#### Option 1: Netlify (Frontend) + Hosted Backend

```bash
# Set environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/alumni"
export ALLOWED_ORIGIN="https://your-frontend.pages.dev"

# Configure frontend
echo 'window.API_BASE = "https://your-backend-url";' > webapp/static/config.js
```

#### Option 2: Render/Railway/Fly.io

Deploy `webapp/` as a Python web service with `DATABASE_URL` environment variable set.

---

## Web Console

The web console provides a terminal-like interface for executing SQL queries against the live database.

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

### Preset Query Categories

- **Core Queries** - Alumni directory, mentorship pairs, donations, events
- **LAB: DDL** - CREATE, ALTER, DROP, TRUNCATE operations
- **LAB: DML** - INSERT, UPDATE, DELETE with various WHERE clauses
- **LAB: Functions** - Numeric, string, date, and aggregate functions
- **LAB: JOINS** - INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF joins
- **LAB: Subquery** - IN, EXISTS, correlated, nested subqueries
- **LAB: Analytic** - ROW_NUMBER, RANK, LEAD, LAG, window functions
- **LAB: Set Ops** - UNION, INTERSECT, EXCEPT operations
- **LAB: Date** - Date arithmetic and formatting
- **LAB: Conversion** - CAST, TYPEOF, PRINTF functions

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
  "columns": ["AlumniID", "FirstName", "LastName", ...],
  "rows": [[1, "Aarav", "Mehta", ...]],
  "rowCount": 5,
  "truncated": false,
  "elapsedMs": 12.5
}
```

**Response (DML):**
```json
{
  "ok": true,
  "kind": "execute",
  "message": "Statement executed. 1 row(s) affected.",
  "rowCount": 1,
  "elapsedMs": 8.2
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `8000` | Server port |
| `MAX_ROWS` | `1000` | Maximum rows returned per query |
| `DATABASE_URL` | (empty) | PostgreSQL connection string (enables PostgreSQL mode) |
| `ALLOWED_ORIGIN` | `*` | CORS allowed origin |

---

## SQL Implementation

The `sql/` directory contains the complete Oracle SQL implementation (DA2 deliverable):

| File | Description | Lines |
|------|-------------|-------|
| `00_drop_all.sql` | Clean teardown of all database objects | ~50 |
| `01_schema.sql` | DDL: 22 tables, 30 FKs, 65 CHECK constraints, 18 indexes | ~400 |
| `02_plsql.sql` | 18 sequences, 22 triggers, 3 views, 4 procedures, 3 functions, 1 package | ~500 |
| `03_seed_data.sql` | Sample data with row-count verification | ~150 |
| `04_demo_queries.sql` | 14 demonstration scenarios | ~100 |
| `run_all.sql` | Master runner producing spool logs | ~30 |

### Running Oracle SQL

```bash
# Connect to Oracle
sqlplus alumni/alumni123@localhost:1521/FREEPDB1

# Run complete implementation
SQL> @sql/run_all.sql

# Run demo queries
SQL> @sql/04_demo_queries.sql
```

---

## Lab Exercises & Preset Queries

The web console includes **100+ preset SQL queries** organized by topic:

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
- EXCEPT (MINUS)

---

## Reports & Documentation

### Generated Reports

| File | Format | Description |
|------|--------|-------------|
| `report/Alumni_Network_Presentation.pptx` | PowerPoint | 26-slide project presentation |
| `report/Alumni_Network_Implementation.docx` | Word | DA2 implementation report |
| `report/Alumni_Network_Implementation.pdf` | PDF | Implementation report (PDF) |
| `report/Alumni_Network_Demo_Presentation.pptx` | PowerPoint | Demo presentation (14 slides) |

### Design Documentation

| File | Description |
|------|-------------|
| `docs/ER_Model.md` | Complete ER model with entities, attributes, relationships |
| `docs/EER_Model.md` | Extended ER model with generalization hierarchies |
| `docs/Normalization.md` | Normalization analysis from 1NF to 5NF |
| `docs/Relational_Schema.md` | Final relational schema with all constraints |

### Diagrams

All diagrams created in draw.io format:
- `diagrams/ER_Diagram_V2.drawio` - Entity-Relationship diagram
- `diagrams/EER_Diagram_V2.drawio` - Extended ER diagram
- `diagrams/Normalization.drawio` - Normalization process visualization
- `diagrams/Relational_Schema.drawio` - Final relational schema diagram

---

## Team

**Course:** Database Management Systems (DBMS)

**Institution:** VIT Chennai

---

## References

1. Silberschatz, A., Korth, H.F., & Sudarshan, S. (2019). *Database System Concepts* (7th ed.)
2. Elmasri, R., & Navathe, S.B. (2015). *Fundamentals of Database Systems* (7th ed.)
3. Connolly, T., & Begg, C. (2014). *Database Systems: A Practical Approach* (6th ed.)
4. Date, C.J. (2003). *An Introduction to Database Systems* (8th ed.)
5. Ramakrishnan, R., & Gehrke, J. (2003). *Database Management Systems* (3rd ed.)
