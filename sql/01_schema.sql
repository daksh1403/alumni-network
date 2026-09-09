-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Part 1: Schema — exactly the 14 relations from the ER model.
--   DEPARTMENT, BATCH, COMPANY, SKILL,
--   ALUMNI, ALUMNI_PHONE, STUDENT, STUDENT_EMAIL,
--   MENTORSHIP, EVENT, DONATION, JOB, ALUMNI_SKILL, ALUMNI_EVENT
-- Target: Oracle 11g+
-- ====================================================================

-- 1. DEPARTMENT
CREATE TABLE DEPARTMENT (
    DeptID           NUMBER(4)      PRIMARY KEY,
    DeptName         VARCHAR2(100)  NOT NULL UNIQUE,
    DeptCode         VARCHAR2(10)   NOT NULL UNIQUE,
    HODName          VARCHAR2(100),
    EstablishedYear  NUMBER(4)
);

-- 2. BATCH  (weak association to department)
CREATE TABLE BATCH (
    BatchID       NUMBER(4)     PRIMARY KEY,
    BatchYear     NUMBER(4)     NOT NULL CHECK (BatchYear BETWEEN 1990 AND 2100),
    Section       VARCHAR2(5),
    TotalStudent  NUMBER(4)     DEFAULT 0 CHECK (TotalStudent >= 0),
    DeptID        NUMBER(4),
    CONSTRAINT FK_BATCH_DEPT FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
);

-- 3. COMPANY
CREATE TABLE COMPANY (
    CompanyID      NUMBER(6)      PRIMARY KEY,
    CompanyName    VARCHAR2(100)  NOT NULL UNIQUE,
    Industry       VARCHAR2(100),
    CompanySize    VARCHAR2(20),
    Website        VARCHAR2(200),
    Headquarters   VARCHAR2(100)
);

-- 4. SKILL
CREATE TABLE SKILL (
    SkillID         NUMBER(4)      PRIMARY KEY,
    SkillName       VARCHAR2(60)   NOT NULL UNIQUE,
    SkillCategory   VARCHAR2(40),
    Description     VARCHAR2(255)
);

-- 5. ALUMNI
CREATE TABLE ALUMNI (
    AlumniID         NUMBER(8)      PRIMARY KEY,
    FirstName        VARCHAR2(50)   NOT NULL,
    LastName         VARCHAR2(50),
    Email            VARCHAR2(120)  NOT NULL UNIQUE,
    DateOfBirth      DATE,
    Address          VARCHAR2(200),
    DeptID           NUMBER(4),
    BatchID          NUMBER(4),
    CompanyID        NUMBER(6),
    CurrentPosition  VARCHAR2(100),
    LinkedInProfile  VARCHAR2(200),
    IsActive         NUMBER(1) DEFAULT 1 CHECK (IsActive IN (0, 1)),
    CONSTRAINT FK_ALUMNI_DEPT    FOREIGN KEY (DeptID)   REFERENCES DEPARTMENT(DeptID),
    CONSTRAINT FK_ALUMNI_BATCH   FOREIGN KEY (BatchID)  REFERENCES BATCH(BatchID),
    CONSTRAINT FK_ALUMNI_COMPANY FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

-- 6. ALUMNI_PHONE  (multivalued: phones of an alumni)
CREATE TABLE ALUMNI_PHONE (
    AlumniID     NUMBER(8)     NOT NULL,
    PhoneNumber  VARCHAR2(15)  NOT NULL,
    CONSTRAINT PK_ALUMNI_PHONE PRIMARY KEY (AlumniID, PhoneNumber),
    CONSTRAINT FK_APHONE_ALUMNI FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID)
        ON DELETE CASCADE
);

-- 7. STUDENT
CREATE TABLE STUDENT (
    StudentID        VARCHAR2(12)   PRIMARY KEY,
    FirstName        VARCHAR2(50)   NOT NULL,
    LastName         VARCHAR2(50),
    DeptID           NUMBER(4),
    BatchID          NUMBER(4),
    EnrollmentYear   NUMBER(4),
    CurrentSemester  NUMBER(2) CHECK (CurrentSemester BETWEEN 1 AND 12),
    CGPA             NUMBER(4,2) CHECK (CGPA BETWEEN 0 AND 10),
    CONSTRAINT FK_STUDENT_DEPT  FOREIGN KEY (DeptID)  REFERENCES DEPARTMENT(DeptID),
    CONSTRAINT FK_STUDENT_BATCH FOREIGN KEY (BatchID) REFERENCES BATCH(BatchID)
);

-- 8. STUDENT_EMAIL  (multivalued: emails of a student)
CREATE TABLE STUDENT_EMAIL (
    StudentID  VARCHAR2(12)   NOT NULL,
    Email      VARCHAR2(120)  NOT NULL,
    CONSTRAINT PK_STUDENT_EMAIL PRIMARY KEY (StudentID, Email),
    CONSTRAINT FK_SEMAIL_STUDENT FOREIGN KEY (StudentID) REFERENCES STUDENT(StudentID)
        ON DELETE CASCADE
);

