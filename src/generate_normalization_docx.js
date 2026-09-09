const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat
} = require("docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };
const accentColor = "1A3C5E";
const secondaryColor = "2E6B9E";
const lightBg = "EAF2FA";
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function hdrCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: accentColor, type: ShadingType.CLEAR }, margins: cellMargins,
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, bold: true, color: "FFFFFF", font: "Calibri", size: 20 })] })]
  });
}
function cell(text, width, shaded = false) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: shaded ? { fill: lightBg, type: ShadingType.CLEAR } : undefined, margins: cellMargins,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), font: "Calibri", size: 20 })] })]
  });
}
function makeTable(headers, rows, colWidths) {
  const totalWidth = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA }, columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => hdrCell(h, colWidths[i])) }),
      ...rows.map((row, ri) => new TableRow({ children: row.map((c, ci) => cell(c, colWidths[ci], ri % 2 === 0)) }))
    ]
  });
}
function heading(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 300, after: 150 }, children: [new TextRun({ text, font: "Calibri" })] });
}
function para(text) {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, font: "Calibri", size: 22 })] });
}
function boldPara(text) {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, font: "Calibri", size: 22, bold: true, color: "2C5F2D" })] });
}
function bullet(text) {
  return new Paragraph({ spacing: { after: 80 }, numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text, font: "Calibri", size: 22 })] });
}
function codePara(text) {
  return new Paragraph({ spacing: { after: 80 }, shading: { fill: "F5F5F5", type: ShadingType.CLEAR }, children: [new TextRun({ text, font: "Consolas", size: 18 })] });
}
function blankPara() { return new Paragraph({ children: [] }); }

