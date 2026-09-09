const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, TableOfContents, LevelFormat
} = require("docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };
const accentColor = "1A3C5E";
const secondaryColor = "2E6B9E";
const lightBg = "EAF2FA";
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function hdrCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: accentColor, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, bold: true, color: "FFFFFF", font: "Calibri", size: 20 })] })]
  });
}

function cell(text, width, shaded = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shaded ? { fill: lightBg, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), font: "Calibri", size: 20 })] })]
  });
}

function makeTable(headers, rows, colWidths) {
  const totalWidth = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => hdrCell(h, colWidths[i])) }),
      ...rows.map((row, ri) =>
        new TableRow({ children: row.map((c, ci) => cell(c, colWidths[ci], ri % 2 === 0)) })
      )
    ]
  });
}

function heading(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 300, after: 150 }, children: [new TextRun({ text, font: "Calibri" })] });
}

function para(text) {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, font: "Calibri", size: 22 })] });
}

function bullet(text) {
  return new Paragraph({
    spacing: { after: 80 },
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, font: "Calibri", size: 22 })]
  });
}

function codePara(text) {
  return new Paragraph({
    spacing: { after: 80 },
    shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
    children: [new TextRun({ text, font: "Consolas", size: 18 })]
  });
}

function blankPara() {
  return new Paragraph({ children: [] });
}

function boldPara(text) {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, font: "Calibri", size: 22, bold: true, color: "2C5F2D" })] });
}

function codeBlock(lines) {
  return lines.map(line => new Paragraph({
    spacing: { after: 40 },
    shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
    children: [new TextRun({ text: line, font: "Consolas", size: 18 })]
  }));
}

