-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Part 3: Sample Data (DML)
-- Prerequisite: 01_schema.sql and 02_plsql.sql on a FRESH schema.
-- IDs follow the DA1 report: AlumniID 1-5, CompanyID 101-105,
-- DeptID 10-14, StudentID S1001-S1005.
-- ====================================================================
SET FEEDBACK ON

-- --------------------------------------------------------------------
-- 1. DEPARTMENT (DeptIDs fixed as per ER model data)
-- --------------------------------------------------------------------
INSERT INTO DEPARTMENT VALUES (10, 'Computer Science and Engineering', 'CSE',   'Dr. Meera Krishnan', 1985);
INSERT INTO DEPARTMENT VALUES (11, 'Information Technology',           'IT',    'Dr. Rajesh Iyer',    1992);
INSERT INTO DEPARTMENT VALUES (12, 'Electronics and Communication',    'ECE',   'Dr. Kavya Menon',    1988);
INSERT INTO DEPARTMENT VALUES (13, 'Mechanical Engineering',           'MECH',  'Dr. Suresh Babu',    1980);
INSERT INTO DEPARTMENT VALUES (14, 'Business Administration',          'MBA',   'Dr. Anita Desai',    1995);

-- --------------------------------------------------------------------
-- 2. BATCH
-- --------------------------------------------------------------------
INSERT INTO BATCH VALUES (1, 2019, 'A', 60, 10);
INSERT INTO BATCH VALUES (2, 2020, 'A', 55, 10);
INSERT INTO BATCH VALUES (3, 2020, 'B', 58, 11);
INSERT INTO BATCH VALUES (4, 2021, 'A', 62, 12);
INSERT INTO BATCH VALUES (5, 2022, 'A', 50, 14);

-- --------------------------------------------------------------------
-- 3. COMPANY (CompanyIDs 101-105 as per DA1)
-- --------------------------------------------------------------------
INSERT INTO COMPANY VALUES (101, 'TCS',                 'IT Services',        '1000+', 'https://www.tcs.com',      'Mumbai');
INSERT INTO COMPANY VALUES (102, 'Infosys',             'IT Services',        '1000+', 'https://www.infosys.com',  'Bengaluru');
INSERT INTO COMPANY VALUES (103, 'Google',              'Technology',         '1000+', 'https://www.google.com',   'Mountain View');
INSERT INTO COMPANY VALUES (104, 'Reliance Industries', 'Conglomerate',       '1000+', 'https://www.ril.com',      'Mumbai');
INSERT INTO COMPANY VALUES (105, 'Zoho Corporation',    'Software Products',  '201-1000', 'https://www.zoho.com',  'Chennai');

-- --------------------------------------------------------------------
-- 4. SKILL (SkillIDs Sk1-Sk8 -> numeric 1-8)
-- --------------------------------------------------------------------
INSERT INTO SKILL VALUES (1, 'Python',           'Programming',  'General-purpose programming language');
INSERT INTO SKILL VALUES (2, 'Java',             'Programming',  'Object-oriented programming language');
INSERT INTO SKILL VALUES (3, 'SQL',              'Database',     'Structured Query Language');
INSERT INTO SKILL VALUES (4, 'Web Development',  'Software',     'Front-end and back-end development');
INSERT INTO SKILL VALUES (5, 'Machine Learning', 'AI/ML',        'Statistical learning algorithms');
INSERT INTO SKILL VALUES (6, 'Cloud Computing',  'Infrastructure','AWS / Azure / GCP platforms');
INSERT INTO SKILL VALUES (7, 'Public Speaking',  'Soft Skill',   'Effective presentation skills');
INSERT INTO SKILL VALUES (8, 'Data Analysis',    'Analytics',    'Exploratory data analysis and visualisation');

-- --------------------------------------------------------------------
-- 5. ALUMNI (AlumniIDs 1-5 as per DA1)
-- --------------------------------------------------------------------
INSERT INTO ALUMNI VALUES (1, 'Aarav',  'Mehta',  'aarav.mehta@gmail.com',  DATE '1997-05-12',
    'Chennai, Tamil Nadu',    10, 1, 101, 'Systems Engineer',      'linkedin.com/in/aaravmehta',  1);
