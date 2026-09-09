# Entity-Relationship Model
## Alumni Network and Engagement Platform

## 1. Entities and Their Attributes

### 1.1 ALUMNI (Strong Entity)
**Primary Key:** AlumniID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| AlumniID | INT | PK, NOT NULL |
| FirstName | VARCHAR(50) | NOT NULL |
| LastName | VARCHAR(50) | NOT NULL |
| Email | VARCHAR(100) | UNIQUE, NOT NULL |
| Phone | VARCHAR(15) | |
| DateOfBirth | DATE | |
| Gender | CHAR(1) | CHECK (M/F/O) |
| GraduationYear | INT | NOT NULL |
| CurrentCity | VARCHAR(50) | |
| CurrentState | VARCHAR(50) | |
| CurrentCountry | VARCHAR(50) | |
| LinkedInProfile | VARCHAR(200) | |
| ProfilePicture | VARCHAR(255) | |
| RegistrationDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| IsActive | BOOLEAN | DEFAULT TRUE |

---

### 1.2 DEPARTMENT (Strong Entity)
**Primary Key:** DeptID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| DeptID | INT | PK, NOT NULL |
| DeptName | VARCHAR(100) | NOT NULL, UNIQUE |
| DeptCode | VARCHAR(10) | NOT NULL, UNIQUE |
| HODName | VARCHAR(100) | |
| EstablishedYear | INT | |

---

### 1.3 BATCH (Strong Entity)
**Primary Key:** BatchID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| BatchID | INT | PK, NOT NULL |
| BatchYear | INT | NOT NULL |
| DeptID | INT | FK (REFERENCES DEPARTMENT) |
| Section | VARCHAR(5) | |
| TotalStudents | INT | |

---

### 1.4 COMPANY (Strong Entity)
**Primary Key:** CompanyID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| CompanyID | INT | PK, NOT NULL |
| CompanyName | VARCHAR(100) | NOT NULL |
| Industry | VARCHAR(50) | |
| CompanySize | VARCHAR(20) | |
| Website | VARCHAR(200) | |
| Headquarters | VARCHAR(100) | |
| FoundedYear | INT | |

---

### 1.5 SKILL (Strong Entity)
**Primary Key:** SkillID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| SkillID | INT | PK, NOT NULL |
| SkillName | VARCHAR(50) | NOT NULL, UNIQUE |
| SkillCategory | VARCHAR(50) | |
| Description | TEXT | |

---

### 1.6 EVENT (Strong Entity)
**Primary Key:** EventID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| EventID | INT | PK, NOT NULL |
| EventName | VARCHAR(100) | NOT NULL |
| EventType | VARCHAR(50) | CHECK (Reunion/Workshop/Seminar/Networking) |
| Description | TEXT | |
| EventDate | DATE | NOT NULL |
| EventTime | TIME | |
| Venue | VARCHAR(200) | |
| MaxCapacity | INT | |
| RegistrationFee | DECIMAL(10,2) | DEFAULT 0.00 |
| OrganizerID | INT | FK (REFERENCES ALUMNI) |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |

---

### 1.7 DONATION (Strong Entity)
**Primary Key:** DonationID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| DonationID | INT | PK, NOT NULL |
| DonorID | INT | FK (REFERENCES ALUMNI) |
| Amount | DECIMAL(12,2) | NOT NULL |
| DonationDate | DATE | NOT NULL |
| PaymentMethod | VARCHAR(30) | CHECK (Online/Check/DD/Cash) |
| Purpose | VARCHAR(100) | |
| TransactionID | VARCHAR(50) | UNIQUE |
| IsAnonymous | BOOLEAN | DEFAULT FALSE |
| ReceiptNumber | VARCHAR(50) | UNIQUE |

---

### 1.8 JOB (Strong Entity)
**Primary Key:** JobID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| JobID | INT | PK, NOT NULL |
| JobTitle | VARCHAR(100) | NOT NULL |
| CompanyID | INT | FK (REFERENCES COMPANY) |
| PostedBy | INT | FK (REFERENCES ALUMNI) |
| JobType | VARCHAR(30) | CHECK (Full-Time/Part-Time/Contract/Internship) |
| Location | VARCHAR(100) | |
| Salary | VARCHAR(50) | |
| Description | TEXT | |
| Requirements | TEXT | |
| PostedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| ExpiryDate | DATE | |
| IsActive | BOOLEAN | DEFAULT TRUE |

---

### 1.9 MENTORSHIP (Weak Entity)
**Primary Key:** MentorshipID (Composite: MentorID + MenteeID + StartDate)

