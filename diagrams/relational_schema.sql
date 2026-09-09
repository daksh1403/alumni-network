-- ================================================================
-- RELATIONAL SCHEMA DDL STATEMENTS
-- Alumni Network and Engagement Platform
-- Fixed: All issues from review
-- ================================================================

-- ================================================================
-- 1. DEPARTMENT (Strong Entity)
-- ================================================================
CREATE TABLE DEPARTMENT (
    DeptID INT PRIMARY KEY,
    DeptName VARCHAR(100) NOT NULL UNIQUE,
    DeptCode VARCHAR(10) NOT NULL UNIQUE,
    HODName VARCHAR(100),
    EstablishedYear INT
);

-- ================================================================
-- 2. BATCH (Strong Entity)
-- ================================================================
CREATE TABLE BATCH (
    BatchID INT PRIMARY KEY,
    BatchYear INT NOT NULL,
    Section VARCHAR(5),
    TotalStudents INT,
    DeptID INT NOT NULL,
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
);

-- ================================================================
-- 3. COMPANY (Strong Entity)
-- ================================================================
CREATE TABLE COMPANY (
    CompanyID INT PRIMARY KEY,
    CompanyName VARCHAR(100) NOT NULL,
    Industry VARCHAR(50),
    CompanySize VARCHAR(20),
    Website VARCHAR(200),
    Headquarters VARCHAR(100)
);

-- ================================================================
-- 4. SKILL (Strong Entity)
-- ================================================================
CREATE TABLE SKILL (
    SkillID INT PRIMARY KEY,
    SkillName VARCHAR(50) NOT NULL UNIQUE,
    SkillCategory VARCHAR(50),
    Description TEXT
);

-- ================================================================
-- 5. ALUMNI (Strong Entity)
-- Phone removed - handled by ALUMNI_PHONE multivalued table
-- ================================================================
CREATE TABLE ALUMNI (
    AlumniID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    DateOfBirth DATE,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Address_City VARCHAR(50),
    Address_State VARCHAR(50),
    Address_PinCode VARCHAR(10),
    GraduationYear INT NOT NULL,
    DeptID INT NOT NULL,
    BatchID INT NOT NULL,
    CompanyID INT,
    CurrentPosition VARCHAR(100),
    LinkedInProfile VARCHAR(200),
    IsActive BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID),
    FOREIGN KEY (BatchID) REFERENCES BATCH(BatchID),
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
);

-- ================================================================
-- 6. STUDENT (Strong Entity)
-- Only attributes present in ER diagram
-- ================================================================
CREATE TABLE STUDENT (
    StudentID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    EnrollmentYear INT NOT NULL,
    DeptID INT NOT NULL,
    CurrentSemester INT,
    CGPA DECIMAL(4,2),
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
);

-- ================================================================
-- 7. EVENT (Strong Entity)
-- OrganizerID references ALUMNI(AlumniID)
-- ================================================================
CREATE TABLE EVENT (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(100) NOT NULL,
    EventType VARCHAR(50) CHECK (EventType IN ('Reunion', 'Workshop', 'Seminar', 'Networking')),
    EventDate DATE NOT NULL,
    Venue VARCHAR(200),
    OrganizerID INT NOT NULL,
    FOREIGN KEY (OrganizerID) REFERENCES ALUMNI(AlumniID)
);

-- ================================================================
-- 8. DONATION (Strong Entity)
-- DonorID references ALUMNI(AlumniID)
-- ================================================================
CREATE TABLE DONATION (
    DonationID INT PRIMARY KEY,
    DonorID INT NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    DonationDate DATE NOT NULL,
    PaymentMethod VARCHAR(30) CHECK (PaymentMethod IN ('Online', 'Check', 'DD', 'Cash')),
    FOREIGN KEY (DonorID) REFERENCES ALUMNI(AlumniID)
);

-- ================================================================
-- 9. JOB (Strong Entity)
-- PostedBy references ALUMNI(AlumniID)
-- CompanyID references COMPANY(CompanyID)
-- ================================================================
CREATE TABLE JOB (
    JobID INT PRIMARY KEY,
    JobTitle VARCHAR(100) NOT NULL,
    JobType VARCHAR(30) CHECK (JobType IN ('Full-Time', 'Part-Time', 'Contract', 'Internship')),
    Salary VARCHAR(50),
    CompanyID INT NOT NULL,
    PostedBy INT NOT NULL,
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID),
    FOREIGN KEY (PostedBy) REFERENCES ALUMNI(AlumniID)
);

-- ================================================================
-- 10. MENTORSHIP (Weak Entity)
-- Identifying relationship: ALUMNI mentors ALUMNI
-- MentorshipID is the primary key
-- ================================================================
CREATE TABLE MENTORSHIP (
    MentorshipID INT PRIMARY KEY,
    MentorID INT NOT NULL,
    MenteeID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Status VARCHAR(20) CHECK (Status IN ('Active', 'Completed', 'Paused', 'Cancelled')),
    MentorshipArea VARCHAR(100),
    Goals TEXT,
    FOREIGN KEY (MentorID) REFERENCES ALUMNI(AlumniID),
    FOREIGN KEY (MenteeID) REFERENCES ALUMNI(AlumniID)
);

-- ================================================================
-- 11. ALUMNI_SKILL (Junction Table for M:N ALUMNI ↔ SKILL)
-- Composite Primary Key: (AlumniID, SkillID)
-- ================================================================
CREATE TABLE ALUMNI_SKILL (
    AlumniID INT NOT NULL,
    SkillID INT NOT NULL,
    PRIMARY KEY (AlumniID, SkillID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID),
    FOREIGN KEY (SkillID) REFERENCES SKILL(SkillID)
);

-- ================================================================
-- 12. ALUMNI_PHONE (Multivalued Attribute)
-- Composite Primary Key: (AlumniID, PhoneNumber)
-- ================================================================
CREATE TABLE ALUMNI_PHONE (
    AlumniID INT NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    PRIMARY KEY (AlumniID, PhoneNumber),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID)
);

-- ================================================================
-- 13. ALUMNI_EVENT (Junction Table for M:N ALUMNI ↔ EVENT)
-- Composite Primary Key: (AlumniID, EventID)
-- ================================================================
CREATE TABLE ALUMNI_EVENT (
    AlumniID INT NOT NULL,
    EventID INT NOT NULL,
    RegistrationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (AlumniID, EventID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(AlumniID),
    FOREIGN KEY (EventID) REFERENCES EVENT(EventID)
);

-- ================================================================
-- INDEXES FOR PERFORMANCE
-- ================================================================
CREATE INDEX idx_alumni_dept ON ALUMNI(DeptID);
CREATE INDEX idx_alumni_batch ON ALUMNI(BatchID);
CREATE INDEX idx_alumni_company ON ALUMNI(CompanyID);
CREATE INDEX idx_student_dept ON STUDENT(DeptID);
CREATE INDEX idx_event_organizer ON EVENT(OrganizerID);
CREATE INDEX idx_donation_donor ON DONATION(DonorID);
CREATE INDEX idx_job_company ON JOB(CompanyID);
CREATE INDEX idx_job_postedby ON JOB(PostedBy);
CREATE INDEX idx_mentorship_mentor ON MENTORSHIP(MentorID);
CREATE INDEX idx_mentorship_mentee ON MENTORSHIP(MenteeID);
