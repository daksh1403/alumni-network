const pptxgen = require("pptxgenjs");

const prs = new pptxgen();
prs.defineLayout({ name: "WIDE", width: 13.33, height: 7.5 });
prs.layout = "WIDE";
prs.author = "Sagarika Kaistha, Praveen G, Daksh Agarwal";
prs.title = "Alumni Network and Engagement Platform";

// Ocean Gradient palette - professional for DBMS project
const C = {
  primary: "065A82",      // Deep blue
  secondary: "1C7293",    // Teal
  accent: "21295C",       // Midnight
  light: "F0F7FB",        // Ice blue
  white: "FFFFFF",
  dark: "0A1628",         // Dark navy
  text: "1E293B",         // Dark slate
  muted: "64748B",        // Slate gray
  success: "059669",      // Emerald
  card: "FFFFFF",         // White cards
};

const headerFont = "Georgia";
const bodyFont = "Calibri";

// Shape aliases
const shapes = {
  rect: "rect",
  oval: "ellipse",
  line: "line",
};

// Helper for shadows (fresh object each time per pptxgenjs best practices)
const makeShadow = () => ({ type: "outer", blur: 4, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

function titleSlide(title, subtitle, members) {
  const slide = prs.addSlide();
  slide.background = { color: C.dark };
  
  // Left accent bar
  slide.addShape(shapes.rect, { x: 0, y: 0, w: 0.12, h: 7.5, fill: { color: C.secondary } });
  
  // Decorative circle
  slide.addShape(shapes.oval, { x: 10.5, y: -1, w: 4, h: 4, fill: { color: C.primary, transparency: 30 } });
  slide.addShape(shapes.oval, { x: 11.5, y: 5, w: 3, h: 3, fill: { color: C.secondary, transparency: 40 } });
  
  // Institution
  slide.addText("Vellore Institute of Technology", { x: 1, y: 0.8, w: 9, h: 0.5, fontSize: 16, fontFace: bodyFont, color: C.secondary, bold: true, margin: 0 });
  slide.addText("School of Computer Science and Engineering", { x: 1, y: 1.3, w: 9, h: 0.35, fontSize: 12, fontFace: bodyFont, color: C.muted, margin: 0 });
  
  // Title
  slide.addText(title, { x: 1, y: 2.2, w: 9, h: 1.5, fontSize: 38, fontFace: headerFont, color: C.white, bold: true, margin: 0 });
  
  // Subtitle
  slide.addText(subtitle, { x: 1, y: 4.0, w: 9, h: 0.6, fontSize: 16, fontFace: bodyFont, color: C.light, margin: 0 });
  
  // Course info
  slide.addText("Course: Database Management Systems (CSE2005)", { x: 1, y: 5.0, w: 9, h: 0.3, fontSize: 12, fontFace: bodyFont, color: C.muted, margin: 0 });
  
  // Team members in card
  slide.addShape(shapes.rect, { x: 1, y: 5.6, w: 6, h: 1.2, fill: { color: C.primary, transparency: 50 }, shadow: makeShadow() });
  slide.addText("Team Members", { x: 1.2, y: 5.65, w: 5, h: 0.3, fontSize: 10, fontFace: bodyFont, color: C.secondary, bold: true, margin: 0 });
  members.forEach((m, i) => {
    slide.addText(m, { x: 1.2, y: 5.95 + i * 0.25, w: 5, h: 0.25, fontSize: 11, fontFace: bodyFont, color: C.white, margin: 0 });
  });
}

function sectionSlide(title, subtitle) {
  const slide = prs.addSlide();
  slide.background = { color: C.primary };
  
  // Decorative elements
  slide.addShape(shapes.oval, { x: -1, y: -1, w: 3, h: 3, fill: { color: C.secondary, transparency: 50 } });
  slide.addShape(shapes.oval, { x: 11, y: 5, w: 4, h: 4, fill: { color: C.accent, transparency: 40 } });
  
  // Content
  slide.addText(title, { x: 1.5, y: 2.5, w: 10, h: 1.2, fontSize: 36, fontFace: headerFont, color: C.white, bold: true, align: "center", margin: 0 });
  slide.addText(subtitle, { x: 1.5, y: 3.8, w: 10, h: 0.6, fontSize: 16, fontFace: bodyFont, color: C.light, align: "center", margin: 0 });
}

function contentSlide(title, items) {
  const slide = prs.addSlide();
  slide.background = { color: C.light };
  
  // Header bar
  slide.addShape(shapes.rect, { x: 0, y: 0, w: 13.33, h: 1.0, fill: { color: C.primary } });
  slide.addText(title, { x: 0.8, y: 0.2, w: 11, h: 0.6, fontSize: 24, fontFace: headerFont, color: C.white, bold: true, margin: 0 });
  
  // Content card
  slide.addShape(shapes.rect, { x: 0.5, y: 1.3, w: 12.33, h: 5.5, fill: { color: C.white }, shadow: makeShadow() });
  
  // Bullet points
  const rows = items.map(item => ({
    text: item,
    options: { fontSize: 15, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 12 }, paraSpaceAfter: 8 }
  }));
  
  slide.addText(rows, { x: 1.0, y: 1.5, w: 11.33, h: 5.0, valign: "top", margin: 0 });
  
  // Slide number
  slide.addText(String(slide._slideNum), { x: 12.5, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, fontFace: bodyFont, color: C.muted, align: "right", margin: 0 });
}

function tableSlide(title, headers, data) {
  const slide = prs.addSlide();
  slide.background = { color: C.light };
  
  // Header bar
  slide.addShape(shapes.rect, { x: 0, y: 0, w: 13.33, h: 1.0, fill: { color: C.primary } });
  slide.addText(title, { x: 0.8, y: 0.2, w: 11, h: 0.6, fontSize: 24, fontFace: headerFont, color: C.white, bold: true, margin: 0 });
  
  // Table
  const rows = [
    headers.map(h => ({ text: h, options: { fontSize: 11, fontFace: bodyFont, color: C.white, bold: true, align: "center", fill: { color: C.secondary } } })),
    ...data.map((row, ri) => row.map((c, ci) => ({
      text: String(c),
      options: { fontSize: 10, fontFace: bodyFont, color: C.text, align: ci === 0 ? "left" : "center", fill: { color: ri % 2 === 0 ? C.white : C.light } }
    })))
  ];
  
  const colW = headers.map(() => 12 / headers.length);
  slide.addTable(rows, {
    x: 0.5, y: 1.3, w: 12.33,
    colW: colW,
    border: { pt: 0.5, color: "CBD5E1" },
    rowH: 0.3,
    fill: { color: C.white },
    shadow: makeShadow(),
  });
  
  // Slide number
  slide.addText(String(slide._slideNum), { x: 12.5, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, fontFace: bodyFont, color: C.muted, align: "right", margin: 0 });
}

function cardSlide(title, cards) {
  const slide = prs.addSlide();
  slide.background = { color: C.light };
  
  // Header bar
  slide.addShape(shapes.rect, { x: 0, y: 0, w: 13.33, h: 1.0, fill: { color: C.primary } });
  slide.addText(title, { x: 0.8, y: 0.2, w: 11, h: 0.6, fontSize: 24, fontFace: headerFont, color: C.white, bold: true, margin: 0 });
  
  // Cards in 2x2 or 2x3 grid
  const cols = Math.min(cards.length, 3);
  const rows = Math.ceil(cards.length / cols);
  const cardW = (12.33 - (cols - 1) * 0.3) / cols;
  const cardH = (5.5 - (rows - 1) * 0.3) / rows;
  
  cards.forEach((card, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = 0.5 + col * (cardW + 0.3);
    const y = 1.3 + row * (cardH + 0.3);
    
    // Card background
    slide.addShape(shapes.rect, { x, y, w: cardW, h: cardH, fill: { color: C.white }, shadow: makeShadow() });
    
    // Accent bar
    slide.addShape(shapes.rect, { x, y, w: 0.08, h: cardH, fill: { color: C.secondary } });
    
    // Card title
    slide.addText(card.title, { x: x + 0.2, y: y + 0.15, w: cardW - 0.4, h: 0.35, fontSize: 14, fontFace: bodyFont, color: C.primary, bold: true, margin: 0 });
    
    // Card content
    const contentRows = card.items.map(item => ({
      text: item,
      options: { fontSize: 11, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 8 }, paraSpaceAfter: 4 }
    }));
    slide.addText(contentRows, { x: x + 0.2, y: y + 0.5, w: cardW - 0.4, h: cardH - 0.6, valign: "top", margin: 0 });
  });
  
  // Slide number
  slide.addText(String(slide._slideNum), { x: 12.5, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, fontFace: bodyFont, color: C.muted, align: "right", margin: 0 });
}