| Attribute | Type | Constraints |
|-----------|------|-------------|
| MentorshipID | INT | PK, NOT NULL |
| MentorID | INT | FK (REFERENCES ALUMNI) |
| MenteeID | INT | FK (REFERENCES ALUMNI) |
| StartDate | DATE | NOT NULL |
| EndDate | DATE | |
| Status | VARCHAR(20) | CHECK (Active/Completed/Paused/Cancelled) |
| MentorshipArea | VARCHAR(100) | |
| Goals | TEXT | |
| Feedback | TEXT | |
| Rating | INT | CHECK (1-5) |

---

### 1.10 FORUM (Strong Entity)
**Primary Key:** ForumID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| ForumID | INT | PK, NOT NULL |
| ForumName | VARCHAR(100) | NOT NULL |
| Description | TEXT | |
| Category | VARCHAR(50) | |
| CreatedBy | INT | FK (REFERENCES ALUMNI) |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| IsActive | BOOLEAN | DEFAULT TRUE |

---

### 1.11 POST (Strong Entity)
**Primary Key:** PostID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| PostID | INT | PK, NOT NULL |
| ForumID | INT | FK (REFERENCES FORUM) |
| AuthorID | INT | FK (REFERENCES ALUMNI) |
| Title | VARCHAR(200) | NOT NULL |
| Content | TEXT | NOT NULL |
| PostedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| LikesCount | INT | DEFAULT 0 |
| IsPinned | BOOLEAN | DEFAULT FALSE |

---

### 1.12 COMMENT (Strong Entity)
**Primary Key:** CommentID

| Attribute | Type | Constraints |
|-----------|------|-------------|
| CommentID | INT | PK, NOT NULL |
| PostID | INT | FK (REFERENCES POST) |
| AuthorID | INT | FK (REFERENCES ALUMNI) |
| Content | TEXT | NOT NULL |
| CommentDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| ParentCommentID | INT | FK (SELF-REFERENCE) |

---

## 2. Relationships

### 2.1 ALUMNI - DEPARTMENT (Many-to-One)
- An alumnus belongs to ONE department
- A department has MANY alumni
- **Foreign Key:** DeptID in ALUMNI

### 2.2 ALUMNI - BATCH (Many-to-One)
- An alumnus belongs to ONE batch
- A batch has MANY alumni
- **Foreign Key:** BatchID in ALUMNI

### 2.3 ALUMNI - COMPANY (Many-to-One)
- An alumnus works at ONE company (current)
- A company employs MANY alumni
- **Foreign Key:** CompanyID in ALUMNI

### 2.4 ALUMNI - SKILL (Many-to-Many)
- An alumnus has MANY skills
- A skill is possessed by MANY alumni
- **Junction Table:** ALUMNI_SKILL (AlumniID, SkillID, ProficiencyLevel)

### 2.5 ALUMNI - EVENT (Many-to-Many)
- An alumnus can attend MANY events
- An event can have MANY alumni attendees
- **Junction Table:** EVENT_REGISTRATION (AlumniID, EventID, RegistrationDate, AttendanceStatus)

### 2.6 ALUMNI - EVENT (One-to-Many) [Organizer]
- An alumnus can organize MANY events
- An event is organized by ONE alumnus
- **Foreign Key:** OrganizerID in EVENT

### 2.7 ALUMNI - DONATION (One-to-Many)
- An alumnus can make MANY donations
- A donation is made by ONE alumnus
- **Foreign Key:** DonorID in DONATION

### 2.8 ALUMNI - JOB (One-to-Many) [Posted By]
- An alumnus can post MANY jobs
- A job is posted by ONE alumnus
- **Foreign Key:** PostedBy in JOB

### 2.9 COMPANY - JOB (One-to-Many)
- A company has MANY job postings
- A job belongs to ONE company
- **Foreign Key:** CompanyID in JOB

### 2.10 ALUMNI - MENTORSHIP (One-to-Many) [As Mentor]
- An alumnus can mentor MANY mentees
- A mentorship has ONE mentor
- **Foreign Key:** MentorID in MENTORSHIP

### 2.11 ALUMNI - MENTORSHIP (One-to-Many) [As Mentee]
- An alumnus can have ONE mentor (in a specific mentorship)
- A mentorship has ONE mentee
- **Foreign Key:** MenteeID in MENTORSHIP

### 2.12 ALUMNI - FORUM (One-to-Many)
- An alumnus can create MANY forums
- A forum is created by ONE alumnus
- **Foreign Key:** CreatedBy in FORUM

### 2.13 FORUM - POST (One-to-Many)
- A forum has MANY posts
- A post belongs to ONE forum
- **Foreign Key:** ForumID in POST

### 2.14 ALUMNI - POST (One-to-Many)
- An alumnus can create MANY posts
- A post is created by ONE alumnus
- **Foreign Key:** AuthorID in POST

### 2.15 POST - COMMENT (One-to-Many)
- A post has MANY comments
- A comment belongs to ONE post
- **Foreign Key:** PostID in COMMENT