async function main() {
  const doc = new Document({
    numbering: {
      config: [{
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }]
    },
    styles: {
      default: { document: { run: { font: "Calibri", size: 22 } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 36, bold: true, font: "Calibri", color: accentColor },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 30, bold: true, font: "Calibri", color: secondaryColor },
          paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 26, bold: true, font: "Calibri", color: "333333" },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
      ]
    },
    sections: [
      // ==================== TITLE PAGE ====================
      {
        properties: {
          page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
        },
        children: [
          new Paragraph({ spacing: { before: 2000 }, children: [] }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 100 },
            children: [new TextRun({ text: "Vellore Institute of Technology", font: "Calibri", size: 32, bold: true, color: "8B0000" })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 100 },
            children: [new TextRun({ text: "School of Computer Science and Engineering", font: "Calibri", size: 24, color: "555555" })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 60 },
            children: [new TextRun({ text: "Course: Database Management Systems (CSE2005)", font: "Calibri", size: 22, color: "555555" })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 60 },
            children: [new TextRun({ text: "Faculty: Dr. [Faculty Name]", font: "Calibri", size: 22, color: "555555" })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: secondaryColor, space: 1 } },
            children: [new TextRun({ text: "Slot: [Slot]", font: "Calibri", size: 22, color: "555555" })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 200 },
            children: [new TextRun({ text: "ALUMNI NETWORK AND", font: "Calibri", size: 52, bold: true, color: accentColor })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 200 },
            children: [new TextRun({ text: "ENGAGEMENT PLATFORM", font: "Calibri", size: 52, bold: true, color: accentColor })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 100 },
            children: [new TextRun({ text: "Database Design Assignment \u2014 DA1", font: "Calibri", size: 26, color: secondaryColor, italics: true })]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 200 },
            children: [new TextRun({ text: "ER Model | EER Model | Normalization | Relational Schema", font: "Calibri", size: 22, color: "777777", italics: true })]
          }),
          new Paragraph({ spacing: { before: 400 }, children: [] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "Submitted by:", font: "Calibri", size: 24, bold: true, color: accentColor })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Sagarika Kaistha  \u2014  25BCE5091", font: "Calibri", size: 22 })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Praveen G  \u2014  25BCE5092", font: "Calibri", size: 22 })] }),
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "Daksh Agarwal  \u2014  25BCE5098", font: "Calibri", size: 22 })] }),
          new Paragraph({ spacing: { before: 300 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Date of Submission: 31-07-2026", font: "Calibri", size: 22, italics: true, color: "888888" })] }),
        ]
      },
      // ==================== BODY ====================
      {
        properties: {
          page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
        },
        headers: {
          default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Alumni Network \u2014 DBMS DA1", font: "Calibri", size: 18, italics: true, color: "888888" })] })] })
        },
        footers: {
          default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: "Calibri", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 18 })] })] })
        },
        children: [
          // TABLE OF CONTENTS
          heading("Table of Contents", HeadingLevel.HEADING_1),
          new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 1. INTRODUCTION ====================
          heading("1. Introduction", HeadingLevel.HEADING_1),
          para("So basically, the whole idea behind this project is to build a proper database system for managing alumni information of a college. Right now, most colleges don\u2019t really have a centralized system to keep track of their passed-out students. Once someone graduates, the connection is pretty much lost. There\u2019s no easy way to find out where they\u2019re working, what they\u2019re doing, or even invite them for events."),
          para("This Alumni Network and Engagement Platform solves that problem. It stores all the details about alumni \u2014 their personal info, which department they studied in, which batch they belonged to, where they\u2019re currently working, what skills they have, and so on. On top of that, it also supports features like organizing events, tracking donations, posting job opportunities, running mentorship programs, and having discussion forums."),
          para("From a database design perspective, this project covers most of the important topics we\u2019ve studied in our DBMS course. We\u2019ve designed the ER model with all types of attributes and relationships, extended it using the EER model with generalization and specialization, normalized all the tables up to BCNF, and finally created a complete relational schema with all the constraints."),
          blankPara(),
          heading("1.1 Problem Statement", HeadingLevel.HEADING_2),
          para("Colleges produce thousands of graduates every year, but there\u2019s no proper system to maintain the connection between the institution and its alumni. This leads to several problems:"),
          bullet("No centralized database to store and retrieve alumni information"),
          bullet("Alumni can\u2019t easily connect with each other or with current students"),
          bullet("No system to organize alumni events like reunions or workshops"),
          bullet("Donation tracking is done manually, which is error-prone"),
          bullet("Current students miss out on mentorship and job opportunities from alumni"),
          bullet("No platform for alumni to share knowledge through forums or discussions"),
          blankPara(),
          heading("1.2 Objectives", HeadingLevel.HEADING_2),
          bullet("Design a comprehensive ER model with all entity types, attributes, and relationships"),
          bullet("Extend the model using EER concepts like generalization/specialization"),
          bullet("Normalize all relations up to BCNF to eliminate redundancy"),
          bullet("Create a complete relational schema with proper constraints and referential integrity"),
          bullet("Demonstrate understanding of key DBMS concepts through practical application"),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 2. ER MODEL ====================
          heading("2. Entity-Relationship Model", HeadingLevel.HEADING_1),
          para("The ER model is basically the blueprint of our database. It shows what data we\u2019re storing (entities), what properties that data has (attributes), and how different pieces of data are connected to each other (relationships). We\u2019ve tried to cover all the ER concepts taught in class."),
          blankPara(),

          heading("2.1 Types of Attributes", HeadingLevel.HEADING_2),
          para("Attributes are the properties that describe an entity. In our design, we\u2019ve used all 8 types of attributes that were covered in the syllabus. Here\u2019s a breakdown:"),
          blankPara(),

          heading("2.1.1 Simple (Atomic) Attributes", HeadingLevel.HEADING_3),
          para("These are the most basic type \u2014 they can\u2019t be broken down any further. For example, FirstName, LastName, Email, etc. are all simple attributes because they hold a single value."),
          makeTable(
            ["Attribute", "Entity", "Type"],
            [
              ["FirstName", "PERSON", "Single-valued, Simple"],
              ["Email", "PERSON", "Single-valued, Simple"],
              ["DeptName", "DEPARTMENT", "Single-valued, Simple"],
              ["CompanyName", "COMPANY", "Single-valued, Simple"],
              ["SkillName", "SKILL", "Single-valued, Simple"],
              ["JobTitle", "JOB", "Single-valued, Simple"],
            ],
            [3000, 3000, 3360]
          ),
          blankPara(),

          heading("2.1.2 Composite Attributes", HeadingLevel.HEADING_3),
          para("Composite attributes can be split into smaller sub-parts. For instance, Address can be decomposed into City, State, and PinCode. Similarly, a person\u2019s full name is made up of FirstName and LastName."),
          makeTable(
            ["Composite Attribute", "Entity", "Components"],
            [
              ["Address", "PERSON", "City, State, PinCode"],
              ["FullName", "PERSON", "FirstName, LastName"],
            ],
            [3000, 3000, 3360]
          ),
          blankPara(),

          heading("2.1.3 Multi-valued Attributes", HeadingLevel.HEADING_3),
          para("These can hold more than one value for a single entity. For example, an alumni can have multiple phone numbers (mobile, home, work) and multiple skills. In the ER diagram, these are shown as double ovals."),
          makeTable(
            ["Attribute", "Entity", "Example Values"],
            [
              ["Skills", "ALUMNI", "Java, Python, SQL, ML"],
              ["PhoneNumbers", "ALUMNI", "Mobile, Home, Work"],
            ],
            [3000, 3000, 3360]
          ),
          blankPara(),

          heading("2.1.4 Derived Attributes", HeadingLevel.HEADING_3),
          para("Derived attributes are not actually stored in the database \u2014 they\u2019re calculated from other attributes when needed. For example, Age can be derived from DateOfBirth, and YearsSinceGraduation can be calculated from the current year minus GraduationYear. This saves storage and avoids inconsistencies."),
          makeTable(
            ["Derived Attribute", "Entity", "Derived From"],
            [
              ["Age", "PERSON", "CurrentDate - DateOfBirth"],
              ["YearsSinceGraduation", "ALUMNI", "CurrentYear - GraduationYear"],
              ["TotalDonations", "ALUMNI", "SUM of Donation.Amount"],
            ],
            [3000, 3000, 3360]
          ),
          blankPara(),

          heading("2.1.5 Key and NULL Attributes", HeadingLevel.HEADING_3),
          para("Key attributes uniquely identify each entity instance \u2014 they\u2019re shown underlined in the ER diagram. NULL attributes are optional and can be left empty. For example, LinkedInProfile is optional because not every alumni might have one."),
          makeTable(
            ["Type", "Attribute", "Entity", "Description"],
            [
              ["Key", "PersonID", "PERSON", "Primary Key (underlined)"],
              ["Key", "Email", "PERSON", "Candidate Key (unique)"],
              ["NULL", "LinkedInProfile", "ALUMNI", "Optional attribute"],
              ["NULL", "EndDate", "MENTORSHIP", "NULL if still active"],
            ],
            [1800, 2400, 2400, 2760]
          ),
          new Paragraph({ children: [new PageBreak()] }),

          // 2.2 Strong Entities
          heading("2.2 Strong Entities", HeadingLevel.HEADING_2),
          para("Strong entities are the main tables in our database that can exist on their own. They have their own primary key and don\u2019t depend on any other entity for their identity. Our design has the following strong entities:"),
          makeTable(
            ["Entity", "Primary Key", "Key Attributes"],
            [
              ["PERSON", "PersonID", "FirstName, LastName, Email, Gender"],
              ["ALUMNI", "PersonID", "GraduationYear, DeptID, BatchID, CompanyID"],
              ["STUDENT", "PersonID", "StudentID, EnrollmentYear, DeptID, CGPA"],
              ["DEPARTMENT", "DeptID", "DeptName, DeptCode, HODPersonID"],
              ["BATCH", "BatchID", "BatchYear, Section, TotalStudents"],
              ["COMPANY", "CompanyID", "CompanyName, Industry, Headquarters"],
              ["SKILL", "SkillID", "SkillName, SkillCategory"],
              ["EVENT", "EventID", "EventName, EventType, Date, Venue"],
              ["DONATION", "DonationID", "DonorID, Amount, Date, PaymentMethod"],
              ["JOB", "JobID", "JobTitle, CompanyID, JobType, Salary"],
              ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, Status"],
            ],
            [2500, 2300, 4560]
          ),
          blankPara(),

          heading("2.3 Weak Entities", HeadingLevel.HEADING_2),
          para("Weak entities don\u2019t have their own primary key. They depend on an owner entity for identification. In the ER diagram, they\u2019re shown as double rectangles, and the identifying relationship is shown as a double diamond."),
          para("In our V2 design, MENTORSHIP is treated as a weak entity that depends on ALUMNI (both as mentor and mentee). It has total participation in the identifying relationship, which means every mentorship record must be linked to valid alumni."),
          bullet("Shown as double rectangle in ER diagram"),
          bullet("Has total participation in identifying relationship (double diamond)"),
          bullet("Cannot exist without the owner entity"),
          new Paragraph({ children: [new PageBreak()] }),

          // 2.4 Relationships
          heading("2.4 Relationship Types", HeadingLevel.HEADING_2),
          heading("2.4.1 Binary Relationships", HeadingLevel.HEADING_3),
          para("Binary relationships connect two different entities. Our design has quite a few of these. Here\u2019s the complete list with cardinality and participation:"),
          makeTable(
            ["Entities", "Relationship", "Cardinality", "Participation"],
            [
              ["ALUMNI - DEPARTMENT", "belongs_to", "N:1", "Total / Partial"],
              ["ALUMNI - BATCH", "belongs_to", "N:1", "Total / Partial"],
              ["ALUMNI - COMPANY", "works_at", "N:1", "Partial / Partial"],
              ["ALUMNI - SKILL", "has", "M:N", "Partial / Partial"],
              ["ALUMNI - EVENT", "attends", "M:N", "Partial / Partial"],
              ["ALUMNI - DONATION", "makes", "1:N", "Partial / Total"],
              ["ALUMNI - JOB", "posts", "1:N", "Partial / Total"],
              ["ALUMNI - EVENT", "organizes", "1:N", "Partial / Total"],
              ["JOB - COMPANY", "at", "N:1", "Total / Partial"],
            ],
            [2600, 2000, 1800, 2960]
          ),
          blankPara(),

          heading("2.4.2 Unary (Recursive) Relationships", HeadingLevel.HEADING_3),
          para("These are relationships where an entity is related to itself. The MENTORSHIP relationship is a good example \u2014 one alumni mentors another alumni. We need role names to tell apart which one is the mentor and which one is the mentee."),
          makeTable(
            ["Entity", "Relationship", "Cardinality", "Roles"],
            [
              ["ALUMNI - ALUMNI", "mentors", "1:N", "Mentor / Mentee"],
            ],
            [2600, 2000, 1800, 2960]
          ),
          blankPara(),

          heading("2.5 Participation Constraints", HeadingLevel.HEADING_2),
          heading("2.5.1 Total Participation", HeadingLevel.HEADING_3),
          para("Total participation means every instance of the entity MUST participate in the relationship. It\u2019s shown with a double line in the ER diagram. For example, every alumni must belong to a department \u2014 you can\u2019t have an alumni without a department."),
          makeTable(
            ["Relationship", "Entity", "Explanation"],
            [
              ["ALUMNI - DEPARTMENT", "ALUMNI", "Every alumnus must belong to a department"],
              ["ALUMNI - BATCH", "ALUMNI", "Every alumnus must belong to a batch"],
              ["DONATION - ALUMNI", "DONATION", "Every donation must have a donor"],
              ["JOB - ALUMNI", "JOB", "Every job must be posted by someone"],
              ["EVENT - ALUMNI", "EVENT", "Every event must have an organizer"],
            ],
            [3000, 2400, 3960]
          ),
          blankPara(),
          heading("2.5.2 Partial Participation", HeadingLevel.HEADING_3),
          para("Partial participation means not every entity instance is required to participate. For example, not all alumni have skills listed or attend events. Some may not even be currently employed."),
          makeTable(
            ["Relationship", "Entity", "Explanation"],
            [
              ["ALUMNI - SKILL", "ALUMNI", "Not all alumni have skills listed"],
              ["ALUMNI - EVENT", "ALUMNI", "Not all alumni attend events"],
              ["ALUMNI - COMPANY", "ALUMNI", "Not all alumni are currently employed"],
              ["ALUMNI - DONATION", "ALUMNI", "Not all alumni make donations"],
              ["DEPARTMENT - ALUMNI", "DEPARTMENT", "New departments may have no alumni yet"],
            ],
            [3000, 2400, 3960]
          ),
          new Paragraph({ children: [new PageBreak()] }),

          // 2.6 Cardinality
          heading("2.6 Cardinality Constraints", HeadingLevel.HEADING_2),
          para("Cardinality tells us how many instances of one entity can be associated with instances of another entity. The three main types are:"),
          makeTable(
            ["Type", "Relationship", "Description"],
            [
              ["1:N", "DEPARTMENT - ALUMNI", "One department has many alumni, but each alumni belongs to one department"],
              ["1:N", "ALUMNI - DONATION", "One alumni can make many donations, but each donation is by one alumni"],
              ["M:N", "ALUMNI - SKILL", "Many alumni can have many skills, and one skill can be shared by many alumni"],
              ["M:N", "ALUMNI - EVENT", "Many alumni can attend many events, and one event can have many attendees"],
              ["1:N", "ALUMNI - MENTORSHIP", "One alumni can have many mentorships (as mentor or mentee)"],
            ],
            [1500, 3200, 4660]
          ),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 3. EER MODEL ====================
          heading("3. Extended ER (EER) Model", HeadingLevel.HEADING_1),
          para("The Extended ER model adds more concepts on top of the basic ER model. The main additions are generalization/specialization, aggregation, and categories. These help us model real-world scenarios more accurately."),
          blankPara(),

          heading("3.1 Generalization / Specialization", HeadingLevel.HEADING_2),
          para("Generalization is a bottom-up approach where we combine similar entities into a higher-level supertype. Specialization is the opposite \u2014 top-down, where we divide a supertype into subtypes based on distinguishing characteristics."),
          para("In our design, we\u2019ve used generalization to create a PERSON supertype. ALUMNI and STUDENT are both types of PERSONs, so they share common attributes like Name, Email, Phone, etc. Rather than storing these separately, we created a PERSON table and then ALUMNI and STUDENT as subtypes that inherit from it."),
          blankPara(),

          heading("3.1.1 PERSON Supertype Hierarchy", HeadingLevel.HEADING_3),
          makeTable(
            ["Entity", "Type", "Attributes"],
            [
              ["PERSON", "Supertype", "PersonID (PK), FirstName, LastName, Email, Phone, DateOfBirth, Gender, Address"],
              ["ALUMNI", "Subtype", "PersonID (PK, FK), GraduationYear, DeptID, BatchID, CompanyID, LinkedInProfile, IsActive"],
              ["STUDENT", "Subtype", "PersonID (PK, FK), StudentID, EnrollmentYear, DeptID, CurrentSemester, CGPA"],
            ],
            [2000, 1800, 5560]
          ),
          blankPara(),

          heading("3.1.2 ISA Relationship", HeadingLevel.HEADING_3),
          para("The ISA relationship (triangle symbol) connects the supertype to its subtypes. In our V2 ER diagram, it\u2019s shown as a triangle with the following constraints:"),
          bullet("Disjoint constraint (d): An entity can belong to only ONE subtype. A person cannot be both Alumni and Student at the same time."),
          bullet("Total specialization (total): Every PERSON must be either an ALUMNI or a STUDENT. There\u2019s no person who doesn\u2019t belong to any subtype."),
          blankPara(),

          heading("3.2 Disjoint and Total Constraints", HeadingLevel.HEADING_2),
          para("These constraints define the rules for the generalization hierarchy:"),
          makeTable(
            ["Constraint", "Symbol", "Meaning", "Applied To"],
            [
              ["Disjoint", "d", "Entity belongs to only ONE subtype", "PERSON \u2192 ALUMNI, STUDENT"],
              ["Total", "total", "Every supertype instance must be in a subtype", "PERSON \u2192 ALUMNI, STUDENT"],
            ],
            [2000, 1200, 3600, 2560]
          ),
          blankPara(),
          para("So basically, every person in our system is either an alumni or a student, and they can\u2019t be both at the same time. This makes sense in a real college scenario."),
          new Paragraph({ children: [new PageBreak()] }),

          heading("3.3 Aggregation", HeadingLevel.HEADING_2),
          para("Aggregation is used when we need to attach attributes to a relationship itself, not just to the entities. The MENTORSHIP relationship is a perfect example. It\u2019s a relationship between two ALUMNI entities (mentor and mentee), but the mentorship itself has attributes like StartDate, EndDate, Status, MentorshipArea, and Goals."),
          para("Without aggregation, we wouldn\u2019t have a clean way to store these attributes. By treating the mentorship as a higher-level entity, we can properly model this scenario."),
          makeTable(
            ["Attribute", "Type", "Constraints", "Description"],
            [
              ["MentorshipID", "INT", "PK", "Unique identifier for each mentorship"],
              ["MentorID", "INT", "FK to ALUMNI", "The alumni who is mentoring"],
              ["MenteeID", "INT", "FK to ALUMNI", "The alumni who is being mentored"],
              ["StartDate", "DATE", "NOT NULL", "When the mentorship started"],
              ["EndDate", "DATE", "NULL", "When it ended (NULL if ongoing)"],
              ["Status", "VARCHAR(20)", "CHECK", "Active, Completed, Paused, Cancelled"],
              ["MentorshipArea", "VARCHAR(100)", "FK to MENTORSHIP_AREA", "Area of mentorship (e.g., Data Science)"],
              ["Goals", "TEXT", "NULL", "What the mentorship aims to achieve"],
            ],
            [2200, 1600, 2200, 3360]
          ),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 4. NORMALIZATION ====================
          heading("4. Normalization", HeadingLevel.HEADING_1),
          para("Normalization is the process of organizing data in a database to reduce redundancy and avoid anomalies (update, insertion, and deletion anomalies). We normalized all our tables up to BCNF."),
          blankPara(),

          heading("4.1 Why Normalize?", HeadingLevel.HEADING_2),
          para("Let\u2019s say we had a single table storing everything \u2014 alumni details, department info, company info, skills, events, etc. That would be a mess. If a department name changes, we\u2019d have to update it in hundreds of rows. If we delete the last alumni from a department, we lose the department info entirely. Normalization fixes all these problems by splitting data into logical tables."),
          blankPara(),

          heading("4.2 First Normal Form (1NF)", HeadingLevel.HEADING_2),
          para("1NF says: all values must be atomic (no multi-valued attributes in a single cell), and each row must be unique."),
          para("Our main violation was the ALUMNI table having multiple phone numbers and multiple skills stored in a single column. To fix this:"),
          bullet("Phone numbers moved to a separate ALUMNI_PHONE table with composite key (AlumniID, PhoneNumber)"),
          bullet("Skills moved to a separate ALUMNI_SKILL junction table with composite key (AlumniID, SkillID)"),
          bullet("Address decomposed into Address_City, Address_State, Address_PinCode"),
          blankPara(),

          heading("4.3 Second Normal Form (2NF)", HeadingLevel.HEADING_2),
          para("2NF says: the table must be in 1NF, and there should be no partial dependencies (non-key attributes must depend on the WHOLE primary key, not just part of it)."),
          para("Since all our tables have single-attribute primary keys (surrogate keys like AlumniID, DeptID, etc.), partial dependencies are automatically avoided. The only composite keys are in junction tables (ALUMNI_SKILL, ALUMNI_EVENT), where all non-key attributes depend on the full composite key."),
          blankPara(),

          heading("4.4 Third Normal Form (3NF)", HeadingLevel.HEADING_2),
          para("3NF says: no transitive dependencies. A transitive dependency is when A \u2192 B \u2192 C (B depends on A, and C depends on B)."),
          para("In our V2 design, we identified and fixed these transitive dependencies:"),
          bullet("DEPARTMENT.HODName \u2192 replaced with HODPersonID FK to PERSON table (3NF fix)"),
          bullet("EVENT.EventType \u2192 extracted to EVENT_TYPE lookup table"),
          bullet("MENTORSHIP.MentorshipArea \u2192 extracted to MENTORSHIP_AREA lookup table"),
          bullet("COMPANY.CompanySize \u2192 extracted to COMPANY_SIZE lookup table"),
          blankPara(),

          heading("4.5 Boyce-Codd Normal Form (BCNF)", HeadingLevel.HEADING_2),
          para("BCNF is stricter than 3NF. It says: for every functional dependency X \u2192 Y, X must be a superkey. After applying all the 3NF fixes, every determinant in our tables is a candidate key, so all tables satisfy BCNF."),
          blankPara(),
          para("Example \u2014 MENTORSHIP BCNF Check:"),
          bullet("Candidate Keys: MentorshipID, (MentorID, MenteeID, StartDate)"),
          bullet("FD: MentorID, MenteeID, StartDate \u2192 Status, EndDate, Goals, Feedback, Rating"),
          bullet("Left side is a superkey \u2192 No BCNF violation"),
          blankPara(),

          heading("4.6 Fourth Normal Form (4NF)", HeadingLevel.HEADING_2),
          para("4NF eliminates multi-valued dependencies. A multi-valued dependency X \u2192\u2192 Y exists when for each value of X, there is a set of values of Y that is independent of other attributes."),
          para("In our design, the main multi-valued dependencies were:"),
          bullet("AlumniID \u2192\u2192 Skills (an alumni can have multiple skills)"),
          bullet("AlumniID \u2192\u2192 Events (an alumni can attend multiple events)"),
          bullet("AlumniID \u2192\u2192 PhoneNumbers (an alumni can have multiple phone numbers)"),
          para("If we stored skills and events in the same ALUMNI table, we\u2019d get a Cartesian product problem \u2014 each skill would be repeated for every event and vice versa. We already solved this by decomposing into separate junction tables (ALUMNI_SKILL, ALUMNI_EVENT, ALUMNI_PHONE), so 4NF is satisfied."),
          blankPara(),

          heading("4.7 Fifth Normal Form (5NF)", HeadingLevel.HEADING_2),
          para("5NF deals with join dependencies. A relation is in 5NF if every join dependency is implied by its candidate keys. Basically, you can\u2019t decompose the table any further without losing data."),
          para("Consider a scenario tracking which alumni have which skills at which companies. If we had a single table (AlumniID, SkillID, CompanyID), we\u2019d have a cyclic join dependency that can\u2019t be decomposed. In our design, we avoid this by:"),
          bullet("ALUMNI table has CompanyID (current company)"),
          bullet("ALUMNI_SKILL has skills"),
          bullet("No direct three-way relationship between Alumni-Skill-Company"),
          para("All our decompositions are lossless \u2014 natural joins reconstruct the original data without spurious tuples."),
          blankPara(),

          heading("4.8 Functional Dependencies Summary", HeadingLevel.HEADING_2),
          para("Here are the key functional dependencies for our main tables:"),
          blankPara(),
          boldPara("ALUMNI"),
          ...codeBlock([
            "PersonID \u2192 GraduationYear, DeptID, BatchID, CurrentCompanyID, CurrentPosition, LinkedInProfile, IsActive",
            "PersonID (FK to PERSON \u2192 FirstName, LastName, Email, Phone, DOB, Gender, Address)",
          ]),
          blankPara(),
          boldPara("DEPARTMENT"),
          ...codeBlock([
            "DeptID \u2192 DeptName, DeptCode, HODPersonID, EstablishedYear",
            "DeptName \u2192 DeptID (Candidate Key)",
            "DeptCode \u2192 DeptID (Candidate Key)",
          ]),
          blankPara(),
          boldPara("EVENT"),
          ...codeBlock([
            "EventID \u2192 EventName, EventTypeID, Description, EventDate, EventTime, Venue, MaxCapacity, RegistrationFee, OrganizerID",
            "EventTypeID \u2192 (resolved via FK to EVENT_TYPE lookup table)",
          ]),
          blankPara(),
          boldPara("MENTORSHIP"),
          ...codeBlock([
            "MentorID, MenteeID, StartDate \u2192 EndDate, Status, AreaID, Goals, Feedback, Rating",
            "AreaID \u2192 (resolved via FK to MENTORSHIP_AREA lookup table)",
          ]),
          blankPara(),
          boldPara("DONATION"),
          ...codeBlock([
            "DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod, Purpose, TransactionID, IsAnonymous, ReceiptNumber",
            "TransactionID \u2192 DonationID (Candidate Key)",
            "ReceiptNumber \u2192 DonationID (Candidate Key)",
          ]),
          new Paragraph({ children: [new PageBreak()] }),

          heading("4.9 Decomposition Steps", HeadingLevel.HEADING_2),
          para("Here\u2019s a summary of how we decomposed our tables during normalization:"),
          blankPara(),
          boldPara("Step 1: Remove Multi-valued Attributes (1NF)"),
          bullet("Skills \u2192 ALUMNI_SKILL junction table"),
          bullet("Events Attended \u2192 ALUMNI_EVENT junction table"),
          bullet("Phone numbers \u2192 ALUMNI_PHONE table"),
          bullet("Address \u2192 Decomposed into Address_City, Address_State, Address_PinCode"),
          blankPara(),
          boldPara("Step 2: Remove Partial Dependencies (2NF)"),
          bullet("All tables have single-attribute PKs, so 2NF is automatically satisfied"),
          bullet("Junction tables: non-key attributes depend on full composite key"),
          blankPara(),
          boldPara("Step 3: Remove Transitive Dependencies (3NF)"),
          bullet("DeptName depends on DeptID, not AlumniID \u2192 Separate DEPARTMENT table"),
          bullet("CompanyName depends on CompanyID, not AlumniID \u2192 Separate COMPANY table"),
          bullet("BatchYear depends on BatchID, not AlumniID \u2192 Separate BATCH table"),
          bullet("HODName depends on HODPersonID \u2192 FK reference (V2 fix)"),
          bullet("EventType values \u2192 EVENT_TYPE lookup table (V2 fix)"),
          bullet("CompanySize values \u2192 COMPANY_SIZE lookup table (V2 fix)"),
          bullet("MentorshipArea values \u2192 MENTORSHIP_AREA lookup table (V2 fix)"),
          blankPara(),
          boldPara("Step 4: Verify BCNF"),
          bullet("All functional dependencies have superkeys on left side"),
          bullet("No violations found after 3NF decomposition"),
          blankPara(),
          boldPara("Step 5: Eliminate Multi-valued Dependencies (4NF)"),
          bullet("Already handled by junction tables (ALUMNI_SKILL, ALUMNI_EVENT, ALUMNI_PHONE)"),
          bullet("No redundant data storage"),
          blankPara(),
          boldPara("Step 6: Verify Join Dependencies (5NF)"),
          bullet("Complex relationships decomposed without loss"),
          bullet("All joins are lossless \u2014 no spurious tuples"),
          new Paragraph({ children: [new PageBreak()] }),

          heading("4.10 V2 Normalization Refinements", HeadingLevel.HEADING_2),
          para("In the second version of our design, we made several improvements based on normalization principles:"),
          makeTable(
            ["Issue", "Violation", "Solution"],
            [
              ["DEPARTMENT.HODName", "3NF - Transitive dependency", "Replaced with HODPersonID FK to PERSON"],
              ["EVENT.EventType", "Repeating domain values", "Extracted to EVENT_TYPE lookup table"],
              ["MENTORSHIP.MentorshipArea", "Free-text redundancy", "Extracted to MENTORSHIP_AREA lookup table"],
              ["COMPANY.CompanySize", "Repeating categories", "Extracted to COMPANY_SIZE lookup table"],
              ["POST.LikesCount", "Derived attribute", "Intentional denormalization (documented)"],
              ["JOB_APPLICATION", "Missing M:N relationship", "Added new junction table"],
            ],
            [2800, 2600, 3960]
          ),
          blankPara(),

          heading("4.11 Normalization Summary", HeadingLevel.HEADING_2),
          makeTable(
            ["Table", "1NF", "2NF", "3NF", "BCNF", "4NF", "5NF", "Notes"],
            [
              ["DEPARTMENT", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Multiple candidate keys"],
              ["BATCH", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", ""],
              ["COMPANY", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Size\u2192FK (v2)"],
              ["SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "SkillName is candidate key"],
              ["PERSON", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Email is candidate key"],
              ["ALUMNI", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "FK references"],
              ["STUDENT", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "StudentID is candidate key"],
              ["EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Type\u2192FK (v2)"],
              ["DONATION", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", ""],
              ["JOB", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", ""],
              ["MENTORSHIP", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Area\u2192FK (v2)"],
              ["ALUMNI_SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Junction table"],
              ["ALUMNI_PHONE", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Multivalued attribute"],
              ["ALUMNI_EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "Junction table"],
              ["JOB_APPLICATION", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "\u2713", "New in v2"],
            ],
            [1800, 700, 700, 700, 800, 700, 700, 2360]
          ),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 5. RELATIONAL SCHEMA ====================
          heading("5. Relational Schema", HeadingLevel.HEADING_1),
          para("The relational schema is the final step where we convert our ER/EER model into actual database tables with proper data types, constraints, and foreign key relationships. Here\u2019s what we ended up with:"),

          heading("5.1 Core Entity Tables", HeadingLevel.HEADING_2),
          makeTable(
            ["Table", "Primary Key", "Foreign Keys", "Key Constraints"],
            [
              ["PERSON", "PersonID", "\u2014", "Email UNIQUE, Gender CHECK (M/F/O)"],
              ["ALUMNI", "PersonID", "PersonID, DeptID, BatchID, CompanyID", "GraduationYear NOT NULL"],
              ["STUDENT", "PersonID", "PersonID, DeptID", "StudentID UNIQUE, CGPA CHECK"],
              ["DEPARTMENT", "DeptID", "HODPersonID", "DeptName UNIQUE, DeptCode UNIQUE"],
              ["BATCH", "BatchID", "DeptID", "BatchYear NOT NULL"],
              ["COMPANY", "CompanyID", "SizeID", "CompanyName NOT NULL"],
              ["SKILL", "SkillID", "\u2014", "SkillName UNIQUE"],
              ["EVENT", "EventID", "EventTypeID, OrganizerID", "EventDate NOT NULL"],
              ["DONATION", "DonationID", "DonorID", "TransactionID UNIQUE, ReceiptNumber UNIQUE"],
              ["JOB", "JobID", "CompanyID, PostedBy", "JobType CHECK"],
              ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, AreaID", "Status CHECK, Rating CHECK 1-5"],
            ],
            [2000, 1600, 3000, 2760]
          ),
          blankPara(),

          heading("5.2 Lookup Tables", HeadingLevel.HEADING_2),
          para("Lookup tables store domain values to avoid repeating the same strings everywhere. This is a normalization improvement we made in V2."),
          makeTable(
            ["Table", "Primary Key", "Key Column", "Purpose"],
            [
              ["EVENT_TYPE", "TypeID", "TypeName UNIQUE", "Categorize events (Reunion, Workshop, Seminar, Networking)"],
              ["COMPANY_SIZE", "SizeID", "SizeRange UNIQUE", "Categorize company sizes (1-10, 11-50, etc.)"],
              ["MENTORSHIP_AREA", "AreaID", "AreaName UNIQUE", "Categorize mentorship areas (Data Science, Web Dev, etc.)"],
            ],
            [2200, 1600, 2200, 3360]
          ),
          blankPara(),

          heading("5.3 Junction Tables", HeadingLevel.HEADING_2),
          para("Junction tables are used to resolve many-to-many (M:N) relationships into two one-to-many relationships. They have composite primary keys."),
          makeTable(
            ["Table", "Composite PK", "Foreign Keys", "Additional Attributes"],
            [
              ["ALUMNI_SKILL", "(AlumniID, SkillID)", "AlumniID, SkillID", "ProficiencyLevel CHECK"],
              ["ALUMNI_EVENT", "(AlumniID, EventID)", "AlumniID, EventID", "RegistrationDate"],
              ["ALUMNI_PHONE", "(AlumniID, PhoneNumber)", "AlumniID", "\u2014"],
              ["JOB_APPLICATION", "ApplicationID", "JobID, ApplicantID", "Status CHECK, ResumeLink"],
            ],
            [2200, 2200, 2200, 2760]
          ),
          blankPara(),

          heading("5.4 Referential Integrity", HeadingLevel.HEADING_2),
          para("All foreign keys enforce referential integrity to maintain data consistency:"),
          bullet("CASCADE: When parent is deleted, children are also deleted (e.g., if a PERSON is deleted, their ALUMNI record is also deleted)"),
          bullet("RESTRICT: Cannot delete parent if children exist (e.g., can\u2019t delete a DEPARTMENT if alumni belong to it)"),
          bullet("SET NULL: Foreign key is set to NULL when parent is deleted (e.g., if a COMPANY is deleted, alumni\u2019s CompanyID becomes NULL)"),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 6. CONCLUSION ====================
          heading("6. Conclusion", HeadingLevel.HEADING_1),
          para("So to wrap it up, we\u2019ve designed a complete database system for the Alumni Network and Engagement Platform. The design covers pretty much all the DBMS concepts we\u2019ve studied in class:"),
          blankPara(),
          bullet("ER Model with all 8 types of attributes (Simple, Composite, Multi-valued, Derived, Key, NULL, Single-valued, Stored)"),
          bullet("Strong entities with proper primary keys and weak entities with identifying relationships"),
          bullet("Binary, and unary (recursive) relationships with proper cardinality and participation constraints"),
          bullet("EER Model with Generalization/Specialization (PERSON \u2192 ALUMNI, STUDENT)"),
          bullet("Disjoint and Total constraints on the ISA hierarchy"),
          bullet("Aggregation for the MENTORSHIP relationship"),
          bullet("All tables normalized up to BCNF with documented refinements in V2"),
          bullet("Complete relational schema with 15+ tables, all constraints, foreign keys, and referential integrity"),
          bullet("Lookup tables for domain values and junction tables for M:N relationships"),
          blankPara(),
          para("The V2 version improved upon the initial design by fixing normalization issues like replacing HODName with a foreign key, extracting domain values into lookup tables, and adding the JOB_APPLICATION junction table."),
          new Paragraph({ children: [new PageBreak()] }),

          // ==================== 7. REFERENCES ====================
          heading("7. References", HeadingLevel.HEADING_1),
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
  const outPath = "/Users/dakshagarwal/dbms-project/laguna/report/Alumni_Network_Full_Assignment.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("Full assignment DOCX generated:", outPath);
}

main().catch(console.error);
