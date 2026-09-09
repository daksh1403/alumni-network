-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- D1 (SQLite) schema — the same 14 relations from the ER model.
-- Used by the Cloudflare Worker deployment.
-- ====================================================================

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
    DeptID        INTEGER,
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
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
    DeptID           INTEGER,
    BatchID          INTEGER,
    CompanyID        INTEGER,
    CurrentPosition  TEXT,
    LinkedInProfile  TEXT,
    IsActive         INTEGER DEFAULT 1 CHECK (IsActive IN (0, 1)),
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID),
    FOREIGN KEY (BatchID) REFERENCES BATCH(BatchID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

CREATE TABLE ALUMNI_PHONE (
    AlumniID     INTEGER NOT NULL,
    PhoneNumber  TEXT NOT NULL,
    PRIMARY KEY (AlumniID, PhoneNumber),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE
);

CREATE TABLE STUDENT (
    StudentID        TEXT PRIMARY KEY,
    FirstName        TEXT NOT NULL,
    LastName         TEXT,
    DeptID           INTEGER,
    BatchID          INTEGER,
    EnrollmentYear   INTEGER,
    CurrentSemester  INTEGER CHECK (CurrentSemester BETWEEN 1 AND 12),
    CGPA             REAL CHECK (CGPA BETWEEN 0 AND 10),
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID),
    FOREIGN KEY (BatchID) REFERENCES BATCH(BatchID)
);

CREATE TABLE STUDENT_EMAIL (
    StudentID  TEXT NOT NULL,
    Email      TEXT NOT NULL,
    PRIMARY KEY (StudentID, Email),
    FOREIGN KEY (StudentID) REFERENCES STUDENT(StudentID) ON DELETE CASCADE
);

CREATE TABLE MENTORSHIP (
    AlumniID        INTEGER NOT NULL,
    MentorshipID    TEXT NOT NULL,
    StudentID       TEXT,
    StartDate       TEXT,
    EndDate         TEXT,
    Status          TEXT DEFAULT 'Active' CHECK (Status IN ('Active', 'Completed', 'Terminated')),
    MentorshipArea  TEXT,
    Goals           TEXT,
    PRIMARY KEY (AlumniID, MentorshipID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID),
    FOREIGN KEY (StudentID) REFERENCES STUDENT(StudentID)
);

CREATE TABLE EVENT (
    EventID      INTEGER PRIMARY KEY,
    EventName    TEXT NOT NULL,
    EventType    TEXT,
    EventDate    TEXT,
    Venue        TEXT,
    OrganizerID  INTEGER,
    FOREIGN KEY (OrganizerID) REFERENCES ALUMNI(AlumniID)
);

CREATE TABLE DONATION (
    DonationID     INTEGER PRIMARY KEY,
    Amount         REAL CHECK (Amount > 0),
    DonationDate   TEXT,
    PaymentMethod  TEXT,
    DonorID        INTEGER,
    FOREIGN KEY (DonorID) REFERENCES ALUMNI(AlumniID)
);

CREATE TABLE JOB (
    JobID      INTEGER PRIMARY KEY,
    JobTitle   TEXT NOT NULL,
    JobType    TEXT,
    Salary     TEXT,
    CompanyID  INTEGER,
    PostedBy   INTEGER,
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID),
    FOREIGN KEY (PostedBy) REFERENCES ALUMNI(AlumniID)
);

CREATE TABLE ALUMNI_SKILL (
    AlumniID  INTEGER NOT NULL,
    SkillID   INTEGER NOT NULL,
    PRIMARY KEY (AlumniID, SkillID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
    FOREIGN KEY (SkillID) REFERENCES SKILL(SkillID)
);

CREATE TABLE ALUMNI_EVENT (
    AlumniID  INTEGER NOT NULL,
    EventID   INTEGER NOT NULL,
    PRIMARY KEY (AlumniID, EventID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID) ON DELETE CASCADE,
    FOREIGN KEY (EventID) REFERENCES EVENT(EventID)
);

CREATE INDEX IX_ALUMNI_DEPT   ON ALUMNI(DeptID);
CREATE INDEX IX_ALUMNI_BATCH  ON ALUMNI(BatchID);
CREATE INDEX IX_MNT_STUDENT   ON MENTORSHIP(StudentID);
CREATE INDEX IX_EVENT_ORG     ON EVENT(OrganizerID);
CREATE INDEX IX_DON_DONOR     ON DONATION(DonorID);
CREATE INDEX IX_JOB_POSTEDBY  ON JOB(PostedBy);

CREATE VIEW VW_ALUMNI_DIRECTORY AS
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS FullName,
       a.Email,
       a.CurrentPosition,
       c.CompanyName,
       d.DeptName,
       b.BatchYear,
       a.IsActive
FROM ALUMNI a
LEFT JOIN COMPANY c    ON a.CompanyID = c.CompanyID
LEFT JOIN DEPARTMENT d ON a.DeptID = d.DeptID
LEFT JOIN BATCH b      ON a.BatchID = b.BatchID;

CREATE VIEW VW_MENTORSHIP_SUMMARY AS
SELECT m.AlumniID,
       al.FirstName || ' ' || al.LastName AS MentorName,
       m.MentorshipID,
       s.StudentID,
       s.FirstName || ' ' || s.LastName AS StudentName,
       m.MentorshipArea,
       m.Status,
       m.StartDate,
       m.EndDate
FROM MENTORSHIP m
JOIN ALUMNI  al ON m.AlumniID = al.AlumniID
JOIN STUDENT s  ON m.StudentID = s.StudentID;

CREATE VIEW VW_EVENT_ATTENDANCE AS
SELECT e.EventID,
       e.EventName,
       e.EventType,
       e.EventDate,
       e.Venue,
       org.FirstName || ' ' || org.LastName AS Organizer,
       COUNT(ae.AlumniID) AS AttendeeCount
FROM EVENT e
LEFT JOIN ALUMNI_EVENT ae ON e.EventID = ae.EventID
LEFT JOIN ALUMNI org      ON e.OrganizerID = org.AlumniID
GROUP BY e.EventID, e.EventName, e.EventType, e.EventDate, e.Venue,
         org.FirstName, org.LastName;

CREATE VIEW VW_DONATION_TOTALS AS
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS DonorName,
       COUNT(d.DonationID) AS DonationCount,
       IFNULL(SUM(d.Amount), 0) AS TotalAmount
FROM ALUMNI a
LEFT JOIN DONATION d ON d.DonorID = a.AlumniID
GROUP BY a.AlumniID, a.FirstName, a.LastName;
