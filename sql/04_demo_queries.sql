-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Part 4: Demonstration queries for the 14-relation schema
-- ====================================================================
SET PAGESIZE 100 LINESIZE 200

PROMPT === Q1: Alumni directory with department and company ===
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS FullName,
       d.DeptName,
       b.BatchYear,
       c.CompanyName,
       a.CurrentPosition
FROM ALUMNI a
LEFT JOIN DEPARTMENT d ON a.DeptID = d.DeptID
LEFT JOIN BATCH      b ON a.BatchID = b.BatchID
LEFT JOIN COMPANY    c ON a.CompanyID = c.CompanyID
ORDER BY a.AlumniID;

PROMPT === Q2: Contact numbers of each alumni (multivalued) ===
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS FullName,
       p.PhoneNumber
FROM ALUMNI a
JOIN ALUMNI_PHONE p ON a.AlumniID = p.AlumniID
ORDER BY a.AlumniID, p.PhoneNumber;

PROMPT === Q3: Mentorship pairs (weak entity owned by ALUMNI) ===
SELECT m.AlumniID,
       al.FirstName || ' ' || al.LastName AS MentorName,
       m.MentorshipID,
       s.StudentID,
       s.FirstName || ' ' || s.LastName AS StudentName,
       m.MentorshipArea,
       m.Status
FROM MENTORSHIP m
JOIN ALUMNI  al ON m.AlumniID  = al.AlumniID
JOIN STUDENT s  ON m.StudentID = s.StudentID
ORDER BY m.AlumniID, m.MentorshipID;

PROMPT === Q4: Donations above the average donation ===
SELECT dn.DonationID,
       a.FirstName || ' ' || a.LastName AS Donor,
       dn.Amount,
       dn.PaymentMethod
FROM DONATION dn
JOIN ALUMNI a ON dn.DonorID = a.AlumniID
WHERE dn.Amount > (SELECT AVG(Amount) FROM DONATION)
ORDER BY dn.Amount DESC;

PROMPT === Q5: Event attendance counts (M:N via ALUMNI_EVENT) ===
SELECT e.EventName, e.EventType, e.EventDate, e.Venue,
       COUNT(ae.AlumniID) AS Attendees
FROM EVENT e
LEFT JOIN ALUMNI_EVENT ae ON e.EventID = ae.EventID
GROUP BY e.EventName, e.EventType, e.EventDate, e.Venue
ORDER BY e.EventDate;

PROMPT === Q6: Jobs posted by alumni at companies ===
SELECT j.JobTitle, c.CompanyName, j.JobType, j.Salary,
       a.FirstName || ' ' || a.LastName AS PostedBy
FROM JOB j
JOIN COMPANY c ON j.CompanyID = c.CompanyID
JOIN ALUMNI  a ON j.PostedBy  = a.AlumniID
ORDER BY c.CompanyName;

PROMPT === Q7: Total donations per donor (aggregation view available too) ===
SELECT a.AlumniID,
       a.FirstName || ' ' || a.LastName AS Donor,
       COUNT(*) AS Donations,
       SUM(dn.Amount) AS TotalAmount
FROM DONATION dn
JOIN ALUMNI a ON dn.DonorID = a.AlumniID
GROUP BY a.AlumniID, a.FirstName, a.LastName
ORDER BY TotalAmount DESC;

PROMPT === Q8: Skills of each alumni (M:N via ALUMNI_SKILL) ===
SELECT a.FirstName || ' ' || a.LastName AS Alumni,
       s.SkillName,
       s.SkillCategory
FROM ALUMNI_SKILL ask
JOIN ALUMNI a ON ask.AlumniID = a.AlumniID
JOIN SKILL  s ON ask.SkillID  = s.SkillID
ORDER BY 1;

PROMPT === Q9: Students with their multiple emails (multivalued) ===
SELECT st.StudentID,
       st.FirstName || ' ' || st.LastName AS StudentName,
       se.Email,
       st.CGPA
FROM STUDENT st
LEFT JOIN STUDENT_EMAIL se ON st.StudentID = se.StudentID
ORDER BY st.StudentID, se.Email;

PROMPT === Q10: Using the PL/SQL views built in Part 2 ===
SELECT * FROM VW_EVENT_ATTENDANCE;
SELECT * FROM VW_DONATION_TOTALS ORDER BY TotalAmount DESC;