function thankYouSlide() {
  const slide = prs.addSlide();
  slide.background = { color: C.dark };
  
  // Decorative
  slide.addShape(shapes.oval, { x: 0.5, y: 0.5, w: 3, h: 3, fill: { color: C.primary, transparency: 40 } });
  slide.addShape(shapes.oval, { x: 10, y: 4, w: 4, h: 4, fill: { color: C.secondary, transparency: 50 } });
  
  // Thank you
  slide.addText("THANK YOU", { x: 1, y: 2.2, w: 11, h: 1.2, fontSize: 48, fontFace: headerFont, color: C.white, bold: true, align: "center", margin: 0 });
  slide.addText("Questions & Discussion", { x: 1, y: 3.5, w: 11, h: 0.6, fontSize: 20, fontFace: bodyFont, color: C.light, align: "center", margin: 0 });
  
  // Team info card
  slide.addShape(shapes.rect, { x: 3, y: 4.8, w: 7, h: 1.5, fill: { color: C.primary, transparency: 50 }, shadow: makeShadow() });
  slide.addText("Sagarika Kaistha (25BCE5091)", { x: 3.2, y: 4.9, w: 6.5, h: 0.35, fontSize: 13, fontFace: bodyFont, color: C.white, align: "center", margin: 0 });
  slide.addText("Praveen G (25BCE5092)", { x: 3.2, y: 5.25, w: 6.5, h: 0.35, fontSize: 13, fontFace: bodyFont, color: C.white, align: "center", margin: 0 });
  slide.addText("Daksh Agarwal (25BCE5098)", { x: 3.2, y: 5.6, w: 6.5, h: 0.35, fontSize: 13, fontFace: bodyFont, color: C.white, align: "center", margin: 0 });
}

