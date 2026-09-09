# Normalization Analysis
## Alumni Network and Engagement Platform

## 1. Introduction to Normalization

Normalization is a process of organizing data in a database to:
- Eliminate redundancy (duplicate data)
- Ensure data dependencies make sense
- Protect data integrity
- Reduce storage space
- Prevent update, insertion, and deletion anomalies

### Normal Forms Hierarchy:
```
1NF → 2NF → 3NF → BCNF → 4NF → 5NF
```

---

## 2. First Normal Form (1NF)

### Definition
A relation is in 1NF if:
- All attributes contain only atomic (indivisible) values
- Each row is unique (has a primary key)
- No repeating groups or arrays

### Analysis of Relations

#### ALUMNI Relation (Before 1NF)

| AlumniID | Name | Email | Skills | EventsAttended |
|----------|------|-------|--------|----------------|
| 1 | John Doe | john@email.com | Java, Python, SQL | Reunion2023, Workshop2024 |
| 2 | Jane Smith | jane@email.com | C++, Python | Seminar2024 |

**Violation:** Skills and EventsAttended contain multiple values (not atomic)

#### ALUMNI Relation (After 1NF)

**Table: ALUMNI**
| AlumniID | FirstName | LastName | Email | Phone | DOB | Gender | GraduationYear |
|----------|-----------|----------|-------|-------|-----|--------|----------------|
| 1 | John | Doe | john@email.com | 1234567890 | 1995-05-15 | M | 2017 |
| 2 | Jane | Smith | jane@email.com | 9876543210 | 1996-08-22 | F | 2018 |

**Table: ALUMNI_SKILL**
| AlumniID | SkillID | ProficiencyLevel |
|----------|---------|------------------|
| 1 | 1 | Expert |
| 1 | 2 | Intermediate |
| 1 | 3 | Expert |
| 2 | 4 | Expert |
| 2 | 2 | Beginner |

**Table: ALUMNI_EVENT**
| AlumniID | EventID | RegistrationDate | AttendanceStatus |
|----------|---------|------------------|------------------|
| 1 | 101 | 2023-06-01 | Attended |
| 1 | 102 | 2024-01-15 | Registered |
| 2 | 103 | 2024-03-20 | Attended |

---

## 3. Second Normal Form (2NF)

### Definition
A relation is in 2NF if:
- It is in 1NF
- No partial dependency exists (non-key attributes depend on the WHOLE primary key)

### Analysis

#### ALUMNI_SKILL Relation (Check for 2NF)

**Functional Dependencies:**
```
AlumniID, SkillID → ProficiencyLevel (Full dependency - OK)
AlumniID → FirstName, LastName, Email (Partial dependency - VIOLATION)
```

**Problem:** If we combine Alumni and Skill information in one table, non-key attributes like FirstName depend only on AlumniID (part of the composite key).

**Solution:** Decompose into separate tables:

**Table: ALUMNI** (Primary Key: AlumniID)
| AlumniID | FirstName | LastName | Email | ... |
|----------|-----------|----------|-------|-----|

**Table: SKILL** (Primary Key: SkillID)
| SkillID | SkillName | SkillCategory | Description |
|---------|-----------|---------------|-------------|

**Table: ALUMNI_SKILL** (Primary Key: AlumniID, SkillID)
| AlumniID | SkillID | ProficiencyLevel |
|----------|---------|------------------|

#### EVENT_REGISTRATION Relation (Check for 2NF)

**Functional Dependencies:**
```
AlumniID, EventID → RegistrationDate, AttendanceStatus (Full dependency - OK)
EventID → EventName, EventDate, Venue (Partial dependency - VIOLATION)
```

**Problem:** Event details depend only on EventID, not on the full composite key (AlumniID, EventID).

**Solution:** Decompose:

**Table: EVENT** (Primary Key: EventID)
| EventID | EventName | EventType | EventDate | Venue | ... |
|---------|-----------|-----------|-----------|-------|-----|

**Table: EVENT_REGISTRATION** (Primary Key: AlumniID, EventID)
| AlumniID | EventID | RegistrationDate | AttendanceStatus |
|----------|---------|------------------|------------------|

---

## 4. Third Normal Form (3NF)

