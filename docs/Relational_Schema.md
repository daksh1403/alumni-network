# Relational Schema
## Alumni Network and Engagement Platform

## 1. Complete Relational Schema

### 1.1 DEPARTMENT
```
DEPARTMENT (
    DeptID          INT           PRIMARY KEY AUTO_INCREMENT,
    DeptName        VARCHAR(100)  NOT NULL UNIQUE,
    DeptCode        VARCHAR(10)   NOT NULL UNIQUE,
    HODPersonID     INT,
    EstablishedYear INT,

    FOREIGN KEY (HODPersonID) REFERENCES PERSON(PersonID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: DeptID
- Unique: DeptName, DeptCode
- Foreign Key: HODPersonID → PERSON(PersonID)
- Not Null: DeptID, DeptName, DeptCode

---

### 1.2 BATCH
```
BATCH (
    BatchID       INT          PRIMARY KEY AUTO_INCREMENT,
    BatchYear     INT          NOT NULL,
    DeptID        INT          NOT NULL,
    Section       VARCHAR(5),
    TotalStudents INT,
    
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: BatchID
- Foreign Key: DeptID → DEPARTMENT(DeptID)
- Not Null: BatchID, BatchYear, DeptID

---

### 1.3 COMPANY
```
COMPANY (
    CompanyID     INT           PRIMARY KEY AUTO_INCREMENT,
    CompanyName   VARCHAR(100)  NOT NULL,
    Industry      VARCHAR(50),
    SizeID        INT,
    Website       VARCHAR(200),
    Headquarters  VARCHAR(100),
    FoundedYear   INT,

    FOREIGN KEY (SizeID) REFERENCES COMPANY_SIZE(SizeID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: CompanyID
- Foreign Key: SizeID → COMPANY_SIZE(SizeID)
- Not Null: CompanyID, CompanyName

---

### 1.3.1 COMPANY_SIZE (Lookup Table)
```
COMPANY_SIZE (
    SizeID    INT          PRIMARY KEY AUTO_INCREMENT,
    SizeRange VARCHAR(30)  NOT NULL UNIQUE
);
```

---

### 1.4 SKILL
```
SKILL (
    SkillID       INT          PRIMARY KEY AUTO_INCREMENT,
    SkillName     VARCHAR(50)  NOT NULL UNIQUE,
    SkillCategory VARCHAR(50),
    Description   TEXT
);
```

**Constraints:**
- Primary Key: SkillID
- Unique: SkillName
- Not Null: SkillID, SkillName

---

### 1.5 PERSON (Supertype)
```
PERSON (
    PersonID       INT           PRIMARY KEY AUTO_INCREMENT,
    FirstName      VARCHAR(50)   NOT NULL,
    LastName       VARCHAR(50)   NOT NULL,
    Email          VARCHAR(100)  NOT NULL UNIQUE,
    Phone          VARCHAR(15),
    DateOfBirth    DATE,
    Gender         CHAR(1)       CHECK (Gender IN ('M', 'F', 'O')),
    Address        VARCHAR(200),
    ProfilePicture VARCHAR(255),
    CreatedAt      DATETIME      DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints:**
- Primary Key: PersonID
- Unique: Email
- Check: Gender IN ('M', 'F', 'O')
- Not Null: PersonID, FirstName, LastName, Email

---

### 1.6 ALUMNI (Subtype of PERSON)
```
ALUMNI (
    PersonID          INT          PRIMARY KEY,
    GraduationYear    INT          NOT NULL,
    DeptID            INT          NOT NULL,
    BatchID           INT          NOT NULL,
    CurrentCompanyID  INT,
    CurrentPosition   VARCHAR(100),
    LinkedInProfile   VARCHAR(200),
    IsActive          BOOLEAN      DEFAULT TRUE,
    
    FOREIGN KEY (PersonID) REFERENCES PERSON(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (BatchID) REFERENCES BATCH(BatchID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (CurrentCompanyID) REFERENCES COMPANY(CompanyID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: PersonID
- Foreign Keys: PersonID → PERSON, DeptID → DEPARTMENT, BatchID → BATCH, CurrentCompanyID → COMPANY
- Not Null: PersonID, GraduationYear, DeptID, BatchID

---

### 1.7 STUDENT (Subtype of PERSON)
```
STUDENT (
    PersonID         INT           PRIMARY KEY,
    StudentID        VARCHAR(20)   NOT NULL UNIQUE,
    EnrollmentYear   INT           NOT NULL,
    DeptID           INT           NOT NULL,
    CurrentSemester  INT,
    CGPA             DECIMAL(4,2),
    
    FOREIGN KEY (PersonID) REFERENCES PERSON(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (DeptID) REFERENCES DEPARTMENT(DeptID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: PersonID
- Unique: StudentID
- Foreign Keys: PersonID → PERSON, DeptID → DEPARTMENT
- Not Null: PersonID, StudentID, EnrollmentYear, DeptID

---

### 1.8 ADMIN (Subtype of PERSON)
```
ADMIN (
    PersonID     INT          PRIMARY KEY,
    AdminRole    VARCHAR(50)  NOT NULL,
    Department   VARCHAR(100),
    AccessLevel  INT          CHECK (AccessLevel BETWEEN 1 AND 5),
    
    FOREIGN KEY (PersonID) REFERENCES PERSON(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: PersonID
- Foreign Key: PersonID → PERSON
- Check: AccessLevel BETWEEN 1 AND 5
- Not Null: PersonID, AdminRole

---

### 1.9 EVENT
```
EVENT (
    EventID         INT           PRIMARY KEY AUTO_INCREMENT,
    EventName       VARCHAR(100)  NOT NULL,
    EventTypeID     INT           NOT NULL,
    Description     TEXT,
    EventDate       DATE          NOT NULL,
    EventTime       TIME,
    Venue           VARCHAR(200),
    MaxCapacity     INT,
    RegistrationFee DECIMAL(10,2) DEFAULT 0.00,
    OrganizerID     INT           NOT NULL,
    CreatedDate     DATETIME      DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (EventTypeID) REFERENCES EVENT_TYPE(TypeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (OrganizerID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: EventID
- Foreign Keys: EventTypeID → EVENT_TYPE(TypeID), OrganizerID → ALUMNI(PersonID)
- Not Null: EventID, EventName, EventDate, OrganizerID, EventTypeID

---

### 1.9.1 EVENT_TYPE (Lookup Table)
```
EVENT_TYPE (
    TypeID   INT          PRIMARY KEY AUTO_INCREMENT,
    TypeName VARCHAR(50)  NOT NULL UNIQUE
);
```

---

### 1.10 DONATION
```
DONATION (
    DonationID     INT            PRIMARY KEY AUTO_INCREMENT,
    DonorID        INT            NOT NULL,
    Amount         DECIMAL(12,2)  NOT NULL,
    DonationDate   DATE           NOT NULL,
    PaymentMethod  VARCHAR(30)    CHECK (PaymentMethod IN ('Online', 'Check', 'DD', 'Cash')),
    Purpose        VARCHAR(100),
    TransactionID  VARCHAR(50)    UNIQUE,
    IsAnonymous    BOOLEAN        DEFAULT FALSE,
    ReceiptNumber  VARCHAR(50)    UNIQUE,
    
    FOREIGN KEY (DonorID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: DonationID
- Unique: TransactionID, ReceiptNumber
- Foreign Key: DonorID → ALUMNI(PersonID)
- Check: PaymentMethod IN ('Online', 'Check', 'DD', 'Cash')
- Not Null: DonationID, DonorID, Amount, DonationDate

---

### 1.11 JOB
```
JOB (
    JobID        INT           PRIMARY KEY AUTO_INCREMENT,
    JobTitle     VARCHAR(100)  NOT NULL,
    CompanyID    INT           NOT NULL,
    PostedBy     INT           NOT NULL,
    JobType      VARCHAR(30)   CHECK (JobType IN ('Full-Time', 'Part-Time', 'Contract', 'Internship')),
    Location     VARCHAR(100),
    Salary       VARCHAR(50),
    Description  TEXT,
    Requirements TEXT,
    PostedDate   DATETIME      DEFAULT CURRENT_TIMESTAMP,
    ExpiryDate   DATE,
    IsActive     BOOLEAN       DEFAULT TRUE,
    
    FOREIGN KEY (CompanyID) REFERENCES COMPANY(CompanyID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (PostedBy) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: JobID
- Foreign Keys: CompanyID → COMPANY, PostedBy → ALUMNI(PersonID)
- Check: JobType IN ('Full-Time', 'Part-Time', 'Contract', 'Internship')
- Not Null: JobID, JobTitle, CompanyID, PostedBy

---

### 1.12 MENTORSHIP
```
MENTORSHIP (
    MentorshipID    INT          PRIMARY KEY AUTO_INCREMENT,
    MentorID        INT          NOT NULL,
    MenteeID        INT          NOT NULL,
    StartDate       DATE         NOT NULL,
    EndDate         DATE,
    Status          VARCHAR(20)  CHECK (Status IN ('Active', 'Completed', 'Paused', 'Cancelled')),
    AreaID          INT,
    Goals           TEXT,
    Feedback        TEXT,
    Rating          INT          CHECK (Rating BETWEEN 1 AND 5),

    FOREIGN KEY (MentorID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (MenteeID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (AreaID) REFERENCES MENTORSHIP_AREA(AreaID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    UNIQUE (MentorID, MenteeID, StartDate)
);
```

**Constraints:**
- Primary Key: MentorshipID
- Unique: (MentorID, MenteeID, StartDate)
- Foreign Keys: MentorID → ALUMNI, MenteeID → ALUMNI, AreaID → MENTORSHIP_AREA
- Check: Status IN ('Active', 'Completed', 'Paused', 'Cancelled'), Rating BETWEEN 1 AND 5
- Not Null: MentorshipID, MentorID, MenteeID, StartDate

---

### 1.12.1 MENTORSHIP_AREA (Lookup Table)
```
MENTORSHIP_AREA (
    AreaID   INT           PRIMARY KEY AUTO_INCREMENT,
    AreaName VARCHAR(100)  NOT NULL UNIQUE
);
```

---

### 1.13 FORUM
```
FORUM (
    ForumID     INT           PRIMARY KEY AUTO_INCREMENT,
    ForumName   VARCHAR(100)  NOT NULL,
    Description TEXT,
    Category    VARCHAR(50),
    CreatedBy   INT           NOT NULL,
    CreatedDate DATETIME      DEFAULT CURRENT_TIMESTAMP,
    IsActive    BOOLEAN       DEFAULT TRUE,
    
    FOREIGN KEY (CreatedBy) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: ForumID
- Foreign Key: CreatedBy → ALUMNI(PersonID)
- Not Null: ForumID, ForumName, CreatedBy

---

### 1.14 POST
```
POST (
    PostID      INT           PRIMARY KEY AUTO_INCREMENT,
    ForumID     INT           NOT NULL,
    AuthorID    INT           NOT NULL,
    Title       VARCHAR(200)  NOT NULL,
    Content     TEXT          NOT NULL,
    PostedDate  DATETIME      DEFAULT CURRENT_TIMESTAMP,
    LikesCount  INT           DEFAULT 0,
    IsPinned    BOOLEAN       DEFAULT FALSE,
    
    FOREIGN KEY (ForumID) REFERENCES FORUM(ForumID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (AuthorID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: PostID
- Foreign Keys: ForumID → FORUM, AuthorID → ALUMNI(PersonID)
- Not Null: PostID, ForumID, AuthorID, Title, Content

---

### 1.15 COMMENT
```
COMMENT (
    CommentID       INT       PRIMARY KEY AUTO_INCREMENT,
    PostID          INT       NOT NULL,
    AuthorID        INT       NOT NULL,
    Content         TEXT      NOT NULL,
    CommentDate     DATETIME  DEFAULT CURRENT_TIMESTAMP,
    ParentCommentID INT,
    
    FOREIGN KEY (PostID) REFERENCES POST(PostID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (AuthorID) REFERENCES ALUMNI(PersonID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (ParentCommentID) REFERENCES COMMENT(CommentID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Constraints:**
- Primary Key: CommentID
- Foreign Keys: PostID → POST, AuthorID → ALUMNI, ParentCommentID → COMMENT (self-reference)
- Not Null: CommentID, PostID, AuthorID, Content

---

### 1.16 ALUMNI_SKILL (Junction Table)
```
ALUMNI_SKILL (
    AlumniID        INT          NOT NULL,
    SkillID         INT          NOT NULL,
    ProficiencyLevel VARCHAR(20) CHECK (ProficiencyLevel IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    
    PRIMARY KEY (AlumniID, SkillID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (SkillID) REFERENCES SKILL(SkillID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

**Constraints:**
- Composite Primary Key: (AlumniID, SkillID)
- Foreign Keys: AlumniID → ALUMNI, SkillID → SKILL
- Check: ProficiencyLevel IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')

---

### 1.17 EVENT_REGISTRATION (Junction Table)
```
EVENT_REGISTRATION (
    AlumniID          INT      NOT NULL,
    EventID           INT      NOT NULL,
    RegistrationDate  DATETIME DEFAULT CURRENT_TIMESTAMP,
    AttendanceStatus  VARCHAR(20) CHECK (AttendanceStatus IN ('Registered', 'Attended', 'Cancelled', 'No Show')),

    PRIMARY KEY (AlumniID, EventID),
    FOREIGN KEY (AlumniID) REFERENCES ALUMNI(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (EventID) REFERENCES EVENT(EventID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

**Constraints:**
- Composite Primary Key: (AlumniID, EventID)
- Foreign Keys: AlumniID → ALUMNI, EventID → EVENT
- Check: AttendanceStatus IN ('Registered', 'Attended', 'Cancelled', 'No Show')

---

### 1.18 JOB_APPLICATION (Junction Table)
```
JOB_APPLICATION (
    ApplicationID   INT          PRIMARY KEY AUTO_INCREMENT,
    JobID           INT          NOT NULL,
    ApplicantID     INT          NOT NULL,
    ApplicationDate DATETIME     DEFAULT CURRENT_TIMESTAMP,
    Status          VARCHAR(20)  CHECK (Status IN ('Applied', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted')),
    ResumeLink      VARCHAR(255),

    FOREIGN KEY (JobID) REFERENCES JOB(JobID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (ApplicantID) REFERENCES ALUMNI(PersonID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    UNIQUE (JobID, ApplicantID)
);
```

**Constraints:**
- Primary Key: ApplicationID
- Unique: (JobID, ApplicantID)
- Foreign Keys: JobID → JOB, ApplicantID → ALUMNI(PersonID)
- Check: Status IN ('Applied', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted')

---

## 2. Entity-Relationship Diagram (Textual)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ALUMNI NETWORK - RELATIONAL SCHEMA                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  DEPARTMENT  │     │    BATCH     │     │   COMPANY    │
│──────────────│     │──────────────│     │──────────────│
│ DeptID (PK)  │◄────│ BatchID (PK) │     │CompanyID(PK) │
│ DeptName     │     │ BatchYear    │     │CompanyName   │
│ DeptCode     │     │ DeptID (FK)──┼────►│Industry      │
│ HODName      │     │ Section      │     │Website       │
│ EstablishedYr│     │ TotalStudents│     │Headquarters  │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │
       │                    │                     │
       └────────────────────┼─────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   PERSON     │
                    │──────────────│
                    │ PersonID(PK) │
                    │ FirstName    │
                    │ LastName     │
                    │ Email        │
                    │ Phone        │
                    │ DOB          │
                    │ Gender       │
                    └──────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │    ALUMNI    │ │   STUDENT    │ │    ADMIN     │
     │──────────────│ │──────────────│ │──────────────│
     │PersonID (PK) │ │PersonID (PK) │ │PersonID (PK) │
     │GraduationYear│ │StudentID     │ │AdminRole     │
     │DeptID (FK)───┤ │EnrollmentYear│ │Department    │
     │BatchID (FK)──┤ │DeptID (FK)   │ │AccessLevel   │
     │CompanyID(FK)─┤ │Semester      │ └──────────────┘
     │Position      │ │CGPA          │
     │LinkedIn      │ └──────────────┘
     └──────┬───────┘
            │
    ┌───────┼───────┬───────┬───────┬───────┬───────┐
    │       │       │       │       │       │       │
    ▼       ▼       ▼       ▼       ▼       ▼       ▼
┌───────┐┌───────┐┌───────┐┌───────┐┌───────┐┌───────┐
│EVENT  ││DONAT- ││  JOB  ││MENTOR-││ FORUM ││ALUMNI │
│───────││ ION   ││───────││ SHIP  ││───────││_SKILL │
│EventID││───────││JobID  ││───────││ForumID││───────│
│Name   ││DonID  ││Title  ││MentID ││Name   ││AlumID │
│Type   ││Amount ││CompID ││Mentee ││Desc   ││SkillID│
│Date   ││Date   ││PostBy ││Start  ││Categ  ││Prof.  │
│Venue  ││Method ││Type   ││End    ││Create │└───────┘
│OrgID──┤│Purpose││Salary ││Status ││By─────┤
└───────┘│TxnID  ││Desc   ││Area   │└───────┘
         │Anon   ││Req    ││Goals  │
         │Receipt││Expiry ││Rating │
         └───────┘└───────┘└───────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │   POST    │
                              │───────────│
                              │ PostID    │
                              │ ForumID   │
                              │ AuthorID  │
                              │ Title     │
                              │ Content   │
                              └───────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │  COMMENT  │
                              │───────────│
                              │ CommentID │
                              │ PostID    │
                              │ AuthorID  │
                              │ Content   │
                              │ ParentID  │
                              └───────────┘
```

---

## 3. Referential Integrity Constraints

| Table | Foreign Key | References | On Delete | On Update |
|-------|-------------|------------|-----------|-----------|
| BATCH | DeptID | DEPARTMENT(DeptID) | RESTRICT | CASCADE |
| ALUMNI | PersonID | PERSON(PersonID) | CASCADE | CASCADE |
| ALUMNI | DeptID | DEPARTMENT(DeptID) | RESTRICT | CASCADE |
| ALUMNI | BatchID | BATCH(BatchID) | RESTRICT | CASCADE |
| ALUMNI | CurrentCompanyID | COMPANY(CompanyID) | SET NULL | CASCADE |
| STUDENT | PersonID | PERSON(PersonID) | CASCADE | CASCADE |
| STUDENT | DeptID | DEPARTMENT(DeptID) | RESTRICT | CASCADE |
| ADMIN | PersonID | PERSON(PersonID) | CASCADE | CASCADE |
| COMPANY | SizeID | COMPANY_SIZE(SizeID) | SET NULL | CASCADE |
| EVENT | EventTypeID | EVENT_TYPE(TypeID) | RESTRICT | CASCADE |
| EVENT | OrganizerID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| DONATION | DonorID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| JOB | CompanyID | COMPANY(CompanyID) | RESTRICT | CASCADE |
| JOB | PostedBy | ALUMNI(PersonID) | RESTRICT | CASCADE |
| MENTORSHIP | MentorID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| MENTORSHIP | MenteeID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| MENTORSHIP | AreaID | MENTORSHIP_AREA(AreaID) | SET NULL | CASCADE |
| FORUM | CreatedBy | ALUMNI(PersonID) | RESTRICT | CASCADE |
| POST | ForumID | FORUM(ForumID) | CASCADE | CASCADE |
| POST | AuthorID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| COMMENT | PostID | POST(PostID) | CASCADE | CASCADE |
| COMMENT | AuthorID | ALUMNI(PersonID) | RESTRICT | CASCADE |
| COMMENT | ParentCommentID | COMMENT(CommentID) | SET NULL | CASCADE |
| ALUMNI_SKILL | AlumniID | ALUMNI(PersonID) | CASCADE | CASCADE |
| ALUMNI_SKILL | SkillID | SKILL(SkillID) | CASCADE | CASCADE |
| EVENT_REGISTRATION | AlumniID | ALUMNI(PersonID) | CASCADE | CASCADE |
| EVENT_REGISTRATION | EventID | EVENT(EventID) | CASCADE | CASCADE |
| JOB_APPLICATION | JobID | JOB(JobID) | CASCADE | CASCADE |
| JOB_APPLICATION | ApplicantID | ALUMNI(PersonID) | CASCADE | CASCADE |
| DEPARTMENT | HODPersonID | PERSON(PersonID) | SET NULL | CASCADE |

---

## 4. Indexes

### Primary Key Indexes (Automatic)
- All tables have clustered index on Primary Key

### Recommended Indexes
```sql
-- For frequent queries
CREATE INDEX idx_alumni_email ON ALUMNI(PersonID);
CREATE INDEX idx_alumni_dept ON ALUMNI(DeptID);
CREATE INDEX idx_alumni_batch ON ALUMNI(BatchID);
CREATE INDEX idx_alumni_company ON ALUMNI(CurrentCompanyID);
CREATE INDEX idx_event_date ON EVENT(EventDate);
CREATE INDEX idx_job_company ON JOB(CompanyID);
CREATE INDEX idx_job_postedby ON JOB(PostedBy);
CREATE INDEX idx_donation_donor ON DONATION(DonorID);
CREATE INDEX idx_donation_date ON DONATION(DonationDate);
CREATE INDEX idx_mentorship_mentor ON MENTORSHIP(MentorID);
CREATE INDEX idx_mentorship_mentee ON MENTORSHIP(MenteeID);
CREATE INDEX idx_post_forum ON POST(ForumID);
CREATE INDEX idx_post_author ON POST(AuthorID);
CREATE INDEX idx_comment_post ON COMMENT(PostID);
```

---

## 5. Views

### 5.1 Alumni Profile View
```sql
CREATE VIEW AlumniProfileView AS
SELECT 
    a.PersonID,
    p.FirstName,
    p.LastName,
    p.Email,
    a.GraduationYear,
    d.DeptName,
    c.CompanyName,
    a.CurrentPosition
FROM ALUMNI a
JOIN PERSON p ON a.PersonID = p.PersonID
JOIN DEPARTMENT d ON a.DeptID = d.DeptID
LEFT JOIN COMPANY c ON a.CurrentCompanyID = c.CompanyID
WHERE a.IsActive = TRUE;
```

### 5.2 Event Summary View
```sql
CREATE VIEW EventSummaryView AS
SELECT 
    e.EventID,
    e.EventName,
    e.EventType,
    e.EventDate,
    e.Venue,
    COUNT(er.AlumniID) AS TotalRegistrations,
    p.FirstName AS OrganizerFirstName,
    p.LastName AS OrganizerLastName
FROM EVENT e
LEFT JOIN EVENT_REGISTRATION er ON e.EventID = er.EventID
JOIN ALUMNI a ON e.OrganizerID = a.PersonID
JOIN PERSON p ON a.PersonID = p.PersonID
GROUP BY e.EventID;
```

### 5.3 Donation Summary View
```sql
CREATE VIEW DonationSummaryView AS
SELECT 
    a.PersonID,
    p.FirstName,
    p.LastName,
    COUNT(d.DonationID) AS TotalDonations,
    SUM(d.Amount) AS TotalAmount,
    MAX(d.DonationDate) AS LastDonationDate
FROM ALUMNI a
JOIN PERSON p ON a.PersonID = p.PersonID
LEFT JOIN DONATION d ON a.PersonID = d.DonorID
GROUP BY a.PersonID;
```

---

## 6. Sample Data

### DEPARTMENT
| DeptID | DeptName | DeptCode | HODPersonID | EstablishedYear |
|--------|----------|----------|-------------|-----------------|
| 1 | Computer Science | CS | 1 | 1995 |
| 2 | Electronics | EC | 2 | 1998 |
| 3 | Mechanical | ME | 3 | 1990 |

### COMPANY_SIZE
| SizeID | SizeRange |
|--------|-----------|
| 1 | 1-10 |
| 2 | 11-50 |
| 3 | 51-200 |
| 4 | 201-1000 |
| 5 | 1001-10000 |
| 6 | 10001-50000 |
| 7 | 50001-100000 |
| 8 | 100000+ |

### COMPANY
| CompanyID | CompanyName | Industry | SizeID | Headquarters |
|-----------|-------------|----------|--------|--------------|
| 1 | Google | Technology | 8 | Mountain View |
| 2 | Microsoft | Technology | 8 | Redmond |
| 3 | Amazon | E-commerce | 8 | Seattle |

### EVENT_TYPE
| TypeID | TypeName |
|--------|----------|
| 1 | Reunion |
| 2 | Workshop |
| 3 | Seminar |
| 4 | Networking |

### MENTORSHIP_AREA
| AreaID | AreaName |
|--------|----------|
| 1 | Data Science |
| 2 | Web Development |
| 3 | Career Guidance |
| 4 | Research |
| 5 | Entrepreneurship |

### SKILL
| SkillID | SkillName | SkillCategory | Description |
|---------|-----------|---------------|-------------|
| 1 | Python | Programming | General-purpose programming |
| 2 | Java | Programming | Object-oriented programming |
| 3 | SQL | Database | Structured Query Language |
| 4 | Machine Learning | AI/ML | Statistical learning algorithms |

---

This relational schema provides a complete, normalized structure for the Alumni Network and Engagement Platform database.
