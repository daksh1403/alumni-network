# Normalization Report
## Alumni Network and Engagement Platform

---

## 1. DEPARTMENT

### 1NF Check
✅ All attributes are atomic (no repeating groups)

### Functional Dependencies
```
DeptID → DeptName, DeptCode, HODName, EstablishedYear
DeptName → DeptID, DeptCode, HODName, EstablishedYear (Candidate Key)
DeptCode → DeptID, DeptName, HODName, EstablishedYear (Candidate Key)
```

### Candidate Keys
- DeptID
- DeptName
- DeptCode

### 2NF Check
✅ Single attribute PK, no partial dependencies possible

### 3NF Check
✅ No transitive dependencies
- DeptName → DeptCode (both are candidate keys, not transitive)

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 2. BATCH

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
BatchID → BatchYear, Section, TotalStudents, DeptID
DeptID → (references DEPARTMENT)
```

### Candidate Keys
- BatchID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies
- All non-key attributes depend directly on BatchID

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 3. COMPANY

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
CompanyID → CompanyName, Industry, CompanySize, Website, Headquarters
```

### Candidate Keys
- CompanyID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 4. SKILL

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
SkillID → SkillName, SkillCategory, Description
SkillName → SkillID, SkillCategory, Description (Candidate Key)
```

### Candidate Keys
- SkillID
- SkillName

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 5. ALUMNI

### 1NF Check
✅ All attributes are atomic (Address decomposed into City, State, PinCode)

### Functional Dependencies
```
AlumniID → FirstName, LastName, Email, DateOfBirth, Gender, 
           Address_City, Address_State, Address_PinCode, 
           GraduationYear, DeptID, BatchID, CompanyID, 
           CurrentPosition, LinkedInProfile, IsActive

Email → AlumniID, FirstName, LastName, ... (Candidate Key)

DeptID → (references DEPARTMENT)
BatchID → (references BATCH)
CompanyID → (references COMPANY)
```

### Candidate Keys
- AlumniID
- Email

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies
- All non-key attributes depend directly on AlumniID
- FK references (DeptID, BatchID, CompanyID) are not transitive

### BCNF Check
✅ Every determinant is a candidate key

### Normalization Steps:
1. **Original (Unnormalized):**
   ```
   ALUMNI(AlumniID, FirstName, LastName, Email, Phone1, Phone2, ..., 
          Address, GraduationYear, DeptID, BatchID, CompanyID, ...)
   ```

2. **1NF (Remove repeating groups):**
   - Phone moved to ALUMNI_PHONE table
   - Address decomposed into Address_City, Address_State, Address_PinCode

3. **2NF, 3NF, BCNF:**
   - Already satisfied with single attribute PK

### Result: **Already in BCNF** ✅

---

## 6. STUDENT

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
StudentID → FirstName, LastName, Email, EnrollmentYear, 
            DeptID, CurrentSemester, CGPA

Email → StudentID, FirstName, LastName, ... (Candidate Key)

DeptID → (references DEPARTMENT)
```

### Candidate Keys
- StudentID
- Email

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 7. EVENT

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
EventID → EventName, EventType, EventDate, Venue, OrganizerID

OrganizerID → (references ALUMNI)
```

### Candidate Keys
- EventID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 8. DONATION

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
DonationID → DonorID, Amount, DonationDate, PaymentMethod

DonorID → (references ALUMNI)
```

### Candidate Keys
- DonationID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 9. JOB

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
JobID → JobTitle, JobType, Salary, CompanyID, PostedBy

CompanyID → (references COMPANY)
PostedBy → (references ALUMNI)
```

### Candidate Keys
- JobID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 10. MENTORSHIP

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
MentorshipID → MentorID, MenteeID, StartDate, EndDate, Status, 
               MentorshipArea, Goals

MentorID → (references ALUMNI)
MenteeID → (references ALUMNI)
```

### Candidate Keys
- MentorshipID