// ===================== BUILD SLIDES =====================

// 1. TITLE
titleSlide(
  "ALUMNI NETWORK AND\nENGAGEMENT PLATFORM",
  "Database Management Systems Project  |  DA1",
  ["Sagarika Kaistha - 25BCE5091", "Praveen G - 25BCE5092", "Daksh Agarwal - 25BCE5098"]
);

// 2. AGENDA
cardSlide("What We Cover", [
  { title: "ER Model", items: ["Entities & Attributes", "Relationships", "Constraints"] },
  { title: "EER Model", items: ["Generalization", "ISA Relationship", "Aggregation"] },
  { title: "Normalization", items: ["1NF to BCNF", "Functional Dependencies", "Decomposition"] },
  { title: "Relational Schema", items: ["Tables & Keys", "Constraints", "Referential Integrity"] },
]);

// 3. PROBLEM STATEMENT
cardSlide("Problem Statement", [
  { title: "The Problem", items: ["No centralized alumni tracking", "Lost connection after graduation", "Manual donation tracking", "No mentorship platform"] },
  { title: "Our Solution", items: ["Complete database system", "Alumni information management", "Events & donations tracking", "Job & mentorship support"] },
]);

// 4. SECTION: ER MODEL
sectionSlide("ENTITY-RELATIONSHIP MODEL", "Entities, Attributes, and Relationships");

