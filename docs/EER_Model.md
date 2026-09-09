# Extended Entity-Relationship (EER) Model
## Alumni Network and Engagement Platform

## 1. Generalization / Specialization

### 1.1 PERSON Supertype

**Generalization Hierarchy:** PERSON is a supertype that generalizes common attributes shared by different types of users in the system.

```
                         ┌─────────────┐
                         │    PERSON   │
                         │ (Supertype) │
                         └──────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │    ALUMNI    │ │   STUDENT    │ │    ADMIN     │
        │  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │
        └──────────────┘ └──────────────┘ └──────────────┘
```

#### PERSON (Supertype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| PersonID | INT | PK, NOT NULL |
| FirstName | VARCHAR(50) | NOT NULL |
| LastName | VARCHAR(50) | NOT NULL |
| Email | VARCHAR(100) | UNIQUE, NOT NULL |
| Phone | VARCHAR(15) | |
| DateOfBirth | DATE | |
| Gender | CHAR(1) | CHECK (M/F/O) |
| Address | VARCHAR(200) | |
| ProfilePicture | VARCHAR(255) | |
| CreatedAt | DATETIME | DEFAULT CURRENT_TIMESTAMP |

#### ALUMNI (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| PersonID | INT | PK, FK (REFERENCES PERSON) |
| GraduationYear | INT | NOT NULL |
| DeptID | INT | FK (REFERENCES DEPARTMENT) |
| BatchID | INT | FK (REFERENCES BATCH) |
| CurrentCompanyID | INT | FK (REFERENCES COMPANY) |
| CurrentPosition | VARCHAR(100) | |
| LinkedInProfile | VARCHAR(200) | |
| IsActive | BOOLEAN | DEFAULT TRUE |

#### STUDENT (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| PersonID | INT | PK, FK (REFERENCES PERSON) |
| StudentID | VARCHAR(20) | UNIQUE, NOT NULL |
| EnrollmentYear | INT | NOT NULL |
| DeptID | INT | FK (REFERENCES DEPARTMENT) |
| CurrentSemester | INT | |
| CGPA | DECIMAL(4,2) | |

#### ADMIN (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| PersonID | INT | PK, FK (REFERENCES PERSON) |
| AdminRole | VARCHAR(50) | NOT NULL |
| Department | VARCHAR(100) | |
| AccessLevel | INT | CHECK (1-5) |

**Constraints:**
- **Disjoint:** A person can be only ONE type (Alumni, Student, or Admin)
- **Total:** Every person must be classified as one of the subtypes
- **Inheritance:** Subtypes inherit all attributes from PERSON supertype

---

### 1.2 CONTENT Supertype

**Generalization Hierarchy:** CONTENT generalizes different types of user-generated content.

```
                         ┌─────────────┐
                         │   CONTENT   │
                         │ (Supertype) │
                         └──────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │     POST     │ │   COMMENT    │ │   REPLY      │
        │  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │
        └──────────────┘ └──────────────┘ └──────────────┘
```

#### CONTENT (Supertype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| ContentID | INT | PK, NOT NULL |
| AuthorID | INT | FK (REFERENCES PERSON) |
| ContentText | TEXT | NOT NULL |
| CreatedDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| LastModifiedDate | DATETIME | |
| IsActive | BOOLEAN | DEFAULT TRUE |

#### POST (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| ContentID | INT | PK, FK (REFERENCES CONTENT) |
| ForumID | INT | FK (REFERENCES FORUM) |
| Title | VARCHAR(200) | NOT NULL |
| LikesCount | INT | DEFAULT 0 |
| IsPinned | BOOLEAN | DEFAULT FALSE |

#### COMMENT (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| ContentID | INT | PK, FK (REFERENCES CONTENT) |
| PostID | INT | FK (REFERENCES POST) |
| LikesCount | INT | DEFAULT 0 |

#### REPLY (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| ContentID | INT | PK, FK (REFERENCES CONTENT) |
| CommentID | INT | FK (REFERENCES COMMENT) |