### 2NF Check
✅ Single attribute PK, no partial dependencies

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 11. ALUMNI_SKILL (Junction Table)

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
(AlumniID, SkillID) → (no other attributes)
```

### Candidate Keys
- (AlumniID, SkillID) - Composite Key

### 2NF Check
✅ No partial dependencies (both attributes form the key)

### 3NF Check
✅ No non-key attributes, so no transitive dependencies possible

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 12. ALUMNI_PHONE (Multivalued Attribute)

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
(AlumniID, PhoneNumber) → (no other attributes)
```

### Candidate Keys
- (AlumniID, PhoneNumber) - Composite Key

### 2NF Check
✅ No partial dependencies

### 3NF Check
✅ No non-key attributes

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## 13. ALUMNI_EVENT (Junction Table)

### 1NF Check
✅ All attributes are atomic

### Functional Dependencies
```
(AlumniID, EventID) → RegistrationDate
```

### Candidate Keys
- (AlumniID, EventID) - Composite Key

### 2NF Check
✅ RegistrationDate depends on the full composite key

### 3NF Check
✅ No transitive dependencies

### BCNF Check
✅ Every determinant is a candidate key

### Result: **Already in BCNF** ✅

---

## Summary Table

| Table | 1NF | 2NF | 3NF | BCNF | Notes |
|-------|-----|-----|-----|------|-------|
| DEPARTMENT | ✅ | ✅ | ✅ | ✅ | Multiple candidate keys |
| BATCH | ✅ | ✅ | ✅ | ✅ | |
| COMPANY | ✅ | ✅ | ✅ | ✅ | |
| SKILL | ✅ | ✅ | ✅ | ✅ | SkillName is candidate key |
| ALUMNI | ✅ | ✅ | ✅ | ✅ | Email is candidate key |
| STUDENT | ✅ | ✅ | ✅ | ✅ | Email is candidate key |
| EVENT | ✅ | ✅ | ✅ | ✅ | |
| DONATION | ✅ | ✅ | ✅ | ✅ | |
| JOB | ✅ | ✅ | ✅ | ✅ | |
| MENTORSHIP | ✅ | ✅ | ✅ | ✅ | |
| ALUMNI_SKILL | ✅ | ✅ | ✅ | ✅ | Junction table |
| ALUMNI_PHONE | ✅ | ✅ | ✅ | ✅ | Multivalued |
| ALUMNI_EVENT | ✅ | ✅ | ✅ | ✅ | Junction table |

---

## Normalization Decisions

### 1. Phone Numbers (Multivalued Attribute)
**Decision:** Created separate ALUMNI_PHONE table

**Reasoning:**
- Phone is multivalued in ER diagram
- Storing multiple phones in a single column violates 1NF
- Separate table allows unlimited phone numbers per alumni

### 2. Address (Composite Attribute)
**Decision:** Decomposed into Address_City, Address_State, Address_PinCode

**Reasoning:**
- Composite attributes should be split into atomic components
- Allows querying by individual address parts
- Maintains 1NF compliance

### 3. Derived Attributes
**Decision:** Age, YearsSinceGraduation, TotalDonations not stored

**Reasoning:**
- Can be computed at query time
- Avoids update anomalies
- Reduces storage redundancy

### 4. M:N Relationships
**Decision:** Created junction tables (ALUMNI_SKILL, ALUMNI_EVENT)

**Reasoning:**
- M:N relationships cannot be directly implemented in relational model
- Junction tables resolve to 1:N relationships
- Composite PKs ensure uniqueness

### 5. Weak Entity (MENTORSHIP)
**Decision:** MentorshipID as primary key with FK references

**Reasoning:**
- Weak entities need owner's key
- MentorshipID provides unique identification
- MentorID and MenteeID are FKs referencing ALUMNI

---

## Conclusion

**All 13 tables are in BCNF (Boyce-Codd Normal Form).**

The schema is fully normalized with:
- ✅ No partial dependencies (2NF)
- ✅ No transitive dependencies (3NF)
- ✅ Every determinant is a candidate key (BCNF)

**No further normalization required.**