### 2.16 ALUMNI - COMMENT (One-to-Many)
- An alumnus can write MANY comments
- A comment is written by ONE alumnus
- **Foreign Key:** AuthorID in COMMENT

### 2.17 COMMENT - COMMENT (Self-Referencing)
- A comment can have MANY replies
- A reply belongs to ONE parent comment
- **Foreign Key:** ParentCommentID in COMMENT (self-reference)

---

## 3. Cardinality Constraints

| Relationship | Cardinality | Participation |
|--------------|-------------|---------------|
| ALUMNI - DEPARTMENT | N:1 | Total (Alumni), Partial (Department) |
| ALUMNI - BATCH | N:1 | Total (Alumni), Partial (Batch) |
| ALUMNI - COMPANY | N:1 | Partial (Both) |
| ALUMNI - SKILL | M:N | Partial (Both) |
| ALUMNI - EVENT (Attend) | M:N | Partial (Both) |
| ALUMNI - EVENT (Organize) | 1:N | Partial (Both) |
| ALUMNI - DONATION | 1:N | Partial (Both) |
| ALUMNI - JOB (Post) | 1:N | Partial (Both) |
| COMPANY - JOB | 1:N | Partial (Both) |
| ALUMNI - MENTORSHIP | 1:N | Partial (Both) |
| ALUMNI - FORUM | 1:N | Partial (Both) |
| FORUM - POST | 1:N | Partial (Both) |
| POST - COMMENT | 1:N | Partial (Both) |

---

## 4. ER Diagram (Textual Representation)

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  DEPARTMENT │       │    BATCH    │       │   COMPANY   │
└──────┬──────┘       └──────┬──────┘       └──────┬──────┘
       │                     │                     │
       │ 1                   │ 1                   │ 1
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│                         ALUMNI                               │
│  (AlumniID, FirstName, LastName, Email, Phone, DOB, Gender, │
│   GraduationYear, City, State, Country, LinkedIn, etc.)      │
└──────────────────────────────────────────────────────────────┘
       │           │           │           │           │
       │ 1         │ M         │ M         │ 1         │ M
       │           │           │           │           │
       ▼           ▼           ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  DONATION│ │   EVENT  │ │   JOB    │ │ MENTORSHIP│ │  FORUM   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
                     │                               │
                     │ M                             │ 1
                     │                               │
                     ▼                               ▼
              ┌──────────┐                    ┌──────────┐
              │EVENT_REG │                    │   POST   │
              └──────────┘                    └──────────┘
                                                    │
                                                    │ 1
                                                    │
                                                    ▼
                                             ┌──────────┐
                                             │  COMMENT │
                                             └──────────┘
```

---

## 5. Key Constraints Summary

### Primary Keys
- All entities have a single-attribute primary key (surrogate key)
- Primary keys are auto-incremented integers

### Foreign Keys
- All relationships are enforced through foreign keys
- Cascade delete/update where appropriate
- Set NULL for optional relationships

### Unique Constraints
- Email in ALUMNI
- TransactionID in DONATION
- ReceiptNumber in DONATION
- DeptName, DeptCode in DEPARTMENT
- SkillName in SKILL

### Check Constraints
- Gender: M, F, O
- EventType: Reunion, Workshop, Seminar, Networking
- PaymentMethod: Online, Check, DD, Cash
- JobType: Full-Time, Part-Time, Contract, Internship
- Status in MENTORSHIP: Active, Completed, Paused, Cancelled
- Rating: 1-5

### Not Null Constraints
- All primary key attributes
- Essential attributes like names, emails, dates
- Foreign keys in total participation relationships

---

## 6. Weak Entities

### MENTORSHIP
- **Identifying Relationship:** Mentor and Mentee are identified through their relationship
- **Partial Key:** StartDate (combined with MentorID and MenteeID)
- **Owner Entity:** ALUMNI (both Mentor and Mentee)

---

## 7. Multi-valued Attributes

None in this design. All multi-valued data is normalized into separate tables (e.g., SKILL is a separate entity with M:N relationship).

---

## 8. Composite Attributes

- **Name:** FirstName, LastName (stored as separate attributes)
- **Address:** CurrentCity, CurrentState, CurrentCountry (stored as separate attributes)

---

## 9. Derived Attributes

- **FullName:** Can be derived from FirstName + LastName
- **YearsSinceGraduation:** Can be derived from CurrentYear - GraduationYear
- **TotalDonations:** Can be derived by summing DONATION.Amount for an Alumni
- **TotalEventsAttended:** Can be derived by counting EVENT_REGISTRATION records

---

## 10. Aggregation

Used for the MENTORSHIP relationship:
- Mentorship aggregates the relationship between two ALUMNI entities (Mentor and Mentee)
- This allows us to attach attributes to the mentorship itself (StartDate, EndDate, Status, etc.)

---

This ER Model provides a comprehensive foundation for the Alumni Network and Engagement Platform database design.