-- 9. MENTORSHIP  (weak entity owned by ALUMNI; MentorshipID is a partial key)
CREATE TABLE MENTORSHIP (
    AlumniID        NUMBER(8)      NOT NULL,
    MentorshipID    VARCHAR2(12)   NOT NULL,
    StudentID       VARCHAR2(12),
    StartDate       DATE,
    EndDate         DATE,
    Status          VARCHAR2(15) DEFAULT 'Active'
                    CHECK (Status IN ('Active', 'Completed', 'Terminated')),
    MentorshipArea  VARCHAR2(80),
    Goals           VARCHAR2(255),
    CONSTRAINT PK_MENTORSHIP PRIMARY KEY (AlumniID, MentorshipID),
    CONSTRAINT CK_MNT_DATES CHECK (EndDate IS NULL OR EndDate > StartDate),
    CONSTRAINT FK_MNT_ALUMNI  FOREIGN KEY (AlumniID)  REFERENCES ALUMNI(AlumniID),
    CONSTRAINT FK_MNT_STUDENT FOREIGN KEY (StudentID) REFERENCES STUDENT(StudentID)
);

-- 10. EVENT  (organized by one ALUMNI -> 1:N organizes)
CREATE TABLE EVENT (
    EventID      NUMBER(6)      PRIMARY KEY,
    EventName    VARCHAR2(150)  NOT NULL,
    EventType    VARCHAR2(50),
    EventDate    DATE,
    Venue        VARCHAR2(150),
    OrganizerID  NUMBER(8),
    CONSTRAINT FK_EVENT_ORG FOREIGN KEY (OrganizerID) REFERENCES ALUMNI(AlumniID)
);

-- 11. DONATION  (made by an ALUMNI donor)
CREATE TABLE DONATION (
    DonationID     NUMBER(8)      PRIMARY KEY,
    Amount         NUMBER(12,2)   CHECK (Amount > 0),
    DonationDate   DATE,
    PaymentMethod  VARCHAR2(30),
    DonorID        NUMBER(8),
    CONSTRAINT FK_DON_DONOR FOREIGN KEY (DonorID) REFERENCES ALUMNI(AlumniID)
);

-- 12. JOB  (posted by an ALUMNI at a COMPANY)
CREATE TABLE JOB (
    JobID      NUMBER(6)      PRIMARY KEY,
    JobTitle   VARCHAR2(100)  NOT NULL,
    JobType    VARCHAR2(30),
    Salary     VARCHAR2(50),
    CompanyID  NUMBER(6),
    PostedBy   NUMBER(8),
    CONSTRAINT FK_JOB_COMPANY FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID),
    CONSTRAINT FK_JOB_POSTER  FOREIGN KEY (PostedBy)  REFERENCES ALUMNI(AlumniID)
);

-- 13. ALUMNI_SKILL  (M:N alumni has skills)
CREATE TABLE ALUMNI_SKILL (
    AlumniID  NUMBER(4)  NOT NULL,
    SkillID   NUMBER(4)  NOT NULL,
    CONSTRAINT PK_ALUMNI_SKILL PRIMARY KEY (AlumniID, SkillID),
    CONSTRAINT FK_ASKILL_ALUMNI FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID)
        ON DELETE CASCADE,
    CONSTRAINT FK_ASKILL_SKILL  FOREIGN KEY (SkillID)  REFERENCES SKILL(SkillID)
);

-- 14. ALUMNI_EVENT  (M:N alumni attends events)
CREATE TABLE ALUMNI_EVENT (
    AlumniID  NUMBER(8)  NOT NULL,
    EventID   NUMBER(6)  NOT NULL,
    CONSTRAINT PK_ALUMNI_EVENT PRIMARY KEY (AlumniID, EventID),
    CONSTRAINT FK_AEVENT_ALUMNI FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID)
        ON DELETE CASCADE,
    CONSTRAINT FK_AEVENT_EVENT  FOREIGN KEY (EventID)  REFERENCES EVENT(EventID)
);

-- Helpful indexes on foreign keys
CREATE INDEX IX_ALUMNI_DEPT    ON ALUMNI(DeptID);
CREATE INDEX IX_ALUMNI_BATCH   ON ALUMNI(BatchID);
CREATE INDEX IX_MNT_STUDENT    ON MENTORSHIP(StudentID);
CREATE INDEX IX_EVENT_ORG      ON EVENT(OrganizerID);
CREATE INDEX IX_DON_DONOR      ON DONATION(DonorID);
CREATE INDEX IX_JOB_POSTEDBY   ON JOB(PostedBy);