**Constraints:**
- **Disjoint:** Content can be only ONE type
- **Total:** Every content must be classified
- **Overlap:** Not allowed (content cannot be both post and comment)

---

### 1.3 TRANSACTION Supertype

**Generalization Hierarchy:** TRANSACTION generalizes different types of financial transactions.

```
                         ┌──────────────┐
                         │ TRANSACTION  │
                         │  (Supertype) │
                         └──────┬───────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   DONATION   │ │ EVENT_FEE    │ │ MEMBERSHIP   │
        │  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │
        └──────────────┘ └──────────────┘ └──────────────┘
```

#### TRANSACTION (Supertype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| TransactionID | INT | PK, NOT NULL |
| UserID | INT | FK (REFERENCES PERSON) |
| Amount | DECIMAL(12,2) | NOT NULL |
| TransactionDate | DATE | NOT NULL |
| PaymentMethod | VARCHAR(30) | CHECK (Online/Check/DD/Cash) |
| Status | VARCHAR(20) | CHECK (Pending/Completed/Failed/Refunded) |
| ReferenceNumber | VARCHAR(50) | UNIQUE |

#### DONATION (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| TransactionID | INT | PK, FK (REFERENCES TRANSACTION) |
| Purpose | VARCHAR(100) | |
| IsAnonymous | BOOLEAN | DEFAULT FALSE |
| ReceiptNumber | VARCHAR(50) | UNIQUE |

#### EVENT_FEE (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| TransactionID | INT | PK, FK (REFERENCES TRANSACTION) |
| EventID | INT | FK (REFERENCES EVENT) |
| RegistrationType | VARCHAR(30) | |

#### MEMBERSHIP (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| TransactionID | INT | PK, FK (REFERENCES TRANSACTION) |
| MembershipType | VARCHAR(30) | CHECK (Basic/Premium/Lifetime) |
| StartDate | DATE | NOT NULL |
| EndDate | DATE | |

**Constraints:**
- **Disjoint:** A transaction can be only ONE type
- **Partial:** Not all transactions need to be classified (future extensibility)

---

## 2. Categories (Union Types)

### 2.1 NOTIFICATION_RECIPIENT

A notification can be sent to different types of recipients.

```
                    ┌─────────────────────┐
                    │     NOTIFICATION    │
                    └──────────┬──────────┘
                               │
                               │ Recipient
                               │
                    ┌──────────┴──────────┐
                    │         ∪           │
                    │      (UNION)        │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │    ALUMNI    │    │   STUDENT    │    │    ADMIN     │
    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 3. Specialization with Attributes

### 3.1 EVENT Specialization

Events can be specialized based on their type, with each subtype having additional specific attributes.

```
                         ┌─────────────┐
                         │    EVENT    │
                         │ (Supertype) │
                         └──────┬──────┘
                                │
        ┌───────────────┬───────┴───────┬───────────────┐
        │               │               │               │
        ▼               ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   REUNION    │ │  WORKSHOP    │ │   SEMINAR    │ │ NETWORKING   │
│  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

#### REUNION (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| EventID | INT | PK, FK (REFERENCES EVENT) |
| BatchYear | INT | NOT NULL |
| Theme | VARCHAR(100) | |
| DressCode | VARCHAR(50) | |

#### WORKSHOP (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| EventID | INT | PK, FK (REFERENCES EVENT) |
| Topic | VARCHAR(100) | NOT NULL |
| InstructorID | INT | FK (REFERENCES PERSON) |
| Duration | INT | (in hours) |
| Prerequisites | TEXT | |
| Materials | TEXT | |

#### SEMINAR (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| EventID | INT | PK, FK (REFERENCES EVENT) |
| SpeakerID | INT | FK (REFERENCES PERSON) |
| Topic | VARCHAR(200) | NOT NULL |
| Abstract | TEXT | |
| RecordingURL | VARCHAR(255) | |

#### NETWORKING (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| EventID | INT | PK, FK (REFERENCES EVENT) |
| Industry | VARCHAR(50) | |
| TargetAudience | VARCHAR(100) | |
| TableSize | INT | |