// 5. TYPES OF ATTRIBUTES
tableSlide("Types of Attributes",
  ["Type", "Example", "Entity", "Description"],
  [
    ["Simple", "FirstName, Email", "PERSON", "Atomic, indivisible"],
    ["Composite", "Address", "PERSON", "City + State + PinCode"],
    ["Multi-valued", "Skills", "ALUMNI", "Multiple values per entity"],
    ["Multi-valued", "PhoneNumbers", "ALUMNI", "Mobile, Home, Work"],
    ["Derived", "Age", "PERSON", "Calculated from DOB"],
    ["Key", "PersonID", "All", "Unique identifier"],
    ["NULL", "LinkedInProfile", "ALUMNI", "Optional attribute"],
    ["Stored", "GraduationYear", "ALUMNI", "Directly stored"],
  ]
);

// 6. STRONG ENTITIES
tableSlide("Strong Entities",
  ["Entity", "Primary Key", "Key Attributes"],
  [
    ["PERSON", "PersonID", "Name, Email, Gender, DOB"],
    ["ALUMNI", "PersonID", "GraduationYear, DeptID, BatchID"],
    ["STUDENT", "PersonID", "StudentID, EnrollmentYear, CGPA"],
    ["DEPARTMENT", "DeptID", "DeptName, DeptCode, HODPersonID"],
    ["BATCH", "BatchID", "BatchYear, Section, TotalStudents"],
    ["COMPANY", "CompanyID", "Name, Industry, SizeID"],
    ["SKILL", "SkillID", "SkillName, Category"],
    ["EVENT", "EventID", "Name, TypeID, Date, Venue"],
    ["DONATION", "DonationID", "Amount, Date, PaymentMethod"],
    ["JOB", "JobID", "Title, CompanyID, Type, Salary"],
    ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, Status"],
  ]
);

// 7. RELATIONSHIPS
tableSlide("Relationships",
  ["Entities", "Relationship", "Cardinality", "Participation"],
  [
    ["ALUMNI - DEPARTMENT", "belongs_to", "N:1", "Total / Partial"],
    ["ALUMNI - BATCH", "belongs_to", "N:1", "Total / Partial"],
    ["ALUMNI - COMPANY", "works_at", "N:1", "Partial / Partial"],
    ["ALUMNI - SKILL", "has", "M:N", "Partial / Partial"],
    ["ALUMNI - EVENT", "attends", "M:N", "Partial / Partial"],
    ["ALUMNI - DONATION", "makes", "1:N", "Partial / Total"],
    ["ALUMNI - JOB", "posts", "1:N", "Partial / Total"],
    ["ALUMNI - MENTORSHIP", "mentors", "1:N", "Unary Recursive"],
  ]
);

// 8. SECTION: EER
sectionSlide("EXTENDED ER MODEL", "Generalization, Specialization & Aggregation");

// 9. GENERALIZATION
cardSlide("Generalization / Specialization", [
  { title: "What We Did", items: ["Combined ALUMNI and STUDENT into PERSON supertype", "Common attributes: Name, Email, Phone, DOB", "Specific attributes in each subtype"] },
  { title: "ISA Relationship", items: ["Shown as triangle in ER diagram", "Disjoint: Person is Alumni OR Student", "Total: Every person must be classified"] },
  { title: "Implementation", items: ["PERSON table for common attributes", "ALUMNI table for alumni-specific data", "STUDENT table for student-specific data", "PersonID links all three tables"] },
]);

