-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Part 2: PL/SQL Components
--   A : Sequences + auto-increment triggers (surrogate keys)
--   B : Business-rule triggers
--   C : Views
--   D : Functions
--   E : Stored procedures
--   F : Package PKG_ALUMNI_REPORTS
-- Target: Oracle 11g+
-- ====================================================================
SET SERVEROUTPUT ON SIZE UNLIMITED

-- ====================================================================
-- SECTION A: SEQUENCES AND AUTO-INCREMENT TRIGGERS
-- ====================================================================

CREATE SEQUENCE SEQ_DEPARTMENT START WITH 10 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_BATCH     START WITH 1  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_COMPANY   START WITH 101 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_SKILL     START WITH 1  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_ALUMNI    START WITH 1  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_EVENT     START WITH 1  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_DONATION  START WITH 1  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_JOB       START WITH 1  INCREMENT BY 1 NOCACHE;

CREATE OR REPLACE TRIGGER TRG_DEPARTMENT_BI BEFORE INSERT ON DEPARTMENT FOR EACH ROW
BEGIN :NEW.DeptID := NVL(:NEW.DeptID, SEQ_DEPARTMENT.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_BATCH_BI BEFORE INSERT ON BATCH FOR EACH ROW
BEGIN :NEW.BatchID := NVL(:NEW.BatchID, SEQ_BATCH.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_COMPANY_BI BEFORE INSERT ON COMPANY FOR EACH ROW
BEGIN :NEW.CompanyID := NVL(:NEW.CompanyID, SEQ_COMPANY.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_SKILL_BI BEFORE INSERT ON SKILL FOR EACH ROW
BEGIN :NEW.SkillID := NVL(:NEW.SkillID, SEQ_SKILL.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_ALUMNI_BI BEFORE INSERT ON ALUMNI FOR EACH ROW
BEGIN :NEW.AlumniID := NVL(:NEW.AlumniID, SEQ_ALUMNI.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_EVENT_BI BEFORE INSERT ON EVENT FOR EACH ROW
BEGIN :NEW.EventID := NVL(:NEW.EventID, SEQ_EVENT.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_DONATION_BI BEFORE INSERT ON DONATION FOR EACH ROW
BEGIN :NEW.DonationID := NVL(:NEW.DonationID, SEQ_DONATION.NEXTVAL); END;
/
CREATE OR REPLACE TRIGGER TRG_JOB_BI BEFORE INSERT ON JOB FOR EACH ROW
BEGIN :NEW.JobID := NVL(:NEW.JobID, SEQ_JOB.NEXTVAL); END;
/

-- ====================================================================
-- SECTION B: BUSINESS-RULE TRIGGERS
-- ====================================================================

-- MentorshipID is a partial key: auto-generate M1, M2 ... per ALUMNI
CREATE OR REPLACE TRIGGER TRG_MNT_PARTIAL_KEY
BEFORE INSERT ON MENTORSHIP
FOR EACH ROW
DECLARE
    v_next NUMBER;
BEGIN
    IF :NEW.MentorshipID IS NULL THEN
        SELECT NVL(MAX(TO_NUMBER(REGEXP_SUBSTR(MentorshipID, '\d+'))), 0) + 1
          INTO v_next
          FROM MENTORSHIP
         WHERE AlumniID = :NEW.AlumniID;
        :NEW.MentorshipID := 'M' || v_next;
    END IF;
END;
/

-- An alumni may store at most 3 phone numbers (ER cardinaity rule)
CREATE OR REPLACE TRIGGER TRG_APHONE_MAX3
BEFORE INSERT ON ALUMNI_PHONE
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
      FROM ALUMNI_PHONE
     WHERE AlumniID = :NEW.AlumniID;
    IF v_count >= 3 THEN
        RAISE_APPLICATION_ERROR(-20001,
            'An alumni can register at most 3 phone numbers.');
    END IF;
END;
/

-- Keep MENTORSHIP.Status consistent with EndDate
CREATE OR REPLACE TRIGGER TRG_MNT_STATUS_SYNC
BEFORE UPDATE OF EndDate ON MENTORSHIP
FOR EACH ROW
BEGIN
    IF :NEW.EndDate IS NOT NULL THEN
        :NEW.Status := 'Completed';
    END IF;
END;
/

-- ====================================================================
-- SECTION C: VIEWS
-- ====================================================================

CREATE OR REPLACE VIEW VW_ALUMNI_DIRECTORY AS
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS FullName,
       a.Email,
       a.CurrentPosition,
       c.CompanyName,
       d.DeptName,
       b.BatchYear,
       a.IsActive
FROM ALUMNI a
LEFT JOIN COMPANY    c ON a.CompanyID = c.CompanyID
LEFT JOIN DEPARTMENT d ON a.DeptID    = d.DeptID
LEFT JOIN BATCH      b ON a.BatchID   = b.BatchID;

CREATE OR REPLACE VIEW VW_MENTORSHIP_SUMMARY AS
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
JOIN ALUMNI  al ON m.AlumniID  = al.AlumniID
JOIN STUDENT s  ON m.StudentID = s.StudentID;

CREATE OR REPLACE VIEW VW_EVENT_ATTENDANCE AS
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

CREATE OR REPLACE VIEW VW_DONATION_TOTALS AS
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS DonorName,
       COUNT(d.DonationID)  AS DonationCount,
       NVL(SUM(d.Amount), 0) AS TotalAmount
FROM ALUMNI a
LEFT JOIN DONATION d ON d.DonorID = a.AlumniID
GROUP BY a.AlumniID, a.FirstName, a.LastName;

-- ====================================================================
-- SECTION D: FUNCTIONS
-- ====================================================================

CREATE OR REPLACE FUNCTION FN_TOTAL_DONATION(p_AlumniID IN NUMBER)
RETURN NUMBER IS
    v_total NUMBER := 0;
BEGIN
    SELECT NVL(SUM(Amount), 0) INTO v_total
      FROM DONATION
     WHERE DonorID = p_AlumniID;
    RETURN v_total;
END;
/

CREATE OR REPLACE FUNCTION FN_ALUMNI_SKILL_COUNT(p_AlumniID IN NUMBER)
RETURN NUMBER IS
    v_count NUMBER := 0;
BEGIN
    SELECT COUNT(*) INTO v_count
      FROM ALUMNI_SKILL
     WHERE AlumniID = p_AlumniID;
    RETURN v_count;
END;
/

-- ====================================================================
-- SECTION E: STORED PROCEDURES
-- ====================================================================

-- Register an alumni for an event (idempotent)
CREATE OR REPLACE PROCEDURE PR_REGISTER_ALUMNI_EVENT(
    p_AlumniID IN ALUMNI_EVENT.AlumniID%TYPE,
    p_EventID  IN ALUMNI_EVENT.EventID%TYPE
) IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
      FROM ALUMNI_EVENT
     WHERE AlumniID = p_AlumniID AND EventID = p_EventID;
    IF v_count = 0 THEN
        INSERT INTO ALUMNI_EVENT (AlumniID, EventID) VALUES (p_AlumniID, p_EventID);
        DBMS_OUTPUT.PUT_LINE('Alumni ' || p_AlumniID || ' registered for event ' || p_EventID);
    ELSE
        DBMS_OUTPUT.PUT_LINE('Already registered.');
    END IF;
END;
/

-- Attach a skill to an alumni (idempotent)
CREATE OR REPLACE PROCEDURE PR_ADD_SKILL_TO_ALUMNI(
    p_AlumniID IN ALUMNI_SKILL.AlumniID%TYPE,
    p_SkillID  IN ALUMNI_SKILL.SkillID%TYPE
) IS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
      FROM ALUMNI_SKILL
     WHERE AlumniID = p_AlumniID AND SkillID = p_SkillID;
    IF v_count = 0 THEN
        INSERT INTO ALUMNI_SKILL (AlumniID, SkillID) VALUES (p_AlumniID, p_SkillID);
        DBMS_OUTPUT.PUT_LINE('Skill ' || p_SkillID || ' added to alumni ' || p_AlumniID);
    ELSE
        DBMS_OUTPUT.PUT_LINE('Skill already linked.');
    END IF;
END;
/

-- Start a mentorship owned by an alumni (partial key auto-assigned by trigger)
CREATE OR REPLACE PROCEDURE PR_START_MENTORSHIP(
    p_AlumniID     IN MENTORSHIP.AlumniID%TYPE,
    p_StudentID    IN MENTORSHIP.StudentID%TYPE,
    p_Area         IN MENTORSHIP.MentorshipArea%TYPE,
    p_Goals        IN MENTORSHIP.Goals%TYPE,
    p_MentorshipID OUT MENTORSHIP.MentorshipID%TYPE
) IS
BEGIN
    INSERT INTO MENTORSHIP (AlumniID, StudentID, StartDate, Status, MentorshipArea, Goals)
    VALUES (p_AlumniID, p_StudentID, SYSDATE, 'Active', p_Area, p_Goals)
    RETURNING MentorshipID INTO p_MentorshipID;
END;
/

-- ====================================================================
-- SECTION F: PACKAGE PKG_ALUMNI_REPORTS
-- ====================================================================
CREATE OR REPLACE PACKAGE PKG_ALUMNI_REPORTS AS
    PROCEDURE PR_TOP_DONORS(p_TopN IN NUMBER DEFAULT 5);
    PROCEDURE PR_ALUMNI_PROFILE(p_AlumniID IN NUMBER);
END PKG_ALUMNI_REPORTS;
/

CREATE OR REPLACE PACKAGE BODY PKG_ALUMNI_REPORTS AS

    PROCEDURE PR_TOP_DONORS(p_TopN IN NUMBER DEFAULT 5) IS
    BEGIN
        DBMS_OUTPUT.PUT_LINE(RPAD('DONOR', 25) || LPAD('DONATIONS', 10) || LPAD('TOTAL', 14));
        DBMS_OUTPUT.PUT_LINE(RPAD('-', 25, '-') || LPAD('-', 10, '-') || LPAD('-', 14, '-'));
        FOR r IN (SELECT DonorName, DonationCount, TotalAmount
                    FROM (SELECT * FROM VW_DONATION_TOTALS
                           ORDER BY TotalAmount DESC)
                   WHERE ROWNUM <= p_TopN) LOOP
            DBMS_OUTPUT.PUT_LINE(RPAD(r.DonorName, 25) ||
                                 LPAD(r.DonationCount, 10) ||
                                 LPAD(TO_CHAR(r.TotalAmount, 'FM999,999,999'), 14));
        END LOOP;
    END;

    PROCEDURE PR_ALUMNI_PROFILE(p_AlumniID IN NUMBER) IS
        r VW_ALUMNI_DIRECTORY%ROWTYPE;
    BEGIN
        SELECT * INTO r FROM VW_ALUMNI_DIRECTORY WHERE AlumniID = p_AlumniID;
        DBMS_OUTPUT.PUT_LINE('Alumni   : ' || r.FullName);
        DBMS_OUTPUT.PUT_LINE('Email    : ' || r.Email);
        DBMS_OUTPUT.PUT_LINE('Position : ' || NVL(r.CurrentPosition, '-'));
        DBMS_OUTPUT.PUT_LINE('Company  : ' || NVL(r.CompanyName, '-'));
        DBMS_OUTPUT.PUT_LINE('Dept     : ' || NVL(r.DeptName, '-') ||
                             '  Batch: ' || NVL(TO_CHAR(r.BatchYear), '-'));
        DBMS_OUTPUT.PUT_LINE('Skills   : ' || FN_ALUMNI_SKILL_COUNT(p_AlumniID));
        DBMS_OUTPUT.PUT_LINE('Donated  : Rs. ' ||
                             TO_CHAR(FN_TOTAL_DONATION(p_AlumniID), 'FM999,999,999'));
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('No alumni found with ID ' || p_AlumniID);
    END;

END PKG_ALUMNI_REPORTS;
/