**Constraints:**
- **Disjoint:** An event can be only ONE type
- **Total:** Every event must be classified
- **Overlap:** Not allowed

---

## 4. Specialization with Constraints

### 4.1 JOB Specialization

```
                         ┌─────────────┐
                         │     JOB     │
                         │ (Supertype) │
                         └──────┬──────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  FULL_TIME   │ │  PART_TIME   │ │  INTERNSHIP  │
        │  (Subtype)   │ │  (Subtype)   │ │  (Subtype)   │
        └──────────────┘ └──────────────┘ └──────────────┘
```

#### FULL_TIME (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| JobID | INT | PK, FK (REFERENCES JOB) |
| Salary | DECIMAL(12,2) | |
| Benefits | TEXT | |
| WorkHours | INT | DEFAULT 40 |

#### PART_TIME (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| JobID | INT | PK, FK (REFERENCES JOB) |
| HourlyRate | DECIMAL(8,2) | |
| MaxHours | INT | |
| Schedule | VARCHAR(100) | |

#### INTERNSHIP (Subtype)
| Attribute | Type | Constraints |
|-----------|------|-------------|
| JobID | INT | PK, FK (REFERENCES JOB) |
| Stipend | DECIMAL(10,2) | |
| Duration | INT | (in months) |
| IsPaid | BOOLEAN | DEFAULT TRUE |
| ConversionChance | VARCHAR(20) | |

**Constraints:**
- **Disjoint:** A job can be only ONE type
- **Partial:** Not all jobs need specialization
- **Overlap:** Not allowed

---

## 5. Aggregation in EER

### 5.1 MENTORSHIP Aggregation

The MENTORSHIP relationship is an aggregation that combines two ALUMNI entities with additional attributes.

```
    ┌─────────────┐                    ┌─────────────┐
    │   ALUMNI    │                    │   ALUMNI    │
    │  (Mentor)   │                    │  (Mentee)   │
    └──────┬──────┘                    └──────┬──────┘
           │                                  │
           │ 1                                │ 1
           │                                  │
           ▼                                  ▼
    ┌─────────────────────────────────────────────────┐
    │              MENTORSHIP_RELATIONSHIP             │
    │  (Aggregated Relationship)                       │
    │                                                  │
    │  Attributes:                                     │
    │  - StartDate                                     │
    │  - EndDate                                       │
    │  - Status                                        │
    │  - MentorshipArea                                │
    │  - Goals                                         │
    │  - Feedback                                      │
    │  - Rating                                        │
    └─────────────────────────────────────────────────┘
```

---

## 6. Cardinality Constraints in EER

### 6.1 Complex Constraints

| Constraint Type | Description | Example |
|----------------|-------------|---------|
| **Disjointness** | Subtypes do not overlap | Alumni cannot be Student simultaneously |
| **Completeness** | Every instance must belong to a subtype | Every Person must be Alumni, Student, or Admin |
| **Cardinality** | Min/Max participation | Alumni must belong to at least 1 department |
| ** Participation** | Total or Partial | Alumni has total participation in DEPARTMENT |

### 6.2 Participation Constraints

| Entity | Relationship | Min | Max | Type |
|--------|--------------|-----|-----|------|
| ALUMNI | belongs_to DEPARTMENT | 1 | 1 | Total |
| ALUMNI | belongs_to BATCH | 1 | 1 | Total |
| ALUMNI | works_at COMPANY | 0 | 1 | Partial |
| ALUMNI | has SKILL | 0 | N | Partial |
| ALUMNI | attends EVENT | 0 | N | Partial |
| ALUMNI | makes DONATION | 0 | N | Partial |
| ALUMNI | posts JOB | 0 | N | Partial |
| ALUMNI | mentors via MENTORSHIP | 0 | N | Partial |
| ALUMNI | creates FORUM | 0 | N | Partial |
| EVENT | organized_by ALUMNI | 1 | 1 | Total |
| DONATION | made_by ALUMNI | 1 | 1 | Total |
| JOB | posted_by ALUMNI | 1 | 1 | Total |
| JOB | at COMPANY | 1 | 1 | Total |
| FORUM | created_by ALUMNI | 1 | 1 | Total |
| POST | in FORUM | 1 | 1 | Total |
| POST | authored_by ALUMNI | 1 | 1 | Total |
| COMMENT | on POST | 1 | 1 | Total |
| COMMENT | authored_by ALUMNI | 1 | 1 | Total |