// 10. PERSON HIERARCHY
tableSlide("PERSON Generalization Hierarchy",
  ["Entity", "Type", "Attributes"],
  [
    ["PERSON", "Supertype", "PersonID (PK), FirstName, LastName, Email, Phone, DOB, Gender, Address"],
    ["ALUMNI", "Subtype", "PersonID (PK,FK), GraduationYear, DeptID, BatchID, CompanyID, LinkedIn, IsActive"],
    ["STUDENT", "Subtype", "PersonID (PK,FK), StudentID, EnrollmentYear, DeptID, Semester, CGPA"],
  ]
);

// 11. AGGREGATION
cardSlide("Aggregation - MENTORSHIP", [
  { title: "The Problem", items: ["Mentorship is a relationship between two ALUMNI", "But it has its own attributes", "Can't store these without aggregation"] },
  { title: "The Solution", items: ["Treat mentorship as higher-level entity", "MentorshipID as Primary Key", "MentorID and MenteeID as Foreign Keys"] },
  { title: "Key Attributes", items: ["StartDate, EndDate", "Status: Active/Completed/Paused", "AreaID (FK to MENTORSHIP_AREA)", "Goals, Feedback, Rating"] },
]);

// 12. SECTION: NORMALIZATION
sectionSlide("NORMALIZATION", "Eliminating Redundancy & Preventing Anomalies");

// 13. WHY NORMALIZE
cardSlide("Why Normalize?", [
  { title: "Problems Without", items: ["DeptName change = update 100s of rows", "Can't add dept without alumni", "Delete last alumni = lose dept info", "Data repeated everywhere"] },
  { title: "Benefits With", items: ["Each data stored only once", "Changes in one place only", "No update anomalies", "No insertion/deletion anomalies"] },
]);

// 14. 1NF
cardSlide("First Normal Form (1NF)", [
  { title: "Rule", items: ["All values must be atomic", "No multi-valued attributes", "No repeating groups"] },
  { title: "Our Fixes", items: ["Skills -> ALUMNI_SKILL table", "Phones -> ALUMNI_PHONE table", "Address -> City, State, PinCode"] },
]);

// 15. 2NF AND 3NF
cardSlide("2NF and 3NF", [
  { title: "2NF - No Partial Deps", items: ["All tables have single PK", "No partial dependencies", "Automatic for our design"] },
  { title: "3NF - No Transitive Deps", items: ["DeptID -> DeptName was violation", "Fixed with separate DEPARTMENT table", "HODName -> HODPersonID FK", "EventType -> EVENT_TYPE lookup"] },
]);

// 16. BCNF
cardSlide("BCNF and Beyond", [
  { title: "BCNF Rule", items: ["Every determinant must be candidate key", "Stricter than 3NF", "All tables satisfy BCNF"] },
  { title: "Also Verified", items: ["4NF: No multi-valued deps", "5NF: All join deps implied by keys", "Result: 18 tables in BCNF"] },
]);

