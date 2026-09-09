# Live Demonstration Script - DA2
## Alumni Network and Engagement Platform (Oracle SQL + PL/SQL)

Companion to `report/Alumni_Network_Demo_Presentation.pptx`.
Every command below was executed and verified; expected outputs come from
`logs/run_04_demo_queries.log`.

---

## 0. Setup (before audience arrives)

```bash
cd /Users/dakshagarwal/dbms-project

# If using the local Docker Oracle:
docker start oracle-free                      # wait ~1 min for "DATABASE IS READY"
/opt/oracle/instantclient_23_26/sqlplus -S alumni/alumni123@localhost:1521/FREEPDB1
```

Fresh rebuild (only if needed) - takes under a minute:

```
@sql/00_drop_all.sql
@sql/01_schema.sql
@sql/02_plsql.sql
@sql/03_seed_data.sql
SET SERVEROUTPUT ON SIZE UNLIMITED
SET LINESIZE 140
```

> On **Oracle Live SQL**: paste scripts 01 -> 02 -> 03 into the worksheet in order,
> enable DBMS_OUTPUT in settings, then follow the same demo steps.

---

## 1. Schema inventory (Slide 12)

```sql
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT object_type, COUNT(*) FROM user_objects GROUP BY object_type ORDER BY 1;
```

Expected: 22 tables; totals = 18 sequences, 22 triggers, 4 procedures,
3 functions, package + body, 3 views.

---

## 2. Queries Q1-Q7 (Slides 4-11)

Run from `@sql/04_demo_queries.sql` sections Q1..Q7:

| Show | Highlight |
|------|-----------|
| Q1 | LEFT JOIN keeps alumni with NULL company |
| Q3 | GROUP BY + HAVING filters departments with > 2 alumni (CSE wins: 5) |
| Q5 | Correlated NOT EXISTS finds non-donors |
| Q6 | RANK() analytical function on registrations |
| Q7 | CONNECT BY PRIOR prints the nested comment tree of Post #1 with indentation |

---

## 3. Procedure happy paths (Slide 8)

```sql
DECLARE v VARCHAR2(200);
BEGIN sp_record_donation(6, 5000, 'Online', 'General Fund', v); END;
/
EXEC sp_register_event(6, 5);
EXEC sp_apply_to_job(2, 10, 'drive.google.com/resume/meera.pdf');
EXEC sp_close_mentorship(2, TRUNC(SYSDATE), 'Great PM interview preparation.', 5);
```

Expected:

```
[OK] Donation of Rs.5000.00 recorded from Ananya Iyer. Receipt: RCP-1012-2026
[OK] Alumnus #6 registered for "Annual Tech Meetup" (#5)
[OK] Application submitted for "Product Management Intern" (#2)
[OK] Mentorship #2 marked Completed (rating: 5/5).
```

Point out the auto-generated receipt number (`RCP-<seq>-<yyyy>`) produced by
trigger R1.

---

## 4. Business rules rejecting bad input (Slide 10)

```sql
-- 4a. Full event: Reunion (#1) already has 3/3 seats
BEGIN
    INSERT INTO EVENT_REGISTRATION (AlumniID, EventID) VALUES (7, 1);
EXCEPTION WHEN OTHERS THEN DBMS_OUTPUT.PUT_LINE('CAUGHT: ' || SQLERRM); END;
/

-- 4b. Duplicate job application
BEGIN sp_apply_to_job(1, 3);   -- alumnus 3 applied to job 1 earlier
EXCEPTION WHEN OTHERS THEN DBMS_OUTPUT.PUT_LINE('CAUGHT: ' || SQLERRM); END;
/

-- 4c. Self-mentorship
BEGIN
    INSERT INTO MENTORSHIP (MentorID, MenteeID, StartDate, Status)
    VALUES (1, 1, TRUNC(SYSDATE), 'Active');
EXCEPTION WHEN OTHERS THEN DBMS_OUTPUT.PUT_LINE('CAUGHT: ' || SQLERRM); END;
/
```

Expected: ORA-20002 ("Event is FULL (3/3)..."), ORA-20205 ("already applied"),
ORA-20003 ("same person").

---

## 5. Audit trail (trigger R5)

```sql
SELECT AuditID, Operation, AlumniID, NewValues, ChangeTS
  FROM ALUMNI_AUDIT ORDER BY AuditID;
```

Expected: one INSERT row per seeded alumnus (10 rows), plus DELETE entries if
you demonstrate deleting an alumnus live.

---

## 6. Package & functions (Slides 9)

```sql
EXEC pkg_alumni_reports.top_donors(5);
EXEC pkg_alumni_reports.dept_alumni_summary;

SELECT fn_total_donations(3)  AS arjun_total      FROM DUAL;
SELECT fn_event_occupancy(1)  AS reunion_full_pct FROM DUAL;   -- returns 100
```

---

## 7. Closing line

"The database enforces every rule at two levels - declarative constraints and
PL/SQL triggers/procedures - exactly as designed in DA1."

### Likely viva questions

- Why sequences+triggers instead of IDENTITY? (portability to 11g labs; explicit control)
- Mutating-table risk on capacity trigger? (BEFORE row trigger on single-row INSERT reads pre-statement snapshot - safe; compound trigger needed only for multi-row DML)
- Where does ON UPDATE CASCADE go? (Oracle doesn't support it; documented omission)
- How is receipt uniqueness guaranteed? (sequence + UNIQUE constraint)