---

## 7. EER Diagram Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EER MODEL OVERVIEW                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐                                                            │
│  │ PERSON  │──────────┬──────────────┬──────────────┐                  │
│  │(Super)  │          │              │              │                  │
│  └─────────┘          │              │              │                  │
│      │          ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐           │
│      │          │  ALUMNI   │  │  STUDENT  │  │   ADMIN   │           │
│      │          └───────────┘  └───────────┘  └───────────┘           │
│      │               │                                                 │
│      │               │ (M:N)                                           │
│      │               │                                                 │
│      │         ┌─────┴─────┐                                           │
│      │         │   SKILL   │                                           │
│      │         └───────────┘                                           │
│      │               │                                                 │
│      │               │ (1:N)                                           │
│      │               │                                                 │
│      │    ┌──────────┼──────────┬──────────────┬──────────────┐        │
│      │    │          │          │              │              │        │
│      │ ┌──┴───┐  ┌───┴───┐  ┌───┴───┐    ┌────┴────┐   ┌────┴────┐   │
│      │ │EVENT │  │DONATION│  │  JOB  │    │MENTORSHIP│  │  FORUM  │   │
│      │ └──────┘  └────────┘  └───────┘    └─────────┘   └─────────┘   │
│      │    │                     │                        │             │
│      │    │ (M:N)               │ (1:N)                  │ (1:N)      │
│      │    │                     │                        │             │
│      │ ┌──┴──────────┐    ┌─────┴─────┐            ┌─────┴─────┐      │
│      │ │EVENT_REG    │    │  COMPANY  │            │   POST    │      │
│      │ └─────────────┘    └───────────┘            └───────────┘      │
│      │                                                                │
│      │                           ┌───────────────────────────────┐    │
│      └───────────────────────────│          CONTENT (Super)      │    │
│                                  └───────────────────────────────┘    │
│                                          │                            │
│                              ┌───────────┼───────────┐                │
│                              │           │           │                │
│                         ┌────┴────┐ ┌────┴────┐ ┌────┴────┐          │
│                         │  POST   │ │ COMMENT │ │  REPLY  │          │
│                         └─────────┘ └─────────┘ └─────────┘          │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Design Decisions

### 8.1 Why Generalization?

1. **Code Reusability:** Common attributes stored once in supertype
2. **Data Integrity:** Consistent data across subtypes
3. **Query Efficiency:** Join operations are optimized
4. **Maintainability:** Changes to common attributes affect all subtypes

### 8.2 Why Disjoint Constraints?

1. **Business Rules:** Alumni cannot be current students simultaneously
2. **Data Consistency:** Prevents conflicting classifications
3. **Simplified Queries:** No need to handle overlapping cases

### 8.3 Why Partial Participation?

1. **Flexibility:** Not all alumni need to have skills, attend events, etc.
2. **Real-world Modeling:** Matches actual alumni behavior
3. **Future Extensibility:** Easy to add optional relationships

---

## 9. Mapping EER to Relational Schema

The EER model maps to relational schema using these strategies:

1. **Supertype/Subtype:** 
   - Option A: Single table with type discriminator
   - Option B: Separate tables with foreign keys to supertype
   - **Chosen:** Option B for better normalization

2. **M:N Relationships:** 
   - Create junction tables with composite keys
   - Add relationship attributes to junction table

3. **1:N Relationships:**
   - Add foreign key to the "many" side
   - Include relationship attributes in the "many" side table

4. **Aggregation:**
   - Create separate table for the aggregated relationship
   - Include all participating entity keys as foreign keys

---

This EER Model provides a comprehensive, normalized design for the Alumni Network and Engagement Platform that supports all required functionality while maintaining data integrity and efficiency.