// 17. NORMALIZATION SUMMARY
tableSlide("Normalization Summary",
  ["Table", "1NF", "2NF", "3NF", "BCNF", "Notes"],
  [
    ["PERSON", "\u2713", "\u2713", "\u2713", "\u2713", "Supertype"],
    ["ALUMNI", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype"],
    ["STUDENT", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype"],
    ["DEPARTMENT", "\u2713", "\u2713", "\u2713", "\u2713", "HODPersonID FK"],
    ["COMPANY", "\u2713", "\u2713", "\u2713", "\u2713", "SizeID FK"],
    ["EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "EventTypeID FK"],
    ["MENTORSHIP", "\u2713", "\u2713", "\u2713", "\u2713", "AreaID FK"],
    ["ALUMNI_SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Junction"],
    ["ALUMNI_EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "Junction"],
    ["JOB_APPLICATION", "\u2713", "\u2713", "\u2713", "\u2713", "Junction"],
  ]
);

// 18. SECTION: RELATIONAL SCHEMA
sectionSlide("RELATIONAL SCHEMA", "Tables, Constraints & Referential Integrity");

// 19. CORE TABLES
tableSlide("Core Tables",
  ["Table", "Primary Key", "Foreign Keys"],
  [
    ["PERSON", "PersonID", "-"],
    ["ALUMNI", "PersonID", "PersonID, DeptID, BatchID, CompanyID"],
    ["STUDENT", "PersonID", "PersonID, DeptID"],
    ["DEPARTMENT", "DeptID", "HODPersonID"],
    ["BATCH", "BatchID", "DeptID"],
    ["COMPANY", "CompanyID", "SizeID"],
    ["EVENT", "EventID", "EventTypeID, OrganizerID"],
    ["DONATION", "DonationID", "DonorID"],
    ["JOB", "JobID", "CompanyID, PostedBy"],
    ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, AreaID"],
  ]
);

// 20. LOOKUP AND JUNCTION TABLES
tableSlide("Lookup & Junction Tables",
  ["Table", "Type", "Key Columns", "Purpose"],
  [
    ["EVENT_TYPE", "Lookup", "TypeID, TypeName", "Event categories"],
    ["COMPANY_SIZE", "Lookup", "SizeID, SizeRange", "Company sizes"],
    ["MENTORSHIP_AREA", "Lookup", "AreaID, AreaName", "Mentorship areas"],
    ["ALUMNI_SKILL", "Junction", "PersonID, SkillID", "M:N resolver"],
    ["ALUMNI_EVENT", "Junction", "PersonID, EventID", "M:N resolver"],
    ["ALUMNI_PHONE", "Junction", "PersonID, PhoneNumber", "Multivalued"],
    ["JOB_APPLICATION", "Junction", "ApplicationID", "M:N resolver"],
  ]
);

// 21. CONSTRAINTS
cardSlide("Constraints Applied", [
  { title: "Key Constraints", items: ["Primary Keys on all tables", "Foreign Keys with CASCADE/RESTRICT/SET NULL", "CHECK for data validation", "UNIQUE on Email, StudentID, TransactionID"] },
  { title: "Referential Integrity", items: ["CASCADE: Delete children with parent", "RESTRICT: Can't delete if children exist", "SET NULL: FK becomes NULL on delete", "Example: Delete COMPANY -> alumni CompanyID = NULL"] },
]);

// 22. CONCLUSION
cardSlide("Conclusion", [
  { title: "ER Model", items: ["All 8 attribute types", "11 strong entities", "Binary & unary relationships", "Participation & cardinality"] },
  { title: "EER Model", items: ["PERSON supertype", "ALUMNI/STUDENT subtypes", "ISA with disjoint+total", "Aggregation for MENTORSHIP"] },
  { title: "Normalization", items: ["All 18 tables in BCNF", "Lookup tables for domain values", "Junction tables for M:N", "No redundancy or anomalies"] },
  { title: "Schema", items: ["Complete relational schema", "Proper constraints", "Referential integrity", "Ready for implementation"] },
]);

// 23. REFERENCES
contentSlide("References", [
  "[1] Silberschatz, Korth & Sudarshan - Database System Concepts (7th ed.)",
  "[2] Elmasri & Navathe - Fundamentals of Database Systems (7th ed.)",
  "[3] Connolly & Begg - Database Systems: A Practical Approach (6th ed.)",
  "[4] Date - An Introduction to Database Systems (8th ed.)",
  "[5] Ramakrishnan & Gehrke - Database Management Systems (3rd ed.)"
]);

// 24. THANK YOU
thankYouSlide();

// SAVE
const outPath = "/Users/dakshagarwal/dbms-project/laguna/report/Alumni_Network_Presentation.pptx";
prs.writeFile({ fileName: outPath }).then(() => {
  console.log("Presentation generated:", outPath);
  console.log("Total slides:", prs.slides.length);
}).catch(console.error);