### Definition
A relation is in 3NF if:
- It is in 2NF
- No transitive dependency exists (non-key attributes don't depend on other non-key attributes)

### Analysis

#### ALUMNI Relation (Check for 3NF)

**Functional Dependencies:**
```
AlumniID → FirstName, LastName, Email, Phone, DOB, Gender, GraduationYear
AlumniID → CurrentCity, CurrentState, CurrentCountry
AlumniID → DeptID → DeptName (Transitive dependency!)
AlumniID → CompanyID → CompanyName (Transitive dependency!)
```

**Problem:** DeptName depends on DeptID, which depends on AlumniID. This creates a transitive dependency.

**Solution:** Decompose:

**Table: ALUMNI** (Primary Key: AlumniID)
| AlumniID | FirstName | LastName | Email | ... | DeptID | CompanyID |
|----------|-----------|----------|-------|-----|--------|-----------|

**Table: DEPARTMENT** (Primary Key: DeptID)
| DeptID | DeptName | DeptCode | HODName | EstablishedYear |
|--------|----------|----------|---------|-----------------|

**Table: COMPANY** (Primary Key: CompanyID)
| CompanyID | CompanyName | Industry | ... |
|-----------|-------------|----------|-----|

#### JOB Relation (Check for 3NF)

**Functional Dependencies:**
```
JobID → JobTitle, JobType, Location, Description
JobID → CompanyID → CompanyName, Industry (Transitive!)
JobID → PostedBy → PostedByName, PostedByEmail (Transitive!)
```

**Problem:** CompanyName depends on CompanyID, which depends on JobID.

**Solution:** Keep CompanyID as foreign key, don't store CompanyName in JOB table.

**Table: JOB** (Primary Key: JobID)
| JobID | JobTitle | CompanyID | PostedBy | JobType | Location | ... |
|-------|----------|-----------|----------|---------|----------|-----|

---

## 5. Boyce-Codd Normal Form (BCNF)

### Definition
A relation is in BCNF if:
- It is in 3NF
- For every functional dependency X → Y, X is a superkey

### Analysis

#### MENTORSHIP Relation (Check for BCNF)

**Candidate Keys:**
- (MentorID, MenteeID, StartDate) - Primary Key
- (MentorID, MenteeID, MentorshipArea) - Alternative Key

**Functional Dependencies:**
```
MentorID, MenteeID, StartDate → Status, EndDate, Goals, Feedback, Rating
MentorID, MenteeID → MentorshipArea (Potential BCNF violation!)
```

**Problem:** If MentorshipArea depends on (MentorID, MenteeID) but not on the full primary key, we have a BCNF violation.

**Analysis:** 
- A mentor-mentee pair might have multiple mentorships (at different times)
- MentorshipArea could be specific to each mentorship instance
- Therefore: MentorID, MenteeID, StartDate → MentorshipArea (No violation)

**Result:** MENTORSHIP is in BCNF after proper analysis.

#### EVENT_REGISTRATION Relation (Check for BCNF)

**Candidate Keys:**
- (AlumniID, EventID) - Primary Key

**Functional Dependencies:**
```
AlumniID, EventID → RegistrationDate, AttendanceStatus
```

**Analysis:** Left side (AlumniID, EventID) is a superkey. No violation.

**Result:** EVENT_REGISTRATION is in BCNF.

#### ALUMNI_SKILL Relation (Check for BCNF)

**Candidate Keys:**
- (AlumniID, SkillID) - Primary Key

**Functional Dependencies:**
```
AlumniID, SkillID → ProficiencyLevel
```

**Analysis:** Left side (AlumniID, SkillID) is a superkey. No violation.

**Result:** ALUMNI_SKILL is in BCNF.

---

## 6. Fourth Normal Form (4NF)

### Definition
A relation is in 4NF if:
- It is in BCNF
- No multi-valued dependencies exist

### Analysis

#### ALUMNI Relation (Check for 4NF)

**Potential Multi-valued Dependencies:**
```
AlumniID →→ Skills (An alumni can have multiple skills)
AlumniID →→ Events (An alumni can attend multiple events)
```

**Problem:** If we store skills and events in the same ALUMNI table, we have multi-valued dependencies.

**Example (Before 4NF):**
| AlumniID | Skill | Event |
|----------|-------|-------|
| 1 | Java | Reunion2023 |
| 1 | Java | Workshop2024 |
| 1 | Python | Reunion2023 |
| 1 | Python | Workshop2024 |

This creates redundancy: Alumni 1's skills are repeated for each event.

**Solution:** Already solved by decomposition into separate tables:
- ALUMNI table
- ALUMNI_SKILL table (AlumniID →→ Skills)
- EVENT_REGISTRATION table (AlumniID →→ Events)

**Result:** All relations are in 4NF after proper decomposition.

---

## 7. Fifth Normal Form (5NF) - Join Dependency

### Definition
A relation is in 5NF if:
- It is in 4NF
- Every join dependency is implied by candidate keys

### Analysis

#### Complex Relationship: Alumni-Skill-Company

Consider a scenario where we want to track which alumni have which skills and work at which companies.

**Potential Relation:**
| AlumniID | SkillID | CompanyID |
|----------|---------|-----------|
| 1 | 1 | 101 |
| 1 | 2 | 101 |
| 2 | 1 | 102 |

**Join Dependencies:**
```
AlumniID, SkillID → CompanyID (If an alumni has a skill, they work at one company)
AlumniID, CompanyID → SkillID (If an alumni works at a company, they have specific skills)
SkillID, CompanyID → AlumniID (If a skill is at a company, specific alumni have it)
```

**Analysis:** This creates a cyclic join dependency that cannot be decomposed without loss.

**Solution:** In our design, we avoid this by:
1. ALUMNI table has CompanyID (current company)
2. ALUMNI_SKILL has skills
3. No direct three-way relationship between Alumni-Skill-Company

**Result:** Our design avoids problematic join dependencies by proper decomposition.

---

## 8. Normalization Summary Table

| Relation | 1NF | 2NF | 3NF | BCNF | 4NF | 5NF | Notes |
|----------|-----|-----|-----|------|-----|-----|-------|
| ALUMNI | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Decomposed to remove transitive deps |
| DEPARTMENT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| BATCH | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| COMPANY | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| SKILL | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| EVENT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| DONATION | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| JOB | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Decomposed to remove transitive deps |
| MENTORSHIP | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Composite key, no violations |
| FORUM | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| POST | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| COMMENT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Single attribute PK |
| ALUMNI_SKILL | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Junction table, no violations |
| EVENT_REGISTRATION | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Junction table, no violations |

---

## 9. Functional Dependencies Summary

### ALUMNI Relation
```
AlumniID → FirstName, LastName, Email, Phone, DateOfBirth, Gender
AlumniID → GraduationYear, CurrentCity, CurrentState, CurrentCountry
AlumniID → LinkedInProfile, ProfilePicture, RegistrationDate, IsActive
AlumniID → DeptID (FK)
AlumniID → BatchID (FK)
AlumniID → CompanyID (FK)
Email → AlumniID (Candidate key)
```

### DEPARTMENT Relation
```
DeptID → DeptName, DeptCode, HODName, EstablishedYear
DeptName → DeptID (Candidate key)
DeptCode → DeptID (Candidate key)
```

### EVENT Relation
```
EventID → EventName, EventType, Description, EventDate, EventTime
EventID → Venue, MaxCapacity, RegistrationFee, OrganizerID, CreatedDate
```

### JOB Relation
```
JobID → JobTitle, CompanyID, PostedBy, JobType, Location
JobID → Salary, Description, Requirements, PostedDate, ExpiryDate, IsActive
```

### MENTORSHIP Relation
```
MentorID, MenteeID, StartDate → EndDate, Status, MentorshipArea
MentorID, MenteeID, StartDate → Goals, Feedback, Rating
```

### DONATION Relation
```
DonationID → DonorID, Amount, DonationDate, PaymentMethod
DonationID → Purpose, TransactionID, IsAnonymous, ReceiptNumber
TransactionID → DonationID (Candidate key)
ReceiptNumber → DonationID (Candidate key)
```

---

## 10. Decomposition Steps Summary

### Step 1: Remove Multi-valued Attributes (1NF)
- Skills → ALUMNI_SKILL junction table
- Events Attended → EVENT_REGISTRATION junction table
- Phone numbers → Keep as single value or create CONTACT table

### Step 2: Remove Partial Dependencies (2NF)
- Separate ALUMNI from EVENT details
- Separate ALUMNI from SKILL details
- Create independent DEPARTMENT, COMPANY, BATCH tables

### Step 3: Remove Transitive Dependencies (3NF)
- DeptName depends on DeptID, not AlumniID → Separate DEPARTMENT table
- CompanyName depends on CompanyID, not AlumniID → Separate COMPANY table
- BatchYear depends on BatchID, not AlumniID → Separate BATCH table

### Step 4: Verify BCNF
- All functional dependencies have superkeys on left side
- No violations found after 3NF decomposition

### Step 5: Eliminate Multi-valued Dependencies (4NF)
- Already handled by junction tables
- No redundant data storage

### Step 6: Verify Join Dependencies (5NF)
- Complex relationships decomposed without loss
- All joins are lossless

---

## 11. Lossless Join Decomposition

All decompositions performed are lossless:
- Natural joins reconstruct original data
- No information is lost
- No spurious tuples are generated

### Verification Example:

**Original:** ALUMNI(AlumniID, FirstName, DeptID, DeptName)

**Decomposed:**
- ALUMNI(AlumniID, FirstName, DeptID)
- DEPARTMENT(DeptID, DeptName)

**Join:** ALUMNI ⋈ DEPARTMENT = Original (Lossless ✓)

---

## 12. Dependency Preservation

All functional dependencies are preserved after decomposition:
- Each FD is captured in at least one decomposed relation
- No need to join tables to verify dependencies
- Constraint checking is efficient

---

## 13. Final Normalized Schema

All relations in the Alumni Network and Engagement Platform are normalized up to BCNF (and 4NF/5NF where applicable). The design:
- Eliminates all redundancy
- Prevents update, insertion, and deletion anomalies
- Maintains data integrity through foreign keys
- Supports efficient querying
- Allows for future extensibility

---

## 14. Practical Examples of Anomalies Prevented

### Update Anomaly (Without Normalization)
**Problem:** If DeptName is stored in ALUMNI table:
```
AlumniID=1: DeptName="Computer Science"
AlumniID=2: DeptName="Computer Science"
```
If department name changes, we must update multiple rows.

**Solution:** With separate DEPARTMENT table, update only one row.

### Insertion Anomaly (Without Normalization)
**Problem:** Cannot add a new department unless an alumni exists for it.

**Solution:** With separate DEPARTMENT table, departments can exist independently.

### Deletion Anomaly (Without Normalization)
**Problem:** If last alumni of a department is deleted, department info is lost.

**Solution:** With separate DEPARTMENT table, department data persists.

---

This normalization analysis ensures the Alumni Network database is properly structured, efficient, and maintainable.

---

## 15. Version 2 — Normalization Refinements

After review, several additional normalization issues and refinements were identified and addressed in v2.

### 15.1 DEPARTMENT.HODName — Transitive Dependency (3NF Violation)

**Problem:** `HODName` stores a person's name as a string. If the HOD changes, the old name is lost; if the same person is HOD of another department, their name is duplicated (redundancy). This is a transitive dependency: `DeptID → HODPersonID → HODName`.

**Solution:** Replace `HODName` with `HODPersonID` as a foreign key to `PERSON(PersonID)`.

```
-- Before (v1)
DEPARTMENT (DeptID, DeptName, DeptCode, HODName, EstablishedYear)

-- After (v2)
DEPARTMENT (DeptID, DeptName, DeptCode, HODPersonID, EstablishedYear)
    HODPersonID → FK to PERSON(PersonID)
```

---

### 15.2 EVENT.EventType — Repeating Domain Values (2NF/3NF Concern)

**Problem:** `EventType` stores values like 'Reunion', 'Workshop', 'Seminar', 'Networking' via a CHECK constraint. Adding a new event type requires altering the schema. Values are repeated across rows.

**Solution:** Extract into a lookup table `EVENT_TYPE`.

```
-- New Table
EVENT_TYPE (
    TypeID    INT PRIMARY KEY AUTO_INCREMENT,
    TypeName  VARCHAR(50) NOT NULL UNIQUE
)

-- Modified EVENT
EVENT (..., EventTypeID INT FK → EVENT_TYPE(TypeID), ...)
```

---

### 15.3 MENTORSHIP.MentorshipArea — Free-Text Redundancy

**Problem:** `MentorshipArea` is a free-text field. Two rows may store "Data Science" and "data science" for the same area — this violates the spirit of 1NF (non-atomic ambiguity) and creates update anomalies.

**Solution:** Extract into a lookup table `MENTORSHIP_AREA`.

```
-- New Table
MENTORSHIP_AREA (
    AreaID   INT PRIMARY KEY AUTO_INCREMENT,
    AreaName VARCHAR(100) NOT NULL UNIQUE
)

-- Modified MENTORSHIP
MENTORSHIP (..., AreaID INT FK → MENTORSHIP_AREA(AreaID), ...)
```

---

### 15.4 COMPANY.CompanySize — Repeating Domain Values

**Problem:** `CompanySize` stores values like "100000+", "50000-100000" repeatedly. These are a bounded set of categories, not free-form data.

**Solution:** Extract into a lookup table `COMPANY_SIZE`.

```
-- New Table
COMPANY_SIZE (
    SizeID   INT PRIMARY KEY AUTO_INCREMENT,
    SizeRange VARCHAR(30) NOT NULL UNIQUE
)

-- Modified COMPANY
COMPANY (..., SizeID INT FK → COMPANY_SIZE(SizeID), ...)
```

---

### 15.5 POST.LikesCount / Derived Attributes — Intentional Denormalization

**Problem:** `POST.LikesCount` is a derived/calculated attribute — it can be computed by counting rows in a `POST_LIKE` junction table. Storing it in the POST table is technically denormalized.

**Decision:** This is an **intentional denormalization** for read performance. The Alumni Network is read-heavy (many users viewing posts, few liking). Computing `COUNT(*)` on every page load is expensive. The trade-off:

| Approach | Pros | Cons |
|----------|------|------|
| Derived (normalize) | Always accurate, no update anomalies | Slow reads, COUNT on every query |
| Stored (denormalize) | Fast reads | Possible stale count, need trigger/app logic |

**Chosen approach:** Keep `LikesCount` as stored, but document it as a conscious denormalization. In production, use a database trigger or application-level increment to keep it consistent.

```sql
-- Trigger to maintain consistency
CREATE TRIGGER update_likes_count
AFTER INSERT ON POST_LIKE
FOR EACH ROW
UPDATE POST SET LikesCount = LikesCount + 1 WHERE PostID = NEW.PostID;
```

---

### 15.6 Missing: JOB_APPLICATION Junction Table (M:N Relationship)

**Problem:** Alumni can apply to jobs posted by other alumni. This is a many-to-many relationship between ALUMNI and JOB that was not modeled.

**Solution:** Add a `JOB_APPLICATION` junction table.

```
-- New Table
JOB_APPLICATION (
    ApplicationID   INT PRIMARY KEY AUTO_INCREMENT,
    JobID           INT NOT NULL,
    ApplicantID     INT NOT NULL,
    ApplicationDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status          VARCHAR(20) CHECK (Status IN ('Applied', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted')),
    ResumeLink      VARCHAR(255),

    FOREIGN KEY (JobID) REFERENCES JOB(JobID),
    FOREIGN KEY (ApplicantID) REFERENCES ALUMNI(PersonID),
    UNIQUE (JobID, ApplicantID)
)
```

---

### 15.7 Updated Normalization Summary Table (v2)

| Relation | 1NF | 2NF | 3NF | BCNF | 4NF | 5NF | v2 Change |
|----------|-----|-----|-----|------|-----|-----|-----------|
| DEPARTMENT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | HODName → HODPersonID FK |
| EVENT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | EventType → EventTypeID FK |
| MENTORSHIP | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | MentorshipArea → AreaID FK |
| COMPANY | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | CompanySize → SizeID FK |
| POST | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | LikesCount denormalized (documented) |
| JOB_APPLICATION | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | New junction table |

---

### 15.8 v2 Functional Dependencies Summary (Changes Only)

#### DEPARTMENT (v2)
```
DeptID → DeptName, DeptCode, HODPersonID, EstablishedYear
HODPersonID → (resolved via FK to PERSON, no redundancy)
```

#### EVENT (v2)
```
EventID → EventName, EventTypeID, Description, EventDate, EventTime
EventTypeID → TypeName (resolved via FK to EVENT_TYPE)
```

#### MENTORSHIP (v2)
```
MentorID, MenteeID, StartDate → EndDate, Status, AreaID, Goals, Feedback, Rating
AreaID → AreaName (resolved via FK to MENTORSHIP_AREA)
```

#### JOB_APPLICATION (v2)
```
JobID, ApplicantID → ApplicationDate, Status, ResumeLink
```