INSERT INTO ALUMNI VALUES (2, 'Priya',  'Nair',   'priya.nair@gmail.com',   DATE '1998-09-25',
    'Bengaluru, Karnataka',   10, 2, 102, 'Software Engineer',     'linkedin.com/in/priyanair',   1);
INSERT INTO ALUMNI VALUES (3, 'Rohan',  'Gupta',  'rohan.gupta@gmail.com',  DATE '1997-01-30',
    'Hyderabad, Telangana',   11, 3, 103, 'Data Scientist',        'linkedin.com/in/rohangupta',  1);
INSERT INTO ALUMNI VALUES (4, 'Sneha',  'Iyer',   'sneha.iyer@gmail.com',   DATE '1999-03-18',
    'Chennai, Tamil Nadu',    12, 4, 104, 'Business Analyst',      'linkedin.com/in/snehaiyer',   1);
INSERT INTO ALUMNI VALUES (5, 'Vikram', 'Singh',  'vikram.singh@gmail.com', DATE '1998-11-08',
    'Coimbatore, Tamil Nadu', 14, 5, 105, 'Product Manager',       'linkedin.com/in/vikramsingh', 1);

-- --------------------------------------------------------------------
-- 6. ALUMNI_PHONE (multivalued attribute)
-- --------------------------------------------------------------------
INSERT INTO ALUMNI_PHONE VALUES (1, '9876543210');
INSERT INTO ALUMNI_PHONE VALUES (1, '9876500011');
INSERT INTO ALUMNI_PHONE VALUES (2, '9123456780');
INSERT INTO ALUMNI_PHONE VALUES (3, '9988776655');
INSERT INTO ALUMNI_PHONE VALUES (4, '9090909090');
INSERT INTO ALUMNI_PHONE VALUES (5, '9843012345');

-- --------------------------------------------------------------------
-- 7. STUDENT (StudentIDs S1001-S1005)
-- --------------------------------------------------------------------
INSERT INTO STUDENT VALUES ('S1001', 'Kiran',   'Raj',    10, 2, 2023, 5, 8.75);
INSERT INTO STUDENT VALUES ('S1002', 'Divya',   'Sharma', 10, 2, 2023, 5, 9.10);
INSERT INTO STUDENT VALUES ('S1003', 'Arjun',   'Kamath', 11, 3, 2022, 7, 8.20);
INSERT INTO STUDENT VALUES ('S1004', 'Nithya',  'Ravi',   12, 4, 2022, 7, 8.95);
INSERT INTO STUDENT VALUES ('S1005', 'Mohammed','Asif',   14, 5, 2023, 4, 8.50);

-- --------------------------------------------------------------------
-- 8. STUDENT_EMAIL (multivalued attribute)
-- --------------------------------------------------------------------
INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiran.raj@student.edu');
INSERT INTO STUDENT_EMAIL VALUES ('S1001', 'kiranraj@gmail.com');
INSERT INTO STUDENT_EMAIL VALUES ('S1002', 'divya.sharma@student.edu');
INSERT INTO STUDENT_EMAIL VALUES ('S1003', 'arjun.kamath@student.edu');
INSERT INTO STUDENT_EMAIL VALUES ('S1004', 'nithya.ravi@student.edu');
INSERT INTO STUDENT_EMAIL VALUES ('S1005', 'mohammed.asif@student.edu');

-- --------------------------------------------------------------------
-- 9. MENTORSHIP (weak entity of ALUMNI; composite key AlumniID + MentorshipID)
-- --------------------------------------------------------------------
INSERT INTO MENTORSHIP VALUES (1, 'M1', 'S1001', DATE '2024-06-01', NULL, 'Active',
    'Data Science', 'Build ML fundamentals and a capstone project');
INSERT INTO MENTORSHIP VALUES (1, 'M2', 'S1002', DATE '2024-08-15', DATE '2025-02-15', 'Completed',
    'Career Guidance', 'Internship preparation and resume review');
INSERT INTO MENTORSHIP VALUES (2, 'M3', 'S1003', DATE '2024-07-10', NULL, 'Active',
    'Web Development', 'Full-stack project mentoring');