async function main() {
  const doc = new Document({
    numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
    styles: {
      default: { document: { run: { font: "Calibri", size: 22 } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 36, bold: true, font: "Calibri", color: accentColor }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 30, bold: true, font: "Calibri", color: secondaryColor }, paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Calibri", color: "333333" }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
      ]
    },
    sections: [
      // TITLE PAGE
      {
        properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
        children: [
          new Paragraph({ spacing: { before: 2000 }, children: [] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: "Vellore Institute of Technology", font: "Calibri", size: 32, bold: true, color: "8B0000" })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: "School of Computer Science and Engineering", font: "Calibri", size: 24, color: "555555" })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "Course: Database Management Systems (CSE2005)", font: "Calibri", size: 22, color: "555555" })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: secondaryColor, space: 1 } }, children: [new TextRun({ text: "Faculty: Dr. [Faculty Name]  |  Slot: [Slot]", font: "Calibri", size: 22, color: "555555" })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "NORMALIZATION REPORT", font: "Calibri", size: 52, bold: true, color: accentColor })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: "Alumni Network and Engagement Platform", font: "Calibri", size: 28, color: secondaryColor })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "Detailed table-by-table normalization analysis from 1NF to BCNF", font: "Calibri", size: 22, color: "777777", italics: true })] }),
          new Paragraph({ spacing: { before: 400 }, children: [] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "Submitted by:", font: "Calibri", size: 24, bold: true, color: accentColor })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Sagarika Kaistha  \u2014  25BCE5091", font: "Calibri", size: 22 })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Praveen G  \u2014  25BCE5092", font: "Calibri", size: 22 })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Daksh Agarwal  \u2014  25BCE5098", font: "Calibri", size: 22 })] }),
          new Paragraph({ spacing: { before: 300 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Date of Submission: 31-07-2026", font: "Calibri", size: 22, italics: true, color: "888888" })] }),
        ]
      },
      // BODY
      {
        properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
        headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Normalization Report \u2014 Alumni Network", font: "Calibri", size: 18, italics: true, color: "888888" })] })] }) },
        footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: "Calibri", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 18 })] })] }) },
        children: [
          // 1. INTRODUCTION
          heading("1. Introduction to Normalization", HeadingLevel.HEADING_1),
          para("So normalization is basically the process of organizing data in a database to reduce redundancy and avoid problems like update, insertion, and deletion anomalies. We learned about this in our DBMS course and applied it to our Alumni Network project."),
          para("The main idea is: instead of storing everything in one giant table, we split the data into smaller, logical tables and connect them using foreign keys. This way, each piece of data is stored only once, and if something changes, we only need to update it in one place."),
          blankPara(),
          heading("1.1 Normal Forms Hierarchy", HeadingLevel.HEADING_2),
          makeTable(["Normal Form", "Requirement", "Eliminates"], [
            ["1NF", "All attributes atomic, no repeating groups", "Multi-valued attributes"],
            ["2NF", "1NF + No partial dependencies", "Partial dependencies on composite keys"],
            ["3NF", "2NF + No transitive dependencies", "Transitive dependencies"],
            ["BCNF", "3NF + Every determinant is a candidate key", "Remaining anomalies"],
          ], [1800, 3800, 3760]),
          blankPara(),
          para("We checked all our tables against each of these normal forms. Let\u2019s go through them one by one."),
          new Paragraph({ children: [new PageBreak()] }),

          // 2. TABLE-BY-TABLE ANALYSIS
          heading("2. Table-by-Table Normalization Analysis", HeadingLevel.HEADING_1),

          // DEPARTMENT
          heading("2.1 DEPARTMENT", HeadingLevel.HEADING_2),
          para("The DEPARTMENT table stores academic departments like CSE, ECE, MECH, etc."),
          para("Candidate Keys: DeptID, DeptName, DeptCode"),
          codePara("DeptID \u2192 DeptName, DeptCode, HODPersonID, EstablishedYear"),
          codePara("DeptName \u2192 DeptID, DeptCode, HODPersonID, EstablishedYear"),
          codePara("DeptCode \u2192 DeptID, DeptName, HODPersonID, EstablishedYear"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic \u2014 no multi-valued or composite attributes"],
            ["2NF", "\u2713 Pass", "Single attribute PK (DeptID), so partial dependencies are impossible"],
            ["3NF", "\u2713 Pass", "No transitive dependencies; HODPersonID is FK to PERSON table"],
            ["BCNF", "\u2713 Pass", "Every determinant (DeptID, DeptName, DeptCode) is a candidate key"],
          ], [1200, 1200, 6960]),
          blankPara(),
          para("V2 Change: In V1, we had HODName as a plain text column, which created a transitive dependency (DeptID \u2192 HODPersonID \u2192 HODName). In V2, we replaced it with HODPersonID FK to the PERSON table."),
          boldPara("Result: DEPARTMENT is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // BATCH
          heading("2.2 BATCH", HeadingLevel.HEADING_2),
          para("The BATCH table stores batch information like 2025 Batch, Section A, etc."),
          para("Candidate Keys: BatchID"),
          codePara("BatchID \u2192 BatchYear, Section, TotalStudents, DeptID"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies possible"],
            ["3NF", "\u2713 Pass", "All non-key attributes depend directly on BatchID; DeptID is FK reference"],
            ["BCNF", "\u2713 Pass", "Every determinant (BatchID) is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: BATCH is in BCNF \u2713"),
          blankPara(),

          // COMPANY
          heading("2.3 COMPANY", HeadingLevel.HEADING_2),
          para("The COMPANY table stores information about companies where alumni work."),
          para("Candidate Keys: CompanyID"),
          codePara("CompanyID \u2192 CompanyName, Industry, SizeID, Website, Headquarters, FoundedYear"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies; SizeID is FK to COMPANY_SIZE lookup table"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          blankPara(),
          para("V2 Change: CompanySize was stored as a string with repeating values like \u2018Small\u2019, \u2018Medium\u2019, \u2018Large\u2019. In V2, we extracted it to a COMPANY_SIZE lookup table to maintain consistency and reduce redundancy."),
          boldPara("Result: COMPANY is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // SKILL
          heading("2.4 SKILL", HeadingLevel.HEADING_2),
          para("The SKILL table stores different skills that alumni can have."),
          para("Candidate Keys: SkillID, SkillName"),
          codePara("SkillID \u2192 SkillName, SkillCategory, Description"),
          codePara("SkillName \u2192 SkillID, SkillCategory, Description"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Every determinant (SkillID, SkillName) is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: SKILL is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // PERSON
          heading("2.5 PERSON (Supertype)", HeadingLevel.HEADING_2),
          para("The PERSON table is the supertype in our EER generalization hierarchy. It stores common attributes shared by ALUMNI and STUDENT."),
          para("Candidate Keys: PersonID, Email"),
          codePara("PersonID \u2192 FirstName, LastName, Email, Phone, DateOfBirth, Gender, Address, ProfilePicture, CreatedAt"),
          codePara("Email \u2192 PersonID, FirstName, LastName, ..."),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic; Address stored as single field or decomposed in subtypes"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "All non-key attributes depend directly on PersonID"],
            ["BCNF", "\u2713 Pass", "Every determinant (PersonID, Email) is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: PERSON is in BCNF \u2713"),
          blankPara(),

          // ALUMNI
          heading("2.6 ALUMNI (Subtype of PERSON)", HeadingLevel.HEADING_2),
          para("The ALUMNI table stores alumni-specific data. It inherits from PERSON through the ISA relationship."),
          para("Candidate Keys: PersonID (inherited)"),
          codePara("PersonID \u2192 GraduationYear, DeptID, BatchID, CurrentCompanyID, CurrentPosition, LinkedInProfile, IsActive"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic after 1NF decomposition"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "FK references (DeptID, BatchID, CompanyID) are not transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          blankPara(),
          para("Normalization Steps Applied:"),
          bullet("Original (Unnormalized): Had multiple phone numbers and skills in single columns"),
          bullet("1NF: Phone numbers moved to ALUMNI_PHONE table; Skills to ALUMNI_SKILL junction table"),
          bullet("2NF, 3NF, BCNF: Already satisfied with single attribute PK"),
          boldPara("Result: ALUMNI is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // STUDENT
          heading("2.7 STUDENT (Subtype of PERSON)", HeadingLevel.HEADING_2),
          para("The STUDENT table stores student-specific data."),
          para("Candidate Keys: PersonID, StudentID, Email"),
          codePara("PersonID \u2192 StudentID, EnrollmentYear, DeptID, CurrentSemester, CGPA"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies; DeptID is FK reference"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: STUDENT is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // EVENT
          heading("2.8 EVENT", HeadingLevel.HEADING_2),
          para("The EVENT table stores alumni events like reunions, workshops, seminars, and networking events."),
          para("Candidate Keys: EventID"),
          codePara("EventID \u2192 EventName, EventTypeID, Description, EventDate, EventTime, Venue, MaxCapacity, RegistrationFee, OrganizerID"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies; EventTypeID and OrganizerID are FKs"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          blankPara(),
          para("V2 Change: EventType was stored as a VARCHAR with CHECK constraint (Reunion/Workshop/Seminar/Networking). In V2, we extracted it to EVENT_TYPE lookup table so we can easily add new event types without altering the schema."),
          boldPara("Result: EVENT is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // DONATION
          heading("2.9 DONATION", HeadingLevel.HEADING_2),
          para("The DONATION table tracks donations made by alumni."),
          para("Candidate Keys: DonationID, TransactionID, ReceiptNumber"),
          codePara("DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod, Purpose, TransactionID, IsAnonymous, ReceiptNumber"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Every determinant (DonationID, TransactionID, ReceiptNumber) is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: DONATION is in BCNF \u2713"),
          blankPara(),

          // JOB
          heading("2.10 JOB", HeadingLevel.HEADING_2),
          para("The JOB table stores job opportunities posted by alumni."),
          para("Candidate Keys: JobID"),
          codePara("JobID \u2192 JobTitle, CompanyID, PostedBy, JobType, Location, Salary, Description, Requirements, PostedDate, ExpiryDate, IsActive"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "CompanyID and PostedBy are FKs, not transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          boldPara("Result: JOB is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // MENTORSHIP
          heading("2.11 MENTORSHIP", HeadingLevel.HEADING_2),
          para("The MENTORSHIP table is interesting because it\u2019s based on the aggregation concept from the EER model. It represents a relationship between two ALUMNI entities that has its own attributes."),
          para("Candidate Keys: MentorshipID, (MentorID, MenteeID, StartDate)"),
          codePara("MentorshipID \u2192 MentorID, MenteeID, StartDate, EndDate, Status, AreaID, Goals, Feedback, Rating"),
          codePara("UNIQUE(MentorID, MenteeID, StartDate)"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All attributes are atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK; UNIQUE constraint on composite also satisfies 2NF"],
            ["3NF", "\u2713 Pass", "No transitive dependencies; AreaID is FK to MENTORSHIP_AREA"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          blankPara(),
          para("V2 Change: MentorshipArea was a free-text field in V1, which could lead to inconsistent values (like \u2018Data Science\u2019 vs \u2018data science\u2019 vs \u2018DS\u2019). In V2, we extracted it to a MENTORSHIP_AREA lookup table."),
          boldPara("Result: MENTORSHIP is in BCNF \u2713"),
          new Paragraph({ children: [new PageBreak()] }),

          // JUNCTION TABLES
          heading("2.12 Junction Tables", HeadingLevel.HEADING_2),
          para("Junction tables are used to resolve many-to-many (M:N) relationships. They have composite primary keys and are always in BCNF if designed properly."),
          blankPara(),

          heading("2.12.1 ALUMNI_SKILL", HeadingLevel.HEADING_3),
          para("Resolves M:N between ALUMNI and SKILL."),
          codePara("(AlumniID, SkillID) \u2192 ProficiencyLevel"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All values atomic"],
            ["2NF", "\u2713 Pass", "ProficiencyLevel depends on full composite key"],
            ["3NF", "\u2713 Pass", "No transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Composite PK is the only determinant"],
          ], [1200, 1200, 6960]),
          blankPara(),

          heading("2.12.2 ALUMNI_EVENT", HeadingLevel.HEADING_3),
          para("Resolves M:N between ALUMNI and EVENT (attendance)."),
          codePara("(AlumniID, EventID) \u2192 RegistrationDate"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All values atomic"],
            ["2NF", "\u2713 Pass", "RegistrationDate depends on full composite key"],
            ["3NF", "\u2713 Pass", "No transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Composite PK is the only determinant"],
          ], [1200, 1200, 6960]),
          blankPara(),

          heading("2.12.3 ALUMNI_PHONE", HeadingLevel.HEADING_3),
          para("Handles the multi-valued attribute (phone numbers) from the ER model."),
          codePara("(AlumniID, PhoneNumber) \u2192 \u2205 (no other attributes)"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All values atomic"],
            ["2NF", "\u2713 Pass", "No non-key attributes, so no partial dependencies"],
            ["3NF", "\u2713 Pass", "No non-key attributes"],
            ["BCNF", "\u2713 Pass", "Composite PK is the only determinant"],
          ], [1200, 1200, 6960]),
          blankPara(),

          heading("2.12.4 JOB_APPLICATION (V2 Addition)", HeadingLevel.HEADING_3),
          para("Added in V2 to handle the M:N relationship between JOB and ALUMNI (who applied to which job)."),
          codePara("ApplicationID \u2192 JobID, ApplicantID, ApplicationDate, Status, ResumeLink"),
          codePara("UNIQUE(JobID, ApplicantID)"),
          makeTable(["Check", "Status", "Reasoning"], [
            ["1NF", "\u2713 Pass", "All values atomic"],
            ["2NF", "\u2713 Pass", "Single attribute PK, no partial dependencies"],
            ["3NF", "\u2713 Pass", "No transitive dependencies"],
            ["BCNF", "\u2713 Pass", "Every determinant is a candidate key"],
          ], [1200, 1200, 6960]),
          new Paragraph({ children: [new PageBreak()] }),

          // 3. SUMMARY
          heading("3. Normalization Summary", HeadingLevel.HEADING_1),
          para("Here\u2019s the complete summary showing all tables and their normalization status:"),
          makeTable(
            ["Table", "1NF", "2NF", "3NF", "BCNF", "Type", "Notes"],
            [
              ["DEPARTMENT", "\u2713", "\u2713", "\u2713", "\u2713", "Core", "Multiple candidate keys"],
              ["BATCH", "\u2713", "\u2713", "\u2713", "\u2713", "Core", ""],
              ["COMPANY", "\u2713", "\u2713", "\u2713", "\u2713", "Core", "SizeID FK (v2)"],
              ["SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Core", "SkillName is candidate key"],
              ["PERSON", "\u2713", "\u2713", "\u2713", "\u2713", "Supertype", "Email is candidate key"],
              ["ALUMNI", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype", "4 FK references"],
              ["STUDENT", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype", "StudentID is candidate key"],
              ["EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "Core", "EventTypeID FK (v2)"],
              ["DONATION", "\u2713", "\u2713", "\u2713", "\u2713", "Core", "3 candidate keys"],
              ["JOB", "\u2713", "\u2713", "\u2713", "\u2713", "Core", ""],
              ["MENTORSHIP", "\u2713", "\u2713", "\u2713", "\u2713", "Aggregation", "AreaID FK (v2)"],
              ["ALUMNI_SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Junction", "M:N resolver"],
              ["ALUMNI_EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "Junction", "M:N resolver"],
              ["ALUMNI_PHONE", "\u2713", "\u2713", "\u2713", "\u2713", "Multivalued", "Multi-valued attr handler"],
              ["JOB_APPLICATION", "\u2713", "\u2713", "\u2713", "\u2713", "Junction", "New in v2"],
              ["EVENT_TYPE", "\u2713", "\u2713", "\u2713", "\u2713", "Lookup", "New in v2"],
              ["COMPANY_SIZE", "\u2713", "\u2713", "\u2713", "\u2713", "Lookup", "New in v2"],
              ["MENTORSHIP_AREA", "\u2713", "\u2713", "\u2713", "\u2713", "Lookup", "New in v2"],
            ],
            [1800, 700, 700, 700, 800, 1400, 3260]
          ),
          blankPara(),
          boldPara("All 18 tables are in BCNF. No further normalization required."),
          new Paragraph({ children: [new PageBreak()] }),

          // 4. 4NF AND 5NF
          heading("4. Fourth and Fifth Normal Forms (4NF/5NF)", HeadingLevel.HEADING_1),
          heading("4.1 Fourth Normal Form (4NF)", HeadingLevel.HEADING_2),
          para("4NF eliminates multi-valued dependencies. A multi-valued dependency X \u2192\u2192 Y exists when for each value of X, there is a set of values of Y that is independent of other attributes."),
          para("In our design, the main multi-valued dependencies were:"),
          bullet("AlumniID \u2192\u2192 Skills (an alumni can have multiple skills)"),
          bullet("AlumniID \u2192\u2192 Events (an alumni can attend multiple events)"),
          bullet("AlumniID \u2192\u2192 PhoneNumbers (an alumni can have multiple phone numbers)"),
          blankPara(),
          para("If we stored skills and events in the same ALUMNI table, we\u2019d get a Cartesian product problem \u2014 each skill would be repeated for every event and vice versa. Example:"),
          makeTable(
            ["AlumniID", "Skill", "Event"],
            [
              ["1", "Java", "Reunion2023"],
              ["1", "Java", "Workshop2024"],
              ["1", "Python", "Reunion2023"],
              ["1", "Python", "Workshop2024"],
            ],
            [2000, 3000, 4360]
          ),
          blankPara(),
          para("This creates redundant data. We solved this by decomposing into separate junction tables:"),
          bullet("ALUMNI_SKILL table handles AlumniID \u2192\u2192 Skills"),
          bullet("ALUMNI_EVENT table handles AlumniID \u2192\u2192 Events"),
          bullet("ALUMNI_PHONE table handles AlumniID \u2192\u2192 PhoneNumbers"),
          para("All tables satisfy 4NF after this decomposition."),
          blankPara(),

          heading("4.2 Fifth Normal Form (5NF)", HeadingLevel.HEADING_2),
          para("5NF deals with join dependencies. A relation is in 5NF if every join dependency is implied by its candidate keys. Basically, you can\u2019t decompose the table any further without losing data."),
          para("Consider a scenario tracking which alumni have which skills at which companies:"),
          makeTable(
            ["AlumniID", "SkillID", "CompanyID"],
            [
              ["1", "1", "101"],
              ["1", "2", "101"],
              ["2", "1", "102"],
            ],
            [2500, 3000, 3860]
          ),
          blankPara(),
          para("This creates a cyclic join dependency that cannot be decomposed without loss. In our design, we avoid this by:"),
          bullet("ALUMNI table has CompanyID (current company)"),
          bullet("ALUMNI_SKILL has skills"),
          bullet("No direct three-way relationship between Alumni-Skill-Company"),
          para("All our decompositions are lossless \u2014 natural joins reconstruct the original data without spurious tuples."),
          new Paragraph({ children: [new PageBreak()] }),

          // 5. FUNCTIONAL DEPENDENCIES SUMMARY
          heading("5. Functional Dependencies Summary", HeadingLevel.HEADING_1),
          para("Here are the key functional dependencies for our main tables:"),
          blankPara(),

          heading("5.1 ALUMNI", HeadingLevel.HEADING_2),
          codePara("PersonID \u2192 GraduationYear, DeptID, BatchID, CurrentCompanyID, CurrentPosition, LinkedInProfile, IsActive"),
          codePara("PersonID (FK to PERSON \u2192 FirstName, LastName, Email, Phone, DOB, Gender, Address)"),
          codePara("Email \u2192 PersonID (Candidate Key, inherited from PERSON)"),
          blankPara(),

          heading("5.2 DEPARTMENT", HeadingLevel.HEADING_2),
          codePara("DeptID \u2192 DeptName, DeptCode, HODPersonID, EstablishedYear"),
          codePara("DeptName \u2192 DeptID (Candidate Key)"),
          codePara("DeptCode \u2192 DeptID (Candidate Key)"),
          blankPara(),

          heading("5.3 EVENT", HeadingLevel.HEADING_2),
          codePara("EventID \u2192 EventName, EventTypeID, Description, EventDate, EventTime, Venue, MaxCapacity, RegistrationFee, OrganizerID"),
          codePara("EventTypeID \u2192 (resolved via FK to EVENT_TYPE lookup table)"),
          blankPara(),

          heading("5.4 MENTORSHIP", HeadingLevel.HEADING_2),
          codePara("MentorID, MenteeID, StartDate \u2192 EndDate, Status, AreaID, Goals, Feedback, Rating"),
          codePara("AreaID \u2192 (resolved via FK to MENTORSHIP_AREA lookup table)"),
          codePara("UNIQUE(MentorID, MenteeID, StartDate)"),
          blankPara(),

          heading("5.5 DONATION", HeadingLevel.HEADING_2),
          codePara("DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod, Purpose, TransactionID, IsAnonymous, ReceiptNumber"),
          codePara("TransactionID \u2192 DonationID (Candidate Key)"),
          codePara("ReceiptNumber \u2192 DonationID (Candidate Key)"),
          blankPara(),

          heading("5.6 JOB", HeadingLevel.HEADING_2),
          codePara("JobID \u2192 JobTitle, CompanyID, PostedBy, JobType, Location, Salary, Description, Requirements, PostedDate, ExpiryDate, IsActive"),
          blankPara(),

          heading("5.7 JOB_APPLICATION (V2)", HeadingLevel.HEADING_2),
          codePara("JobID, ApplicantID \u2192 ApplicationDate, Status, ResumeLink"),
          codePara("UNIQUE(JobID, ApplicantID)"),
          new Paragraph({ children: [new PageBreak()] }),

          // 6. DECOMPOSITION STEPS
          heading("6. Decomposition Steps", HeadingLevel.HEADING_1),
          para("Here\u2019s a summary of how we decomposed our tables during normalization:"),
          blankPara(),

          heading("6.1 Step 1: Remove Multi-valued Attributes (1NF)", HeadingLevel.HEADING_2),
          bullet("Skills \u2192 ALUMNI_SKILL junction table"),
          bullet("Events Attended \u2192 ALUMNI_EVENT junction table"),
          bullet("Phone numbers \u2192 ALUMNI_PHONE table"),
          bullet("Address \u2192 Decomposed into Address_City, Address_State, Address_PinCode"),
          blankPara(),

          heading("6.2 Step 2: Remove Partial Dependencies (2NF)", HeadingLevel.HEADING_2),
          bullet("All tables have single-attribute PKs, so 2NF is automatically satisfied"),
          bullet("Junction tables: non-key attributes depend on full composite key"),
          blankPara(),

          heading("6.3 Step 3: Remove Transitive Dependencies (3NF)", HeadingLevel.HEADING_2),
          bullet("DeptName depends on DeptID, not AlumniID \u2192 Separate DEPARTMENT table"),
          bullet("CompanyName depends on CompanyID, not AlumniID \u2192 Separate COMPANY table"),
          bullet("BatchYear depends on BatchID, not AlumniID \u2192 Separate BATCH table"),
          bullet("HODName depends on HODPersonID \u2192 FK reference (V2 fix)"),
          bullet("EventType values \u2192 EVENT_TYPE lookup table (V2 fix)"),
          bullet("CompanySize values \u2192 COMPANY_SIZE lookup table (V2 fix)"),
          bullet("MentorshipArea values \u2192 MENTORSHIP_AREA lookup table (V2 fix)"),
          blankPara(),

          heading("6.4 Step 4: Verify BCNF", HeadingLevel.HEADING_2),
          bullet("All functional dependencies have superkeys on left side"),
          bullet("No violations found after 3NF decomposition"),
          blankPara(),

          heading("6.5 Step 5: Eliminate Multi-valued Dependencies (4NF)", HeadingLevel.HEADING_2),
          bullet("Already handled by junction tables (ALUMNI_SKILL, ALUMNI_EVENT, ALUMNI_PHONE)"),
          bullet("No redundant data storage"),
          blankPara(),

          heading("6.6 Step 6: Verify Join Dependencies (5NF)", HeadingLevel.HEADING_2),
          bullet("Complex relationships decomposed without loss"),
          bullet("All joins are lossless \u2014 no spurious tuples"),
          new Paragraph({ children: [new PageBreak()] }),

          // 7. LOSSLESS JOIN AND DEPENDENCY PRESERVATION
          heading("7. Lossless Join and Dependency Preservation", HeadingLevel.HEADING_1),
          heading("7.1 Lossless Join Decomposition", HeadingLevel.HEADING_2),
          para("All decompositions performed are lossless. This means natural joins reconstruct the original data without information loss or spurious tuples."),
          para("Verification Example:"),
          codePara("Original: ALUMNI(AlumniID, FirstName, DeptID, DeptName)"),
          codePara("Decomposed:"),
          codePara("  ALUMNI(AlumniID, FirstName, DeptID)"),
          codePara("  DEPARTMENT(DeptID, DeptName)"),
          codePara("Join: ALUMNI \u22C8 DEPARTMENT = Original (Lossless \u2713)"),
          blankPara(),

          heading("7.2 Dependency Preservation", HeadingLevel.HEADING_2),
          para("All functional dependencies are preserved after decomposition:"),
          bullet("Each FD is captured in at least one decomposed relation"),
          bullet("No need to join tables to verify dependencies"),
          bullet("Constraint checking is efficient"),
          new Paragraph({ children: [new PageBreak()] }),

          // 8. ANOMALIES PREVENTED
          heading("8. Anomalies Prevented by Normalization", HeadingLevel.HEADING_1),
          heading("8.1 Update Anomaly", HeadingLevel.HEADING_2),
          para("Without normalization, if we stored DeptName in the ALUMNI table, changing a department\u2019s name would require updating hundreds of rows. With a separate DEPARTMENT table, we only update one row."),
          blankPara(),
          heading("8.2 Insertion Anomaly", HeadingLevel.HEADING_2),
          para("Without normalization, we couldn\u2019t add a new department unless an alumni from that department exists. With separate tables, departments can exist independently."),
          blankPara(),
          heading("8.3 Deletion Anomaly", HeadingLevel.HEADING_2),
          para("Without normalization, deleting the last alumni from a department would lose the department info. With separate tables, department data persists even if no alumni belong to it."),
          new Paragraph({ children: [new PageBreak()] }),

          // 9. CONCLUSION
          heading("9. Conclusion", HeadingLevel.HEADING_1),
          para("All 18 relations in our Alumni Network database are in BCNF. The normalization process has:"),
          bullet("Eliminated all redundancy through proper decomposition"),
          bullet("Prevented update, insertion, and deletion anomalies"),
          bullet("Maintained data integrity through foreign keys and constraints"),
          bullet("Ensured lossless join decomposition for all tables"),
          bullet("Preserved all functional dependencies"),
          blankPara(),
          para("The V2 refinements further improved the design by extracting lookup tables (EVENT_TYPE, COMPANY_SIZE, MENTORSHIP_AREA), replacing HODName with a proper FK reference, and adding the JOB_APPLICATION junction table."),
          new Paragraph({ children: [new PageBreak()] }),

          // 10. REFERENCES
          heading("10. References", HeadingLevel.HEADING_1),
          para("[1] Silberschatz, A., Korth, H.F., & Sudarshan, S. (2019). Database System Concepts (7th ed.). McGraw-Hill."),
          para("[2] Elmasri, R., & Navathe, S.B. (2015). Fundamentals of Database Systems (7th ed.). Pearson."),
          para("[3] Connolly, T., & Begg, C. (2014). Database Systems: A Practical Approach (6th ed.). Pearson."),
          para("[4] Date, C.J. (2003). An Introduction to Database Systems (8th ed.). Addison-Wesley."),
          para("[5] Ramakrishnan, R., & Gehrke, J. (2003). Database Management Systems (3rd ed.). McGraw-Hill."),
        ]
      }
    ]
  });

  const buffer = await Packer.toBuffer(doc);
  const outPath = "/Users/dakshagarwal/dbms-project/laguna/report/Alumni_Network_Normalization.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("Normalization DOCX generated:", outPath);
}

main().catch(console.error);
