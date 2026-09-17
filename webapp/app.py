"""
Alumni Network and Engagement Platform - Query Console
Flask backend: executes SQL typed in the GUI against a live database.

Run:
    python webapp/app.py
    -> open http://localhost:8000

Database (auto-selected):
    1. If DATABASE_URL env var is set → PostgreSQL (Neon/Supabase/Railway)
    2. Otherwise → SQLite (auto-creates and seeds on first run)
"""
import datetime
import os
import re
import sqlite3
import time
from decimal import Decimal
from pathlib import Path
from dotenv import load_dotenv

from flask import Flask, jsonify, request, send_from_directory

# Load environment variables from .env file
load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
MAX_ROWS = int(os.getenv("MAX_ROWS", "1000"))
DB_PATH = Path(__file__).parent / "alumni.db"

# Detect database engine from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")
USE_POSTGRES = bool(DATABASE_URL)

app = Flask(__name__, static_folder="static", static_url_path="")


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = os.getenv("ALLOWED_ORIGIN", "*")
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


def _json_value(v):
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime.datetime):
        return v.isoformat(sep=" ", timespec="seconds")
    if isinstance(v, (datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def _strip_sql(sql: str) -> str:
    sql = sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1].rstrip()
    return sql


def _statement_kind(sql: str) -> str:
    first = re.match(r"\s*([A-Za-z]+)", sql)
    kw = first.group(1).upper() if first else ""
    if kw in ("SELECT", "WITH", "EXPLAIN"):
        return "query"
    return "execute"


# ================================================================
# PostgreSQL backend (cloud — Neon, Supabase, Railway, etc.)
# ================================================================
if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
    import psycopg2.pool

    pg_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1, maxconn=10, dsn=DATABASE_URL
    )

    def _init_postgres():
        """Create and seed PostgreSQL schema if tables don't exist."""
        conn = pg_pool.getconn()
        try:
            conn.autocommit = True
            cur = conn.cursor()
            # Check if schema exists
            cur.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alumni')"
            )
            if cur.fetchone()[0]:
                return  # Already initialized

            print("[db] Initializing PostgreSQL schema...")
            cur.execute("""
                CREATE TABLE DEPARTMENT (
                    DeptID           INTEGER PRIMARY KEY,
                    DeptName         TEXT NOT NULL UNIQUE,
                    DeptCode         TEXT NOT NULL UNIQUE,
                    HODName          TEXT,
                    EstablishedYear  INTEGER
                );

                CREATE TABLE BATCH (
                    BatchID       INTEGER PRIMARY KEY,
                    BatchYear     INTEGER NOT NULL CHECK (BatchYear BETWEEN 1990 AND 2100),
                    Section       TEXT,
                    TotalStudent  INTEGER DEFAULT 0 CHECK (TotalStudent >= 0),
                    DeptID        INTEGER REFERENCES DEPARTMENT(DeptID)
                );

                CREATE TABLE COMPANY (
                    CompanyID      INTEGER PRIMARY KEY,
                    CompanyName    TEXT NOT NULL UNIQUE,
                    Industry       TEXT,
                    CompanySize    TEXT,
                    Website        TEXT,
                    Headquarters   TEXT
                );

                CREATE TABLE SKILL (
                    SkillID         INTEGER PRIMARY KEY,
                    SkillName       TEXT NOT NULL UNIQUE,
                    SkillCategory   TEXT,
                    Description     TEXT
                );

                CREATE TABLE ALUMNI (
                    AlumniID         INTEGER PRIMARY KEY,
                    FirstName        TEXT NOT NULL,
                    LastName         TEXT,
                    Email            TEXT NOT NULL UNIQUE,
                    DateOfBirth      TEXT,
                    Address          TEXT,
                    DeptID           INTEGER REFERENCES DEPARTMENT(DeptID),
                    BatchID          INTEGER REFERENCES BATCH(BatchID),
                    CompanyID        INTEGER REFERENCES COMPANY(CompanyID),
                    CurrentPosition  TEXT,
                    LinkedInProfile  TEXT,
                    IsActive         INTEGER DEFAULT 1 CHECK (IsActive IN (0, 1))
                );

                CREATE TABLE ALUMNI_PHONE (
                    AlumniID     INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                    PhoneNumber  TEXT NOT NULL,
                    PRIMARY KEY (AlumniID, PhoneNumber)
                );

                CREATE TABLE STUDENT (
                    StudentID        TEXT PRIMARY KEY,
                    FirstName        TEXT NOT NULL,
                    LastName         TEXT,
                    DeptID           INTEGER REFERENCES DEPARTMENT(DeptID),
                    BatchID          INTEGER REFERENCES BATCH(BatchID),
                    EnrollmentYear   INTEGER,
                    CurrentSemester  INTEGER CHECK (CurrentSemester BETWEEN 1 AND 12),
                    CGPA             REAL CHECK (CGPA BETWEEN 0 AND 10)
                );

                CREATE TABLE STUDENT_EMAIL (
                    StudentID  TEXT NOT NULL REFERENCES STUDENT(StudentID) ON DELETE CASCADE,
                    Email      TEXT NOT NULL,
                    PRIMARY KEY (StudentID, Email)
                );

                CREATE TABLE MENTORSHIP (
                    AlumniID        INTEGER NOT NULL REFERENCES ALUMNI(AlumniID),
                    MentorshipID    TEXT NOT NULL,
                    StudentID       TEXT REFERENCES STUDENT(StudentID),
                    StartDate       TEXT,
                    EndDate         TEXT,
                    Status          TEXT DEFAULT 'Active'
                                    CHECK (Status IN ('Active', 'Completed', 'Terminated')),
                    MentorshipArea  TEXT,
                    Goals           TEXT,
                    PRIMARY KEY (AlumniID, MentorshipID)
                );

                CREATE TABLE EVENT (
                    EventID      INTEGER PRIMARY KEY,
                    EventName    TEXT NOT NULL,
                    EventType    TEXT,
                    EventDate    TEXT,
                    Venue        TEXT,
                    OrganizerID  INTEGER REFERENCES ALUMNI(AlumniID)
                );

                CREATE TABLE DONATION (
                    DonationID     INTEGER PRIMARY KEY,
                    Amount         REAL CHECK (Amount > 0),
                    DonationDate   TEXT,
                    PaymentMethod  TEXT,
                    DonorID        INTEGER REFERENCES ALUMNI(AlumniID)
                );

                CREATE TABLE JOB (
                    JobID      INTEGER PRIMARY KEY,
                    JobTitle   TEXT NOT NULL,
                    JobType    TEXT,
                    Salary     TEXT,
                    CompanyID  INTEGER REFERENCES COMPANY(CompanyID),
                    PostedBy   INTEGER REFERENCES ALUMNI(AlumniID)
                );

                CREATE TABLE ALUMNI_SKILL (
                    AlumniID  INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                    SkillID   INTEGER NOT NULL REFERENCES SKILL(SkillID),
                    PRIMARY KEY (AlumniID, SkillID)
                );

                CREATE TABLE ALUMNI_EVENT (
                    AlumniID  INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                    EventID   INTEGER NOT NULL REFERENCES EVENT(EventID),
                    PRIMARY KEY (AlumniID, EventID)
                );
            """)

            print("[db] Seeding PostgreSQL with sample data...")
            cur.execute("""
                INSERT INTO DEPARTMENT VALUES (10, 'Computer Science and Engineering', 'CSE', 'Dr. Meera Krishnan', 1985);
                INSERT INTO DEPARTMENT VALUES (11, 'Information Technology', 'IT', 'Dr. Rajesh Iyer', 1992);
                INSERT INTO DEPARTMENT VALUES (12, 'Electronics and Communication', 'ECE', 'Dr. Kavya Menon', 1988);
                INSERT INTO DEPARTMENT VALUES (13, 'Mechanical Engineering', 'MECH', 'Dr. Suresh Babu', 1980);
                INSERT INTO DEPARTMENT VALUES (14, 'Business Administration', 'MBA', 'Dr. Anita Desai', 1995);

                INSERT INTO BATCH VALUES (1, 2019, 'A', 60, 10);
                INSERT INTO BATCH VALUES (2, 2020, 'A', 55, 10);
                INSERT INTO BATCH VALUES (3, 2020, 'B', 58, 11);
                INSERT INTO BATCH VALUES (4, 2021, 'A', 62, 12);
                INSERT INTO BATCH VALUES (5, 2022, 'A', 50, 14);

                INSERT INTO COMPANY VALUES (101, 'TCS', 'IT Services', '1000+', 'https://www.tcs.com', 'Mumbai');
                INSERT INTO COMPANY VALUES (102, 'Infosys', 'IT Services', '1000+', 'https://www.infosys.com', 'Bengaluru');
                INSERT INTO COMPANY VALUES (103, 'Google', 'Technology', '1000+', 'https://www.google.com', 'Mountain View');
                INSERT INTO COMPANY VALUES (104, 'Reliance Industries', 'Conglomerate', '1000+', 'https://www.ril.com', 'Mumbai');
                INSERT INTO COMPANY VALUES (105, 'Zoho Corporation', 'Software Products', '201-1000', 'https://www.zoho.com', 'Chennai');

                INSERT INTO SKILL VALUES (1, 'Python', 'Programming', 'General-purpose programming language');
                INSERT INTO SKILL VALUES (2, 'Java', 'Programming', 'Object-oriented programming language');
                INSERT INTO SKILL VALUES (3, 'SQL', 'Database', 'Structured Query Language');
                INSERT INTO SKILL VALUES (4, 'Web Development', 'Software', 'Front-end and back-end development');
                INSERT INTO SKILL VALUES (5, 'Machine Learning', 'AI/ML', 'Statistical learning algorithms');
                INSERT INTO SKILL VALUES (6, 'Cloud Computing', 'Infrastructure', 'AWS / Azure / GCP platforms');
                INSERT INTO SKILL VALUES (7, 'Public Speaking', 'Soft Skill', 'Effective presentation skills');
                INSERT INTO SKILL VALUES (8, 'Data Analysis', 'Analytics', 'Exploratory data analysis and visualisation');

                INSERT INTO ALUMNI VALUES (1, 'Aarav', 'Mehta', 'aarav.mehta@gmail.com', '1997-05-12', 'Chennai, Tamil Nadu', 10, 1, 101, 'Systems Engineer', 'linkedin.com/in/aaravmehta', 1);
                INSERT INTO ALUMNI VALUES (2, 'Priya', 'Nair', 'priya.nair@gmail.com', '1998-09-25', 'Bengaluru, Karnataka', 10, 2, 102, 'Software Engineer', 'linkedin.com/in/priyanair', 1);
                INSERT INTO ALUMNI VALUES (3, 'Rohan', 'Gupta', 'rohan.gupta@gmail.com', '1997-01-30', 'Hyderabad, Telangana', 11, 3, 103, 'Data Scientist', 'linkedin.com/in/rohangupta', 1);
                INSERT INTO ALUMNI VALUES (4, 'Sneha', 'Iyer', 'sneha.iyer@gmail.com', '1999-03-18', 'Chennai, Tamil Nadu', 12, 4, 104, 'Business Analyst', 'linkedin.com/in/snehaiyer', 1);
                INSERT INTO ALUMNI VALUES (5, 'Vikram', 'Singh', 'vikram.singh@gmail.com', '1998-11-08', 'Coimbatore, Tamil Nadu', 14, 5, 105, 'Product Manager', 'linkedin.com/in/vikramsingh', 1);

                INSERT INTO ALUMNI_PHONE VALUES (1, '9876543210');
                INSERT INTO ALUMNI_PHONE VALUES (1, '9876500011');
                INSERT INTO ALUMNI_PHONE VALUES (2, '9123456780');
                INSERT INTO ALUMNI_PHONE VALUES (3, '9988776655');
                INSERT INTO ALUMNI_PHONE VALUES (4, '9090909090');
                INSERT INTO ALUMNI_PHONE VALUES (5, '9843012345');

                INSERT INTO STUDENT VALUES ('S1001', 'Kiran', 'Raj', 10, 2, 2023, 5, 8.75);
                INSERT INTO STUDENT VALUES ('S1002', 'Divya', 'Sharma', 10, 2, 2023, 5, 9.10);
                INSERT INTO STUDENT VALUES ('S1003', 'Arjun', 'Kamath', 11, 3, 2022, 7, 8.20);
                INSERT INTO STUDENT VALUES ('S1004', 'Nithya', 'Ravi', 12, 4, 2022, 7, 8.95);
                INSERT INTO STUDENT VALUES ('S1005', 'Mohammed', 'Asif', 14, 5, 2023, 4, 8.50);

                INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiran.raj@student.edu');
                INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiranraj@gmail.com');
                INSERT INTO STUDENT_EMAIL VALUES ('S1002', 'divya.sharma@student.edu');
                INSERT INTO STUDENT_EMAIL VALUES ('S1003', 'arjun.kamath@student.edu');
                INSERT INTO STUDENT_EMAIL VALUES ('S1004', 'nithya.ravi@student.edu');
                INSERT INTO STUDENT_EMAIL VALUES ('S1005', 'mohammed.asif@student.edu');

                INSERT INTO MENTORSHIP VALUES (1, 'M1', 'S1001', '2024-06-01', NULL, 'Active', 'Data Science', 'Build ML fundamentals and a capstone project');
                INSERT INTO MENTORSHIP VALUES (1, 'M2', 'S1002', '2024-08-15', '2025-02-15', 'Completed', 'Career Guidance', 'Internship preparation and resume review');
                INSERT INTO MENTORSHIP VALUES (2, 'M3', 'S1003', '2024-07-10', NULL, 'Active', 'Web Development', 'Full-stack project mentoring');
                INSERT INTO MENTORSHIP VALUES (3, 'M4', 'S1004', '2025-01-05', NULL, 'Active', 'Research', 'Publish a conference paper on IoT');

                INSERT INTO EVENT VALUES (1, 'Annual Tech Reunion 2024', 'Reunion', '2024-12-21', 'VIT Chennai Auditorium', 1);
                INSERT INTO EVENT VALUES (2, 'AI in Industry Workshop', 'Workshop', '2025-03-14', 'CSE Lab Complex', 2);
                INSERT INTO EVENT VALUES (3, 'Alumni Career Fair', 'Seminar', '2025-08-02', 'Main Grounds', 3);
                INSERT INTO EVENT VALUES (4, 'Entrepreneurship Talk', 'Seminar', '2025-09-20', 'MBA Block Seminar Hall', 5);

                INSERT INTO DONATION VALUES (1, 50000, '2024-03-15', 'Online', 1);
                INSERT INTO DONATION VALUES (2, 75000, '2024-01-10', 'Check', 2);
                INSERT INTO DONATION VALUES (3, 25000, '2024-07-22', 'UPI', 3);
                INSERT INTO DONATION VALUES (4, 40000, '2025-02-18', 'DD', 4);
                INSERT INTO DONATION VALUES (5, 60000, '2025-06-30', 'Check', 5);

                INSERT INTO JOB VALUES (1, 'Software Engineer Trainee', 'Full-Time', 'Rs. 6-8 LPA', 101, 1);
                INSERT INTO JOB VALUES (2, 'Systems Engineer', 'Full-Time', 'Rs. 7-9 LPA', 101, 2);
                INSERT INTO JOB VALUES (3, 'Data Analyst Intern', 'Internship', 'Rs. 30k/month', 103, 3);
                INSERT INTO JOB VALUES (4, 'Business Analyst', 'Full-Time', 'Rs. 12-18 LPA', 102, 4);
                INSERT INTO JOB VALUES (5, 'Product Management Intern', 'Internship', 'Rs. 45k/month', 105, 5);

                INSERT INTO ALUMNI_SKILL VALUES (1, 1), (1, 3), (1, 4), (2, 2), (2, 4);
                INSERT INTO ALUMNI_SKILL VALUES (3, 1), (3, 5), (3, 8), (4, 7), (4, 8);
                INSERT INTO ALUMNI_SKILL VALUES (5, 6), (5, 7);

                INSERT INTO ALUMNI_EVENT VALUES (1, 1), (2, 1), (3, 1), (1, 2), (2, 2);
                INSERT INTO ALUMNI_EVENT VALUES (3, 3), (4, 3), (5, 4);
            """)
            print("[db] PostgreSQL initialized and seeded.")
        finally:
            pg_pool.putconn(conn)

    _init_postgres()

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/api/health")
    def health():
        conn = pg_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            return jsonify(ok=True, engine="PostgreSQL", database="cloud")
        except Exception as exc:
            return jsonify(ok=False, error=str(exc)), 503
        finally:
            pg_pool.putconn(conn)

    @app.get("/api/schema")
    def schema():
        tables = {}
        conn = pg_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' ORDER BY table_name
            """)
            table_names = [row[0] for row in cur.fetchall()]
            for tname in table_names:
                cur.execute("""
                    SELECT column_name, data_type,
                           CASE WHEN column_name = ANY(
                               SELECT kcu.column_name
                               FROM information_schema.table_constraints tc
                               JOIN information_schema.key_column_usage kcu
                                 ON tc.constraint_name = kcu.constraint_name
                               WHERE tc.constraint_type = 'PRIMARY KEY'
                                 AND tc.table_name = %s
                           ) THEN 1 ELSE 0 END AS is_pk
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                """, (tname, tname))
                columns = []
                pk_cols = []
                for cname, dtype, is_pk in cur.fetchall():
                    # Return uppercase names for frontend compatibility
                    columns.append({"name": cname.upper(), "type": dtype.upper()})
                    if is_pk:
                        pk_cols.append(cname.upper())
                tables[tname.upper()] = {"columns": columns, "pk": pk_cols}
        finally:
            pg_pool.putconn(conn)
        return jsonify(tables=tables)

    @app.get("/api/stats")
    def stats():
        counts = {}
        try:
            conn = pg_pool.getconn()
            cur = conn.cursor()
            for key, table in (
                ("alumni", "alumni"),
                ("students", "student"),
                ("events", "event"),
                ("donations", "donation"),
            ):
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                counts[key] = cur.fetchone()[0]
            pg_pool.putconn(conn)
            return jsonify(database="cloud", engine="PostgreSQL", stats=counts)
        except Exception as exc:
            if conn:
                pg_pool.putconn(conn)
            return jsonify(database="cloud", engine="PostgreSQL", stats={}, error=str(exc)), 503

    @app.post("/api/query")
    def run_query():
        body = request.get_json(silent=True) or {}
        sql = _strip_sql(str(body.get("sql", "")))
        if not sql:
            return jsonify(error="Empty statement."), 400
        if "\x00" in sql:
            return jsonify(error="Invalid characters in statement."), 400

        kind = _statement_kind(sql)
        started = time.perf_counter()
        conn = pg_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            if kind == "query":
                cols = [desc[0] for desc in cur.description] if cur.description else []
                rows = cur.fetchmany(MAX_ROWS)
                data = [[_json_value(v) for v in row] for row in rows]
                elapsed = round((time.perf_counter() - started) * 1000, 1)
                pg_pool.putconn(conn)
                return jsonify(
                    ok=True, kind="query", columns=cols, rows=data,
                    rowCount=len(data), truncated=len(rows) == MAX_ROWS,
                    elapsedMs=elapsed,
                )
            conn.commit()
            affected = cur.rowcount if cur.rowcount and cur.rowcount > -1 else 0
            elapsed = round((time.perf_counter() - started) * 1000, 1)
            pg_pool.putconn(conn)
            return jsonify(
                ok=True, kind="execute",
                message=f"Statement executed. {affected} row(s) affected.",
                rowCount=affected, elapsedMs=elapsed,
            )
        except Exception as exc:
            conn.rollback()
            pg_pool.putconn(conn)
            return jsonify(error=str(exc)), 400

    @app.route("/api/query", methods=["OPTIONS"])
    def query_preflight():
        return "", 204


# ================================================================
# SQLite backend (default for local development)
# ================================================================
else:
    def _init_sqlite():
        """Create and seed the SQLite database if it doesn't exist."""
        if DB_PATH.exists():
            return
        print(f"[db] Initializing SQLite database at {DB_PATH}...")
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        cur.executescript("""
            CREATE TABLE DEPARTMENT (
                DeptID           INTEGER PRIMARY KEY,
                DeptName         TEXT NOT NULL UNIQUE,
                DeptCode         TEXT NOT NULL UNIQUE,
                HODName          TEXT,
                EstablishedYear  INTEGER
            );

            CREATE TABLE BATCH (
                BatchID       INTEGER PRIMARY KEY,
                BatchYear     INTEGER NOT NULL CHECK (BatchYear BETWEEN 1990 AND 2100),
                Section       TEXT,
                TotalStudent  INTEGER DEFAULT 0 CHECK (TotalStudent >= 0),
                DeptID        INTEGER REFERENCES DEPARTMENT(DeptID)
            );

            CREATE TABLE COMPANY (
                CompanyID      INTEGER PRIMARY KEY,
                CompanyName    TEXT NOT NULL UNIQUE,
                Industry       TEXT,
                CompanySize    TEXT,
                Website        TEXT,
                Headquarters   TEXT
            );

            CREATE TABLE SKILL (
                SkillID         INTEGER PRIMARY KEY,
                SkillName       TEXT NOT NULL UNIQUE,
                SkillCategory   TEXT,
                Description     TEXT
            );

            CREATE TABLE ALUMNI (
                AlumniID         INTEGER PRIMARY KEY,
                FirstName        TEXT NOT NULL,
                LastName         TEXT,
                Email            TEXT NOT NULL UNIQUE,
                DateOfBirth      TEXT,
                Address          TEXT,
                DeptID           INTEGER REFERENCES DEPARTMENT(DeptID),
                BatchID          INTEGER REFERENCES BATCH(BatchID),
                CompanyID        INTEGER REFERENCES COMPANY(CompanyID),
                CurrentPosition  TEXT,
                LinkedInProfile  TEXT,
                IsActive         INTEGER DEFAULT 1 CHECK (IsActive IN (0, 1))
            );

            CREATE TABLE ALUMNI_PHONE (
                AlumniID     INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                PhoneNumber  TEXT NOT NULL,
                PRIMARY KEY (AlumniID, PhoneNumber)
            );

            CREATE TABLE STUDENT (
                StudentID        TEXT PRIMARY KEY,
                FirstName        TEXT NOT NULL,
                LastName         TEXT,
                DeptID           INTEGER REFERENCES DEPARTMENT(DeptID),
                BatchID          INTEGER REFERENCES BATCH(BatchID),
                EnrollmentYear   INTEGER,
                CurrentSemester  INTEGER CHECK (CurrentSemester BETWEEN 1 AND 12),
                CGPA             REAL CHECK (CGPA BETWEEN 0 AND 10)
            );

            CREATE TABLE STUDENT_EMAIL (
                StudentID  TEXT NOT NULL REFERENCES STUDENT(StudentID) ON DELETE CASCADE,
                Email      TEXT NOT NULL,
                PRIMARY KEY (StudentID, Email)
            );

            CREATE TABLE MENTORSHIP (
                AlumniID        INTEGER NOT NULL REFERENCES ALUMNI(AlumniID),
                MentorshipID    TEXT NOT NULL,
                StudentID       TEXT REFERENCES STUDENT(StudentID),
                StartDate       TEXT,
                EndDate         TEXT,
                Status          TEXT DEFAULT 'Active'
                                CHECK (Status IN ('Active', 'Completed', 'Terminated')),
                MentorshipArea  TEXT,
                Goals           TEXT,
                PRIMARY KEY (AlumniID, MentorshipID)
            );

            CREATE TABLE EVENT (
                EventID      INTEGER PRIMARY KEY,
                EventName    TEXT NOT NULL,
                EventType    TEXT,
                EventDate    TEXT,
                Venue        TEXT,
                OrganizerID  INTEGER REFERENCES ALUMNI(AlumniID)
            );

            CREATE TABLE DONATION (
                DonationID     INTEGER PRIMARY KEY,
                Amount         REAL CHECK (Amount > 0),
                DonationDate   TEXT,
                PaymentMethod  TEXT,
                DonorID        INTEGER REFERENCES ALUMNI(AlumniID)
            );

            CREATE TABLE JOB (
                JobID      INTEGER PRIMARY KEY,
                JobTitle   TEXT NOT NULL,
                JobType    TEXT,
                Salary     TEXT,
                CompanyID  INTEGER REFERENCES COMPANY(CompanyID),
                PostedBy   INTEGER REFERENCES ALUMNI(AlumniID)
            );

            CREATE TABLE ALUMNI_SKILL (
                AlumniID  INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                SkillID   INTEGER NOT NULL REFERENCES SKILL(SkillID),
                PRIMARY KEY (AlumniID, SkillID)
            );

            CREATE TABLE ALUMNI_EVENT (
                AlumniID  INTEGER NOT NULL REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
                EventID   INTEGER NOT NULL REFERENCES EVENT(EventID),
                PRIMARY KEY (AlumniID, EventID)
            );

            CREATE INDEX IX_ALUMNI_DEPT    ON ALUMNI(DeptID);
            CREATE INDEX IX_ALUMNI_BATCH   ON ALUMNI(BatchID);
            CREATE INDEX IX_MNT_STUDENT    ON MENTORSHIP(StudentID);
            CREATE INDEX IX_EVENT_ORG      ON EVENT(OrganizerID);
            CREATE INDEX IX_DON_DONOR      ON DONATION(DonorID);
            CREATE INDEX IX_JOB_POSTEDBY   ON JOB(PostedBy);
        """)

        cur.executescript("""
            INSERT INTO DEPARTMENT VALUES (10, 'Computer Science and Engineering', 'CSE', 'Dr. Meera Krishnan', 1985);
            INSERT INTO DEPARTMENT VALUES (11, 'Information Technology', 'IT', 'Dr. Rajesh Iyer', 1992);
            INSERT INTO DEPARTMENT VALUES (12, 'Electronics and Communication', 'ECE', 'Dr. Kavya Menon', 1988);
            INSERT INTO DEPARTMENT VALUES (13, 'Mechanical Engineering', 'MECH', 'Dr. Suresh Babu', 1980);
            INSERT INTO DEPARTMENT VALUES (14, 'Business Administration', 'MBA', 'Dr. Anita Desai', 1995);

            INSERT INTO BATCH VALUES (1, 2019, 'A', 60, 10);
            INSERT INTO BATCH VALUES (2, 2020, 'A', 55, 10);
            INSERT INTO BATCH VALUES (3, 2020, 'B', 58, 11);
            INSERT INTO BATCH VALUES (4, 2021, 'A', 62, 12);
            INSERT INTO BATCH VALUES (5, 2022, 'A', 50, 14);

            INSERT INTO COMPANY VALUES (101, 'TCS', 'IT Services', '1000+', 'https://www.tcs.com', 'Mumbai');
            INSERT INTO COMPANY VALUES (102, 'Infosys', 'IT Services', '1000+', 'https://www.infosys.com', 'Bengaluru');
            INSERT INTO COMPANY VALUES (103, 'Google', 'Technology', '1000+', 'https://www.google.com', 'Mountain View');
            INSERT INTO COMPANY VALUES (104, 'Reliance Industries', 'Conglomerate', '1000+', 'https://www.ril.com', 'Mumbai');
            INSERT INTO COMPANY VALUES (105, 'Zoho Corporation', 'Software Products', '201-1000', 'https://www.zoho.com', 'Chennai');

            INSERT INTO SKILL VALUES (1, 'Python', 'Programming', 'General-purpose programming language');
            INSERT INTO SKILL VALUES (2, 'Java', 'Programming', 'Object-oriented programming language');
            INSERT INTO SKILL VALUES (3, 'SQL', 'Database', 'Structured Query Language');
            INSERT INTO SKILL VALUES (4, 'Web Development', 'Software', 'Front-end and back-end development');
            INSERT INTO SKILL VALUES (5, 'Machine Learning', 'AI/ML', 'Statistical learning algorithms');
            INSERT INTO SKILL VALUES (6, 'Cloud Computing', 'Infrastructure', 'AWS / Azure / GCP platforms');
            INSERT INTO SKILL VALUES (7, 'Public Speaking', 'Soft Skill', 'Effective presentation skills');
            INSERT INTO SKILL VALUES (8, 'Data Analysis', 'Analytics', 'Exploratory data analysis and visualisation');

            INSERT INTO ALUMNI VALUES (1, 'Aarav', 'Mehta', 'aarav.mehta@gmail.com', '1997-05-12', 'Chennai, Tamil Nadu', 10, 1, 101, 'Systems Engineer', 'linkedin.com/in/aaravmehta', 1);
            INSERT INTO ALUMNI VALUES (2, 'Priya', 'Nair', 'priya.nair@gmail.com', '1998-09-25', 'Bengaluru, Karnataka', 10, 2, 102, 'Software Engineer', 'linkedin.com/in/priyanair', 1);
            INSERT INTO ALUMNI VALUES (3, 'Rohan', 'Gupta', 'rohan.gupta@gmail.com', '1997-01-30', 'Hyderabad, Telangana', 11, 3, 103, 'Data Scientist', 'linkedin.com/in/rohangupta', 1);
            INSERT INTO ALUMNI VALUES (4, 'Sneha', 'Iyer', 'sneha.iyer@gmail.com', '1999-03-18', 'Chennai, Tamil Nadu', 12, 4, 104, 'Business Analyst', 'linkedin.com/in/snehaiyer', 1);
            INSERT INTO ALUMNI VALUES (5, 'Vikram', 'Singh', 'vikram.singh@gmail.com', '1998-11-08', 'Coimbatore, Tamil Nadu', 14, 5, 105, 'Product Manager', 'linkedin.com/in/vikramsingh', 1);

            INSERT INTO ALUMNI_PHONE VALUES (1, '9876543210');
            INSERT INTO ALUMNI_PHONE VALUES (1, '9876500011');
            INSERT INTO ALUMNI_PHONE VALUES (2, '9123456780');
            INSERT INTO ALUMNI_PHONE VALUES (3, '9988776655');
            INSERT INTO ALUMNI_PHONE VALUES (4, '9090909090');
            INSERT INTO ALUMNI_PHONE VALUES (5, '9843012345');

            INSERT INTO STUDENT VALUES ('S1001', 'Kiran', 'Raj', 10, 2, 2023, 5, 8.75);
            INSERT INTO STUDENT VALUES ('S1002', 'Divya', 'Sharma', 10, 2, 2023, 5, 9.10);
            INSERT INTO STUDENT VALUES ('S1003', 'Arjun', 'Kamath', 11, 3, 2022, 7, 8.20);
            INSERT INTO STUDENT VALUES ('S1004', 'Nithya', 'Ravi', 12, 4, 2022, 7, 8.95);
            INSERT INTO STUDENT VALUES ('S1005', 'Mohammed', 'Asif', 14, 5, 2023, 4, 8.50);

            INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiran.raj@student.edu');
            INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiranraj@gmail.com');
            INSERT INTO STUDENT_EMAIL VALUES ('S1002', 'divya.sharma@student.edu');
            INSERT INTO STUDENT_EMAIL VALUES ('S1003', 'arjun.kamath@student.edu');
            INSERT INTO STUDENT_EMAIL VALUES ('S1004', 'nithya.ravi@student.edu');
            INSERT INTO STUDENT_EMAIL VALUES ('S1005', 'mohammed.asif@student.edu');

            INSERT INTO MENTORSHIP VALUES (1, 'M1', 'S1001', '2024-06-01', NULL, 'Active', 'Data Science', 'Build ML fundamentals and a capstone project');
            INSERT INTO MENTORSHIP VALUES (1, 'M2', 'S1002', '2024-08-15', '2025-02-15', 'Completed', 'Career Guidance', 'Internship preparation and resume review');
            INSERT INTO MENTORSHIP VALUES (2, 'M3', 'S1003', '2024-07-10', NULL, 'Active', 'Web Development', 'Full-stack project mentoring');
            INSERT INTO MENTORSHIP VALUES (3, 'M4', 'S1004', '2025-01-05', NULL, 'Active', 'Research', 'Publish a conference paper on IoT');

            INSERT INTO EVENT VALUES (1, 'Annual Tech Reunion 2024', 'Reunion', '2024-12-21', 'VIT Chennai Auditorium', 1);
            INSERT INTO EVENT VALUES (2, 'AI in Industry Workshop', 'Workshop', '2025-03-14', 'CSE Lab Complex', 2);
            INSERT INTO EVENT VALUES (3, 'Alumni Career Fair', 'Seminar', '2025-08-02', 'Main Grounds', 3);
            INSERT INTO EVENT VALUES (4, 'Entrepreneurship Talk', 'Seminar', '2025-09-20', 'MBA Block Seminar Hall', 5);

            INSERT INTO DONATION VALUES (1, 50000, '2024-03-15', 'Online', 1);
            INSERT INTO DONATION VALUES (2, 75000, '2024-01-10', 'Check', 2);
            INSERT INTO DONATION VALUES (3, 25000, '2024-07-22', 'UPI', 3);
            INSERT INTO DONATION VALUES (4, 40000, '2025-02-18', 'DD', 4);
            INSERT INTO DONATION VALUES (5, 60000, '2025-06-30', 'Check', 5);

            INSERT INTO JOB VALUES (1, 'Software Engineer Trainee', 'Full-Time', 'Rs. 6-8 LPA', 101, 1);
            INSERT INTO JOB VALUES (2, 'Systems Engineer', 'Full-Time', 'Rs. 7-9 LPA', 101, 2);
            INSERT INTO JOB VALUES (3, 'Data Analyst Intern', 'Internship', 'Rs. 30k/month', 103, 3);
            INSERT INTO JOB VALUES (4, 'Business Analyst', 'Full-Time', 'Rs. 12-18 LPA', 102, 4);
            INSERT INTO JOB VALUES (5, 'Product Management Intern', 'Internship', 'Rs. 45k/month', 105, 5);

            INSERT INTO ALUMNI_SKILL VALUES (1, 1), (1, 3), (1, 4), (2, 2), (2, 4);
            INSERT INTO ALUMNI_SKILL VALUES (3, 1), (3, 5), (3, 8), (4, 7), (4, 8);
            INSERT INTO ALUMNI_SKILL VALUES (5, 6), (5, 7);

            INSERT INTO ALUMNI_EVENT VALUES (1, 1), (2, 1), (3, 1), (1, 2), (2, 2);
            INSERT INTO ALUMNI_EVENT VALUES (3, 3), (4, 3), (5, 4);
        """)

        conn.commit()
        conn.close()
        print("[db] SQLite database initialized and seeded.")

    _init_sqlite()

    def _get_conn():
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/api/health")
    def health():
        try:
            conn = _get_conn()
            conn.execute("SELECT 1")
            conn.close()
            return jsonify(ok=True, engine="SQLite", database=str(DB_PATH))
        except Exception as exc:
            return jsonify(ok=False, error=str(exc)), 503

    @app.get("/api/schema")
    def schema():
        tables = {}
        conn = _get_conn()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        table_names = [row[0] for row in cur.fetchall()]
        for tname in table_names:
            cols_cur = conn.execute(f'PRAGMA table_info("{tname}")')
            columns = []
            pk_cols = []
            for col in cols_cur.fetchall():
                columns.append({"name": col[1], "type": col[2] or "TEXT"})
                if col[5]:
                    pk_cols.append(col[1])
            tables[tname] = {"columns": columns, "pk": pk_cols}
        conn.close()
        return jsonify(tables=tables)

    @app.get("/api/stats")
    def stats():
        counts = {}
        try:
            conn = _get_conn()
            for key, table in (
                ("alumni", "ALUMNI"),
                ("students", "STUDENT"),
                ("events", "EVENT"),
                ("donations", "DONATION"),
            ):
                cur = conn.execute(f'SELECT COUNT(*) FROM "{table}"')
                counts[key] = cur.fetchone()[0]
            conn.close()
            return jsonify(database=str(DB_PATH), engine="SQLite", stats=counts)
        except Exception as exc:
            return jsonify(database=str(DB_PATH), engine="SQLite", stats={}, error=str(exc)), 503

    @app.post("/api/query")
    def run_query():
        body = request.get_json(silent=True) or {}
        sql = _strip_sql(str(body.get("sql", "")))
        if not sql:
            return jsonify(error="Empty statement."), 400
        if "\x00" in sql:
            return jsonify(error="Invalid characters in statement."), 400

        kind = _statement_kind(sql)
        started = time.perf_counter()
        conn = _get_conn()
        try:
            cur = conn.execute(sql)
            if kind == "query":
                cols = [desc[0] for desc in cur.description] if cur.description else []
                rows = cur.fetchmany(MAX_ROWS)
                data = [[_json_value(v) for v in row] for row in rows]
                elapsed = round((time.perf_counter() - started) * 1000, 1)
                conn.close()
                return jsonify(
                    ok=True, kind="query", columns=cols, rows=data,
                    rowCount=len(data), truncated=len(rows) == MAX_ROWS,
                    elapsedMs=elapsed,
                )
            conn.commit()
            affected = cur.rowcount if cur.rowcount > -1 else 0
            elapsed = round((time.perf_counter() - started) * 1000, 1)
            conn.close()
            return jsonify(
                ok=True, kind="execute",
                message=f"Statement executed. {affected} row(s) affected.",
                rowCount=affected, elapsedMs=elapsed,
            )
        except Exception as exc:
            conn.rollback()
            conn.close()
            return jsonify(error=str(exc)), 400

    @app.route("/api/query", methods=["OPTIONS"])
    def query_preflight():
        return "", 204


if __name__ == "__main__":
    engine = "PostgreSQL (cloud)" if USE_POSTGRES else "SQLite (local)"
    print(f"[db] Using engine: {engine}")
    app.run(host=HOST, port=PORT, debug=False)