INSERT INTO MENTORSHIP VALUES (3, 'M4', 'S1004', DATE '2025-01-05', NULL, 'Active',
    'Research', 'Publish a conference paper on IoT');

-- --------------------------------------------------------------------
-- 10. EVENT (organized by alumni -> 1:N)
-- --------------------------------------------------------------------
INSERT INTO EVENT VALUES (1, 'Annual Tech Reunion 2024',  'Reunion',  DATE '2024-12-21', 'VIT Chennai Auditorium', 1);
INSERT INTO EVENT VALUES (2, 'AI in Industry Workshop',   'Workshop', DATE '2025-03-14', 'CSE Lab Complex',        2);
INSERT INTO EVENT VALUES (3, 'Alumni Career Fair',        'Seminar',  DATE '2025-08-02', 'Main Grounds',           3);
INSERT INTO EVENT VALUES (4, 'Entrepreneurship Talk',     'Seminar',  DATE '2025-09-20', 'MBA Block Seminar Hall', 5);

-- --------------------------------------------------------------------
-- 11. DONATION (made by alumni donors)
-- --------------------------------------------------------------------
INSERT INTO DONATION VALUES (1, 50000,  DATE '2024-03-15', 'Online', 1);
INSERT INTO DONATION VALUES (2, 75000,  DATE '2024-01-10', 'Check',  2);
INSERT INTO DONATION VALUES (3, 25000,  DATE '2024-07-22', 'UPI',    3);
INSERT INTO DONATION VALUES (4, 40000,  DATE '2025-02-18', 'DD',     4);
INSERT INTO DONATION VALUES (5, 60000,  DATE '2025-06-30', 'Check',  5);

-- --------------------------------------------------------------------
-- 12. JOB (posted by alumni at companies)
-- --------------------------------------------------------------------
INSERT INTO JOB VALUES (1, 'Software Engineer Trainee', 'Full-Time', 'Rs. 6-8 LPA',  101, 1);
INSERT INTO JOB VALUES (2, 'Systems Engineer',          'Full-Time', 'Rs. 7-9 LPA',  101, 2);
INSERT INTO JOB VALUES (3, 'Data Analyst Intern',       'Internship','Rs. 30k/month',103, 3);
INSERT INTO JOB VALUES (4, 'Business Analyst',          'Full-Time', 'Rs. 12-18 LPA',102, 4);
INSERT INTO JOB VALUES (5, 'Product Management Intern', 'Internship','Rs. 45k/month',105, 5);

-- --------------------------------------------------------------------
-- 13. ALUMNI_SKILL (M:N)
-- --------------------------------------------------------------------
INSERT INTO ALUMNI_SKILL VALUES (1, 1);
INSERT INTO ALUMNI_SKILL VALUES (1, 3);
INSERT INTO ALUMNI_SKILL VALUES (1, 4);
INSERT INTO ALUMNI_SKILL VALUES (2, 2);
INSERT INTO ALUMNI_SKILL VALUES (2, 4);
INSERT INTO ALUMNI_SKILL VALUES (3, 1);
INSERT INTO ALUMNI_SKILL VALUES (3, 5);
INSERT INTO ALUMNI_SKILL VALUES (3, 8);
INSERT INTO ALUMNI_SKILL VALUES (4, 7);
INSERT INTO ALUMNI_SKILL VALUES (4, 8);
INSERT INTO ALUMNI_SKILL VALUES (5, 6);
INSERT INTO ALUMNI_SKILL VALUES (5, 7);

-- --------------------------------------------------------------------
-- 14. ALUMNI_EVENT (M:N attendance)
-- --------------------------------------------------------------------
INSERT INTO ALUMNI_EVENT VALUES (1, 1);
INSERT INTO ALUMNI_EVENT VALUES (2, 1);
INSERT INTO ALUMNI_EVENT VALUES (3, 1);
INSERT INTO ALUMNI_EVENT VALUES (1, 2);
INSERT INTO ALUMNI_EVENT VALUES (2, 2);
INSERT INTO ALUMNI_EVENT VALUES (3, 3);
INSERT INTO ALUMNI_EVENT VALUES (4, 3);
INSERT INTO ALUMNI_EVENT VALUES (5, 4);

COMMIT;
