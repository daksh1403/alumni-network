#!/usr/bin/env python3
"""
Generate Alumni_Network_Normalization_Class_Method.docx

Per the class method (Normalization.pptx / Dr. Suhail K BCNF pptx) and the
faculty's instruction:

  "If we consider the primary key, all the entities are already in BCNF.
   So write at least 5 sample values in each entity so the schema can
   really be implemented."

For EVERY entity this report provides:
  1. Primary-key consideration statement  (PK -> everything in BCNF)
  2. Initial flat relation + Functional Dependencies + Candidate Key
  3. Sample data (5 records) for the final relation  (implementable)
  4. Normal-form check table (the STATEMENT: 1NF/2NF/3NF/BCNF)
  5. Decomposition shown clearly with DATA tables (not just a statement)
     - 2NF: split partial dependencies by projection
     - 3NF: split transitive dependencies by projection
     - each step shows the actual tables with the 5 records
  6. Result: in BCNF

ER alignment (ER_Diagram_V2.drawio):
  - No PERSON supertype, no COMPANY-JOB relationship (JOB has no CompanyID)
  - STUDENT included; MENTORSHIP links ALUMNI (mentor) -> STUDENT (mentee)
  - 14 relations: DEPARTMENT, BATCH, COMPANY, SKILL, ALUMNI, STUDENT,
    MENTORSHIP, EVENT, DONATION, JOB, ALUMNI_SKILL, ALUMNI_EVENT,
    ALUMNI_PHONE, STUDENT_EMAIL
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/Users/dakshagarwal/dbms-project/Alumni_Network_Normalization_Class_Method.docx"

HEADER_FILL = "1F4E78"
ROW_FILL = "EEF5FB"
GREEN = RGBColor(0x2C, 0x5F, 0x2D)
ACCENT = RGBColor(0x1A, 0x3C, 0x5E)
SUB = RGBColor(0x2E, 0x6B, 0x9E)
GRAY = RGBColor(0x88, 0x88, 0x88)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def set_cell_shading(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def style_cell(cell, text, bold=False, color=None, font_size=8.5, center=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(str(text))
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def add_table(doc, headers, rows, font_size=8.5, center_cols=None):
    center_cols = center_cols or set()
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = table.rows[0].cells[j]
        set_cell_shading(c, HEADER_FILL)
        style_cell(c, h, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), font_size=font_size, center=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = table.rows[i + 1].cells[j]
            if i % 2 == 0:
                set_cell_shading(c, ROW_FILL)
            style_cell(c, val, font_size=font_size, center=(j in center_cols))
    return table


def para(doc, text, size=11, bold=False, color=None, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return p


def bullet(doc, text, size=11):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    return p


def code(doc, text, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "F2F2F2")
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(size)
    return p


def caption(doc, text, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = SUB
    return p


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 13, 3: 11.5}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.bold = True
    run.font.size = Pt(sizes.get(level, 11))
    run.font.color.rgb = ACCENT if level == 1 else (SUB if level == 2 else GRAY)
    return p


def page_break(doc):
    doc.add_page_break()


# ---------------------------------------------------------------------------
# section builder — the class method for ONE relation
# ---------------------------------------------------------------------------

def relation_section(doc, num, title, intro, pk_statement, flat_code, fds, ck,
                     final_headers, final_rows, nf_rows, decomp=None,
                     no_decomp_note=None, bcnf_note=None, final_font=8.5,
                     bcnf_decomp=None):
    heading(doc, f"2.{num} {title}", 2)
    para(doc, intro)

    # 1. primary key consideration (faculty's point)
    p = para(doc, "Primary key consideration: ", bold=True, color=SUB, space_after=2)
    p.add_run(pk_statement)

    # 2. flat relation + FDs + candidate key
    para(doc, "Initial (flat) relation and Functional Dependencies:", bold=True, space_after=2)
    code(doc, flat_code)
    for fd in fds:
        code(doc, fd)
    code(doc, "Candidate Key(s): " + ck)

    # 3. sample data — 5 records (implementable)
    caption(doc, f"Sample data \u2014 {title} (5 records):")
    add_table(doc, final_headers, final_rows, font_size=final_font)

    # 4. normal-form check (the statement)
    caption(doc, "Normal-form check:")
    add_table(doc, ["Normal Form", "Status", "Reasoning"], nf_rows, font_size=9)

    # 5. decomposition — clearly seen with data
    if decomp:
        heading(doc, "Decomposition (step by step)", 3)
        for step in decomp:
            para(doc, step["label"], bold=True, space_after=2)
            para(doc, step["stmt"], space_after=3)
            for cap, h, r in step["tables"]:
                caption(doc, cap)
                add_table(doc, h, r, font_size=step.get("font", 8.5))
            doc.add_paragraph()
    if no_decomp_note is None and not decomp and not bcnf_decomp:
        para(doc, "No decomposition required \u2014 the initial relation is already the final relation.", italic=True, size=10, color=GRAY)

    # 5b. BCNF decomposition check (general algorithm, after MENTORSHIP)
    if bcnf_decomp:
        heading(doc, "BCNF Decomposition Check", 3)
        for step in bcnf_decomp:
            para(doc, step["label"], bold=True, space_after=2)
            para(doc, step["stmt"], space_after=3)
            for cap, h, r in step["tables"]:
                caption(doc, cap)
                add_table(doc, h, r, font_size=step.get("font", 8.5))
            doc.add_paragraph()

    if bcnf_note:
        para(doc, bcnf_note, size=10.5, italic=True, color=GRAY)
    p = para(doc, f"Result: {title} is in BCNF \u2713", bold=True, color=GREEN, space_after=10)


# ---------------------------------------------------------------------------
# document
# ---------------------------------------------------------------------------

def build_document():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)

    # ================= TITLE =================
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Vellore Institute of Technology"); r.font.bold = True; r.font.size = Pt(20); r.font.color.rgb = RGBColor(0x8B, 0x00, 0x00)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("School of Computer Science and Engineering"); r.font.size = Pt(13); r.font.color.rgb = GRAY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Course: Database Management Systems (CSE2005)  |  Faculty: Dr. [Faculty Name]  |  Slot: [Slot]"); r.font.size = Pt(11); r.font.color.rgb = GRAY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(16)
    r = p.add_run("NORMALIZATION REPORT"); r.font.bold = True; r.font.size = Pt(28); r.font.color.rgb = ACCENT
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Alumni Network and Engagement Platform"); r.font.size = Pt(15); r.font.color.rgb = SUB
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Normalization 1NF \u2192 BCNF \u2014 with primary-key consideration, 5 sample records per relation, and step-by-step decomposition"); r.font.italic = True; r.font.size = Pt(10.5); r.font.color.rgb = GRAY
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Submitted by:"); r.font.bold = True; r.font.size = Pt(12)
    for name in ["Sagarika Kaistha \u2014 25BCE5091", "Praveen G \u2014 25BCE5092", "Daksh Agarwal \u2014 25BCE5098"]:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(name); r.font.size = Pt(11)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Date of Submission: 31-07-2026"); r.font.italic = True; r.font.size = Pt(10); r.font.color.rgb = GRAY
    page_break(doc)

    # ================= 1. INTRODUCTION =================
    heading(doc, "1. Introduction to Normalization", 1)
    para(doc, "Normalization organizes the data of a relational database so that redundancy is reduced and update, insertion, and deletion anomalies are prevented. The process used in this report is the one taught in class:")
    bullet(doc, "Take the ER diagram and write each entity as a flat initial relation (one row per occurrence, atomic columns).")
    bullet(doc, "List the functional dependencies (FDs) that hold in that relation and find the candidate key / primary key.")
    bullet(doc, "Check 1NF, 2NF, 3NF and BCNF.")
    bullet(doc, "Wherever a dependency is violated, decompose by projection: split R on the violating FD X \u2192 A into R1 = X \u222a A and R2 = R \u2212 A, and repeat.")
    para(doc, "Faculty note on the primary key: if we consider the primary key of each relation, then all the entities are already in BCNF \u2014 because a single-attribute primary key makes a partial dependency impossible, and the determinants used in the report are exactly the candidate keys. To make the design truly implementable, at least five sample records are written for every relation, and the decomposition that produces each final relation is shown step by step with these records \u2014 not merely stated.")
    para(doc, "The final design contains 14 relations, aligned with the finalized ER diagram: no PERSON supertype, no COMPANY\u2013JOB relationship (JOB carries no CompanyID), STUDENT is included, the multivalued attributes are ALUMNI's PhoneNumbers (ALUMNI_PHONE) and STUDENT's Email (STUDENT_EMAIL), and MENTORSHIP \u2014 a weak entity identified through ALUMNI \u2014 connects one alumnus (mentor) to one student (mentee).")
    page_break(doc)

    # ================= 2. TABLE BY TABLE =================
    heading(doc, "2. Table-by-Table Normalization Analysis", 1)
    para(doc, "Each section below gives the primary-key consideration, the functional dependencies, five sample records, the normal-form check table (statement), and the decomposition with the actual tables.")

    # ---- 2.1 DEPARTMENT ----
    relation_section(
        doc, 1, "DEPARTMENT",
        "Stores academic departments (CSE, ECE, MECH, ...). DEPARTMENT is a strong entity with primary key DeptID.",
        "DeptID is a single-attribute primary key, so every non-key attribute (DeptName, DeptCode, HODName, EstablishedYear) is fully functionally dependent on the whole key. No partial or transitive dependency can exist, so the relation is already in BCNF.",
        "DEPARTMENT (DeptID, DeptName, DeptCode, HODName, EstablishedYear)",
        [
            "DeptID \u2192 DeptName, DeptCode, HODName, EstablishedYear",
            "DeptName \u2192 DeptID   (candidate key)",
            "DeptCode \u2192 DeptID   (candidate key)",
        ],
        "DeptID (DeptName and DeptCode are alternative candidate keys)",
        ["DeptID", "DeptName", "DeptCode", "HODName", "EstablishedYear"],
        [
            ["1", "Computer Science", "CSE", "Dr. R. Sharma", "1998"],
            ["2", "Electronics & Comm.", "ECE", "Dr. S. Iyer", "1999"],
            ["3", "Mechanical Engg.", "MECH", "Dr. A. Verma", "1995"],
            ["4", "Electrical Engg.", "EEE", "Dr. P. Nair", "2001"],
            ["5", "Civil Engg.", "CIVIL", "Dr. K. Rao", "1994"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic; no composite or multi-valued attribute."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 a partial dependency is impossible."],
            ["3NF", "\u2713 Pass", "DeptName and DeptCode are candidate keys, so there is no non-prime \u2192 non-prime dependency."],
            ["BCNF", "\u2713 Pass", "Every determinant (DeptID, DeptName, DeptCode) is a candidate key."],
        ],
        no_decomp_note="No decomposition required: the initial flat relation is already the final relation. The only determinants are DeptID, DeptName and DeptCode \u2014 all candidate keys.",
        bcnf_note="In the ER diagram, BATCH and ALUMNI relate to DEPARTMENT, so DeptID appears as a foreign key in those relations (not repeated as DeptName).",
    )

    # ---- 2.2 BATCH ----
    batch_flat = [
        ["1", "2023", "A", "120", "1", "Computer Science", "S001", "Ravi Kumar"],
        ["1", "2023", "A", "120", "1", "Computer Science", "S002", "Anita Shah"],
        ["3", "2024", "A", "125", "2", "Electronics & Comm.", "S003", "Farhan Ali"],
        ["4", "2024", "B", "122", "3", "Mechanical Engg.", "S004", "Lakshmi Bhat"],
        ["5", "2025", "A", "130", "4", "Electrical Engg.", "S005", "Mohan Das"],
    ]
    relation_section(
        doc, 2, "BATCH",
        "Stores batch year, section, and total students. In the ER diagram BATCH belongs to DEPARTMENT, and a batch has many students \u2014 so the flat relation initially carries DeptName and the student roster.",
        "The flat relation has the composite key (BatchID, StudentID). After the partial and transitive dependencies are removed by projection, each resulting relation has a single-attribute primary key (BatchID or StudentID) and is therefore already in BCNF.",
        "BATCH_flat (BatchID, BatchYear, Section, TotalStudents, DeptID, DeptName, StudentID, StudentName)",
        [
            "BatchID \u2192 BatchYear, Section, TotalStudents, DeptID",
            "DeptID \u2192 DeptName        (transitive dependency)",
            "StudentID \u2192 StudentName   (partial dependency \u2014 StudentID is a proper subset of the key)",
        ],
        "(BatchID, StudentID) \u2014 composite key of the flat relation",
        ["BatchID", "BatchYear", "Section", "TotalStudents", "DeptID"],
        [
            ["1", "2023", "A", "120", "1"],
            ["2", "2023", "B", "118", "1"],
            ["3", "2024", "A", "125", "2"],
            ["4", "2024", "B", "122", "3"],
            ["5", "2025", "A", "130", "4"],
        ],
        [
            ["1NF", "\u2713 Pass", "After flattening, every cell holds one atomic value; no repeating group."],
            ["2NF", "\u2713 Pass", "Partial dependency StudentID \u2192 StudentName removed by projection (Step 1)."],
            ["3NF", "\u2713 Pass", "Transitive dependency BatchID \u2192 DeptID \u2192 DeptName removed by projection (Step 2)."],
            ["BCNF", "\u2713 Pass", "Determinants BatchID (in BATCH) and StudentID (in the student roster) are candidate keys."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 2NF: remove the partial dependency StudentID \u2192 StudentName",
                "stmt": "StudentID is a proper subset of the composite key (BatchID, StudentID). Project the relation over the two dependencies:",
                "tables": [
                    ("R1 = BATCH facts (BatchID \u2192 BatchYear, Section, TotalStudents, DeptID):",
                     ["BatchID", "BatchYear", "Section", "TotalStudents", "DeptID", "DeptName"],
                     [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in batch_flat]),
                    ("R2 = STUDENT_ROSTER (StudentID \u2192 StudentName; carried by STUDENT in the final design):",
                     ["StudentID", "StudentName", "BatchID"],
                     [[r[6], r[7], r[0]] for r in batch_flat]),
                ],
            },
            {
                "label": "Step 2 \u2014 3NF: remove the transitive dependency BatchID \u2192 DeptID \u2192 DeptName",
                "stmt": "DeptName depends on DeptID, which depends on BatchID. Project DeptName out of R1; it merges into DEPARTMENT:",
                "tables": [
                    ("BATCH \u2014 final relation (5 records):",
                     ["BatchID", "BatchYear", "Section", "TotalStudents", "DeptID (FK)"],
                     [[r[0], r[1], r[2], r[3], r[4]] for r in batch_flat]),
                    ("(DeptID, DeptName) \u2014 merges into DEPARTMENT:",
                     ["DeptID", "DeptName"],
                     [["1", "Computer Science"], ["2", "Electronics & Comm."], ["3", "Mechanical Engg."], ["4", "Electrical Engg."], ["5", "Civil Engg."]]),
                ],
            },
        ],
        bcnf_note="DeptID is retained in BATCH as the foreign key to DEPARTMENT.",
    )

    # ---- 2.3 COMPANY ----
    relation_section(
        doc, 3, "COMPANY",
        "Stores companies where alumni work (the ALUMNI\u2013COMPANY works_at relationship). In the finalized ER diagram there is no COMPANY\u2013JOB relationship, so JOB carries no CompanyID.",
        "CompanyID is a single-attribute primary key, so all non-key attributes depend fully on it. No partial or transitive dependency exists \u2014 the relation is already in BCNF.",
        "COMPANY (CompanyID, CompanyName, Industry, CompanySize, Website, Headquarters)",
        [
            "CompanyID \u2192 CompanyName, Industry, CompanySize, Website, Headquarters",
        ],
        "CompanyID",
        ["CompanyID", "CompanyName", "Industry", "CompanySize", "Website", "Headquarters"],
        [
            ["101", "TCS", "IT Services", "500000+", "tcs.com", "Mumbai"],
            ["102", "Infosys", "IT Services", "300000+", "infosys.com", "Bengaluru"],
            ["103", "Google", "Technology", "100000+", "google.com", "Mountain View"],
            ["104", "Reliance", "Conglomerate", "200000+", "reliance.com", "Mumbai"],
            ["105", "Zoho", "Software", "15000", "zoho.com", "Chennai"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "All non-key attributes depend directly on CompanyID; no transitive dependency."],
            ["BCNF", "\u2713 Pass", "CompanyID is the only determinant and is a candidate key."],
        ],
        no_decomp_note="No decomposition required: single-attribute primary key, every determinant is a candidate key.",
    )

    # ---- 2.4 SKILL ----
    relation_section(
        doc, 4, "SKILL",
        "Stores skills that alumni can possess (the ALUMNI\u2013SKILL M:N relationship is resolved by ALUMNI_SKILL).",
        "SkillID is a single-attribute primary key. SkillName is also a candidate key. Every determinant is a candidate key, so the relation is already in BCNF.",
        "SKILL (SkillID, SkillName, SkillCategory, Description)",
        [
            "SkillID \u2192 SkillName, SkillCategory, Description",
            "SkillName \u2192 SkillID   (candidate key)",
        ],
        "SkillID (SkillName is an alternative candidate key)",
        ["SkillID", "SkillName", "SkillCategory", "Description"],
        [
            ["1", "Java", "Programming", "OOP and backend development"],
            ["2", "Python", "Programming", "Data analysis and automation"],
            ["3", "SQL", "Database", "Querying and database design"],
            ["4", "Communication", "Soft Skill", "Verbal and written communication"],
            ["5", "Project Management", "Management", "Planning and team coordination"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "No non-prime \u2192 non-prime dependency."],
            ["BCNF", "\u2713 Pass", "SkillID and SkillName are both candidate keys; every determinant is a candidate key."],
        ],
        no_decomp_note="No decomposition required: single-attribute primary key, all determinants are candidate keys.",
    )

    # ---- 2.5 ALUMNI ----
    alumni_final_headers = ["AlumniID", "FirstName", "LastName", "Email", "DateOfBirth", "Gender",
                            "Address_City", "Address_State", "Address_PinCode", "GraduationYear",
                            "DeptID", "BatchID", "CompanyID", "CurrentPosition", "LinkedInProfile", "IsActive"]
    alumni_final_rows = [
        ["1", "Aarav", "Mehta", "aarav.mehta@email.com", "2001-04-12", "M", "Chennai", "TN", "600001", "2023", "1", "1", "101", "Software Engineer", "in/aaravmehta", "TRUE"],
        ["2", "Priya", "Nair", "priya.nair@email.com", "2000-11-03", "F", "Bengaluru", "KA", "560001", "2023", "1", "2", "102", "Data Analyst", "in/priyanair", "TRUE"],
        ["3", "Rohan", "Gupta", "rohan.gupta@email.com", "2001-07-25", "M", "Mumbai", "MH", "400001", "2024", "2", "3", "103", "Product Manager", "in/rohangupta", "TRUE"],
        ["4", "Sneha", "Reddy", "sneha.reddy@email.com", "2002-01-19", "F", "Hyderabad", "TS", "500001", "2024", "3", "4", "104", "Systems Engineer", "in/snehareddy", "TRUE"],
        ["5", "Vikram", "Singh", "vikram.singh@email.com", "2002-09-30", "M", "Delhi", "DL", "110001", "2025", "4", "5", "105", "Analyst", "in/vikramsingh", "FALSE"],
    ]
    relation_section(
        doc, 5, "ALUMNI",
        "Main entity of the platform. Email is a single-valued attribute of ALUMNI (only PhoneNumbers is multivalued, handled by ALUMNI_PHONE). The flat relation initially carries DeptName, BatchYear and CompanyName (from the ER relationships); 3NF decomposition removes them so only the foreign keys DeptID, BatchID and CompanyID remain.",
        "AlumniID is a single-attribute primary key; Email is an alternative candidate key. Once the transitive dependencies are removed, every determinant is a candidate key \u2014 the relation is in BCNF.",
        "ALUMNI_flat (AlumniID, FirstName, LastName, Email, DateOfBirth, Gender, Address_City, Address_State, Address_PinCode, GraduationYear, DeptID, DeptName, BatchID, BatchYear, CompanyID, CompanyName, CurrentPosition, LinkedInProfile, IsActive)",
        [
            "AlumniID \u2192 FirstName, LastName, Email, DateOfBirth, Gender, Address_City, Address_State, Address_PinCode, GraduationYear, DeptID, BatchID, CompanyID, CurrentPosition, LinkedInProfile, IsActive",
            "Email \u2192 AlumniID   (candidate key)",
            "DeptID \u2192 DeptName      (transitive)",
            "BatchID \u2192 BatchYear    (transitive)",
            "CompanyID \u2192 CompanyName (transitive)",
        ],
        "AlumniID (Email is an alternative candidate key)",
        alumni_final_headers, alumni_final_rows,
        [
            ["1NF", "\u2713 Pass", "Composite attributes (Name, Address) are decomposed into atomic components; PhoneNumbers (multivalued) moved to ALUMNI_PHONE; Skills and Events moved to junction relations."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "Transitive dependencies DeptID \u2192 DeptName, BatchID \u2192 BatchYear, CompanyID \u2192 CompanyName removed by projection."],
            ["BCNF", "\u2713 Pass", "Determinants AlumniID and Email are candidate keys."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 3NF: remove the transitive dependency AlumniID \u2192 DeptID \u2192 DeptName",
                "stmt": "Project (DeptID, DeptName) out of the flat relation; it merges into DEPARTMENT:",
                "tables": [
                    ("(DeptID, DeptName) \u2014 merges into DEPARTMENT:",
                     ["DeptID", "DeptName"],
                     [["1", "Computer Science"], ["2", "Electronics & Comm."], ["3", "Mechanical Engg."], ["4", "Electrical Engg."], ["5", "Civil Engg."]]),
                ],
            },
            {
                "label": "Step 2 \u2014 3NF: remove the transitive dependency AlumniID \u2192 BatchID \u2192 BatchYear",
                "stmt": "Project (BatchID, BatchYear) out of the flat relation; it merges into BATCH:",
                "tables": [
                    ("(BatchID, BatchYear) \u2014 merges into BATCH:",
                     ["BatchID", "BatchYear"],
                     [["1", "2023"], ["2", "2023"], ["3", "2024"], ["4", "2024"], ["5", "2025"]]),
                ],
            },
            {
                "label": "Step 3 \u2014 3NF: remove the transitive dependency AlumniID \u2192 CompanyID \u2192 CompanyName",
                "stmt": "Project (CompanyID, CompanyName) out of the flat relation; it merges into COMPANY:",
                "tables": [
                    ("(CompanyID, CompanyName) \u2014 merges into COMPANY:",
                     ["CompanyID", "CompanyName"],
                     [["101", "TCS"], ["102", "Infosys"], ["103", "Google"], ["104", "Reliance"], ["105", "Zoho"]]),
                ],
            },
            {
                "label": "Step 4 \u2014 the final ALUMNI relation (only foreign keys remain)",
                "stmt": "After all three projections, ALUMNI keeps only DeptID, BatchID and CompanyID as foreign keys \u2014 the final relation below is what is implemented:",
                "tables": [
                    ("ALUMNI \u2014 final relation (5 records):", alumni_final_headers, alumni_final_rows),
                ],
                "font": 7.5,
            },
        ],
        bcnf_note="Multivalued attributes and M:N relationships are handled by separate relations: ALUMNI_PHONE, ALUMNI_SKILL, ALUMNI_EVENT.",
    )

    # ---- 2.6 STUDENT ----
    relation_section(
        doc, 6, "STUDENT",
        "Stores current students, who are the mentees in the MENTORSHIP relationship (MENTORSHIP \u2192 is_for \u2192 STUDENT). Email is a multivalued attribute of STUDENT, so it is handled by the separate STUDENT_EMAIL relation.",
        "StudentID is a single-attribute primary key. Because Email is multivalued, it is moved to its own relation STUDENT_EMAIL \u2014 so it is no longer a candidate key of STUDENT. After the transitive dependency is removed, every determinant is a candidate key \u2014 the relation is in BCNF.",
        "STUDENT_flat (StudentID, FirstName, LastName, Email, DeptID, DeptName, EnrollmentYear, CurrentSemester, CGPA)",
        [
            "StudentID \u2192 FirstName, LastName, DeptID, EnrollmentYear, CurrentSemester, CGPA",
            "Email \u2192\u2192 (multivalued \u2014 handled by STUDENT_EMAIL)",
            "DeptID \u2192 DeptName    (transitive)",
        ],
        "StudentID",
        ["StudentID", "FirstName", "LastName", "DeptID", "EnrollmentYear", "CurrentSemester", "CGPA"],
        [
            ["1", "Ananya", "Joshi", "1", "2024", "4", "8.9"],
            ["2", "Karthik", "Iyer", "2", "2024", "4", "8.4"],
            ["3", "Meera", "Pillai", "3", "2025", "2", "7.8"],
            ["4", "Arjun", "Desai", "4", "2025", "2", "9.1"],
            ["5", "Divya", "Menon", "5", "2023", "7", "8.2"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic; multivalued Email moved to STUDENT_EMAIL."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "Transitive dependency StudentID \u2192 DeptID \u2192 DeptName removed by projection; DeptID kept as FK."],
            ["BCNF", "\u2713 Pass", "StudentID is the only determinant and is a candidate key."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 1NF: remove the multivalued attribute Email",
                "stmt": "Email is multivalued, so it cannot stay as a single column. Project it into its own relation STUDENT_EMAIL:",
                "tables": [
                    ("STUDENT_EMAIL (StudentID, Email) \u2014 multivalued handler (some students have more than one e-mail):",
                     ["StudentID", "Email"],
                     [["1", "ananya.joshi@email.com"], ["1", "ananya.j@vit.ac.in"], ["2", "karthik.iyer@email.com"], ["3", "meera.pillai@email.com"], ["4", "arjun.desai@email.com"], ["5", "divya.menon@email.com"]]),
                ],
            },
            {
                "label": "Step 2 \u2014 3NF: remove the transitive dependency StudentID \u2192 DeptID \u2192 DeptName",
                "stmt": "Project (DeptID, DeptName) out of the flat relation; it merges into DEPARTMENT, and STUDENT keeps DeptID as a foreign key:",
                "tables": [
                    ("STUDENT \u2014 final relation (5 records):",
                     ["StudentID", "FirstName", "LastName", "DeptID (FK)", "EnrollmentYear", "CurrentSemester", "CGPA"],
                     [
                        ["1", "Ananya", "Joshi", "1", "2024", "4", "8.9"],
                        ["2", "Karthik", "Iyer", "2", "2024", "4", "8.4"],
                        ["3", "Meera", "Pillai", "3", "2025", "2", "7.8"],
                        ["4", "Arjun", "Desai", "4", "2025", "2", "9.1"],
                        ["5", "Divya", "Menon", "5", "2023", "7", "8.2"],
                     ]),
                    ("(DeptID, DeptName) \u2014 merges into DEPARTMENT:",
                     ["DeptID", "DeptName"],
                     [["1", "Computer Science"], ["2", "Electronics & Comm."], ["3", "Mechanical Engg."], ["4", "Electrical Engg."], ["5", "Civil Engg."]]),
                ],
            },
        ],
        bcnf_note="STUDENT_EMAIL (StudentID, Email) handles the multivalued e-mail addresses of a student.",
    )

    # ---- 2.7 MENTORSHIP ----
    mentorship_final_headers = ["MentorshipID (PK)", "AlumniID (PK, FK)", "StudentID (PK, FK)", "StartDate", "EndDate", "Status", "MentorshipArea", "Goals"]
    mentorship_final_rows = [
        ["1", "1", "1", "2025-01-10", "NULL", "Active", "Data Science", "Place in tech"],
        ["2", "2", "2", "2025-02-01", "NULL", "Active", "Career Guidance", "Resume review"],
        ["3", "3", "3", "2024-08-15", "2025-06-30", "Completed", "Web Development", "Full-stack skills"],
        ["4", "4", "4", "2025-03-20", "NULL", "Active", "Research", "Conference paper"],
        ["5", "5", "5", "2024-07-01", "2025-05-31", "Completed", "Entrepreneurship", "Startup guidance"],
    ]
    relation_section(
        doc, 7, "MENTORSHIP",
        "MENTORSHIP is a weak entity in the ER diagram. It is identified through the owner entity ALUMNI using the identifying (double-diamond) relationship HAS_MENTORSHIP, and it has total participation (double line). Its partial key is StartDate. As a weak entity, its relational mapping uses a composite primary key made of all three identifiers \u2014 (MentorshipID, StudentID, AlumniID) \u2014 because the mentorship is identified together by its owner (the alumnus mentor), the mentee (the student), and the mentorship instance. It connects one alumnus (mentor) to one student (mentee) \u2014 ALUMNI \u2192 HAS_MENTORSHIP \u2192 MENTORSHIP and MENTORSHIP \u2192 is_for \u2192 STUDENT.",
        "Because MENTORSHIP is a weak entity, the primary key is the composite key (MentorshipID, StudentID, AlumniID): AlumniID identifies the owner (the alumnus mentor), StudentID identifies the mentee, and MentorshipID identifies the particular mentorship instance. A composite key means partial dependencies are possible, so the relation must be checked for 2NF: AlumniID \u2192 AlumniName, AlumniCompany and StudentID \u2192 StudentName, StudentDept are partial dependencies (each is a proper subset of the key) and are removed by projection. After decomposition the only determinant is the composite key itself, which is a candidate key \u2014 the relation is in BCNF.",
        "MENTORSHIP_flat (MentorshipID, AlumniID, StudentID, StartDate, AlumniName, AlumniCompany, StudentName, StudentDept, EndDate, Status, MentorshipArea, Goals)",
        [
            "(MentorshipID, AlumniID, StudentID) \u2192 StartDate, EndDate, Status, MentorshipArea, Goals",
            "AlumniID \u2192 AlumniName, AlumniCompany   (partial dependency \u2014 AlumniID is a proper subset of the key)",
            "StudentID \u2192 StudentName, StudentDept    (partial dependency \u2014 StudentID is a proper subset of the key)",
        ],
        "(MentorshipID, StudentID, AlumniID) \u2014 composite primary key (weak-entity mapping)",
        mentorship_final_headers, mentorship_final_rows,
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic; each mentorship has a single StartDate, Status and Area."],
            ["2NF", "\u2713 Pass", "Partial dependencies AlumniID \u2192 AlumniName/AlumniCompany and StudentID \u2192 StudentName/StudentDept removed by projection (Steps 1\u20132)."],
            ["3NF", "\u2713 Pass", "After 2NF decomposition no non-prime attribute depends on another non-prime attribute."],
            ["BCNF", "\u2713 Pass", "The only determinant left is the composite key (MentorshipID, AlumniID, StudentID), a candidate key."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 2NF: remove the partial dependency AlumniID \u2192 AlumniName, AlumniCompany",
                "stmt": "AlumniID is a proper subset of the composite key (MentorshipID, AlumniID, StudentID). Project the mentor details out of the flat relation; they merge into ALUMNI:",
                "tables": [
                    ("(AlumniID, AlumniName, AlumniCompany) \u2014 merges into ALUMNI:",
                     ["AlumniID", "AlumniName", "AlumniCompany"],
                     [["1", "Aarav Mehta", "TCS"], ["2", "Priya Nair", "Infosys"], ["3", "Rohan Gupta", "Google"], ["4", "Sneha Reddy", "Reliance"], ["5", "Vikram Singh", "Zoho"]]),
                ],
            },
            {
                "label": "Step 2 \u2014 2NF: remove the partial dependency StudentID \u2192 StudentName, StudentDept",
                "stmt": "StudentID is a proper subset of the composite key (MentorshipID, AlumniID, StudentID). Project the mentee details out of the flat relation; they merge into STUDENT:",
                "tables": [
                    ("(StudentID, StudentName, StudentDept) \u2014 merges into STUDENT:",
                     ["StudentID", "StudentName", "StudentDept"],
                     [["1", "Ananya Joshi", "Computer Science"], ["2", "Karthik Iyer", "Electronics & Comm."], ["3", "Meera Pillai", "Mechanical Engg."], ["4", "Arjun Desai", "Electrical Engg."], ["5", "Divya Menon", "Civil Engg."]]),
                ],
            },
            {
                "label": "Step 3 \u2014 the final MENTORSHIP relation (composite key (MentorshipID, StudentID, AlumniID))",
                "stmt": "After both projections, MENTORSHIP keeps the composite primary key (MentorshipID, AlumniID, StudentID) with the remaining mentorship attributes:",
                "tables": [
                    ("MENTORSHIP \u2014 final relation (5 records):", mentorship_final_headers, mentorship_final_rows),
                ],
            },
        ],
        bcnf_note="Weak-entity mapping: AlumniID (owner) represents ALUMNI \u2192 HAS_MENTORSHIP \u2192 MENTORSHIP (identifying relationship, total participation); StudentID represents MENTORSHIP \u2192 is_for \u2192 STUDENT. StartDate is the partial key of the weak entity; the composite primary key is (MentorshipID, AlumniID, StudentID).",
    )

    # ---- 2.8 EVENT ----
    relation_section(
        doc, 8, "EVENT",
        "Stores events organized by alumni (ALUMNI \u2192 organizes \u2192 EVENT). The EVENT entity has the single-attribute key EventID, which derives all the event facts \u2014 so 2NF is automatically satisfied and needs no decomposition. The decomposition that is really required is the BCNF one: the organizer's name depends on OrganizerID, which is NOT a superkey of the relation, so a single key does not derive every attribute.",
        "EventID is a single-attribute primary key, so a partial dependency is impossible and 2NF holds without decomposition. The genuine violation is BCNF: OrganizerID \u2192 OrganizerName holds and OrganizerID is not a superkey of EVENT \u2014 so a real BCNF decomposition is needed. After it, every determinant is a candidate key \u2014 the relation is in BCNF.",
        "EVENT_flat (EventID, EventName, EventType, EventDate, Venue, OrganizerID, OrganizerName)",
        [
            "EventID \u2192 EventName, EventType, EventDate, Venue, OrganizerID   (single key derives the event facts)",
            "OrganizerID \u2192 OrganizerName   (non-superkey determinant \u2014 BCNF violation)",
        ],
        "EventID",
        ["EventID", "EventName", "EventType", "EventDate", "Venue", "OrganizerID"],
        [
            ["1", "Alumni Reunion 2025", "Reunion", "2025-06-15", "Main Auditorium", "1"],
            ["2", "AI Workshop", "Workshop", "2025-04-20", "Tech Hall", "2"],
            ["3", "Career Seminar", "Seminar", "2025-03-10", "Seminar Hall", "3"],
            ["4", "Startup Networking", "Networking", "2025-05-05", "Innovation Lab", "4"],
            ["5", "Freshers Meet 2025", "Networking", "2025-08-01", "Main Auditorium", "5"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key EventID \u2014 no partial dependency, so 2NF holds without decomposition."],
            ["3NF", "\u2713 Pass", "No non-prime \u2192 non-prime dependency (OrganizerID is an FK after the BCNF decomposition)."],
            ["BCNF", "\u2713 Pass", "Non-superkey determinant OrganizerID \u2192 OrganizerName removed by decomposition (Step 2); every remaining determinant is a candidate key."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 the flat relation (single key EventID, 5 rows)",
                "stmt": "The event facts repeat the organizer's name on every row \u2014 that is the redundancy the BCNF decomposition removes. There is no partial dependency here, so no 2NF decomposition is needed:",
                "tables": [
                    ("EVENT_flat \u2014 initial relation:",
                     ["EventID", "EventName", "EventType", "EventDate", "Venue", "OrganizerID", "OrganizerName"],
                     [
                        ["1", "Alumni Reunion 2025", "Reunion", "2025-06-15", "Main Auditorium", "1", "Aarav Mehta"],
                        ["2", "AI Workshop", "Workshop", "2025-04-20", "Tech Hall", "2", "Priya Nair"],
                        ["3", "Career Seminar", "Seminar", "2025-03-10", "Seminar Hall", "3", "Rohan Gupta"],
                        ["4", "Startup Networking", "Networking", "2025-05-05", "Innovation Lab", "4", "Sneha Reddy"],
                        ["5", "Freshers Meet 2025", "Networking", "2025-08-01", "Main Auditorium", "5", "Vikram Singh"],
                     ]),
                ],
            },
            {
                "label": "Step 2 \u2014 BCNF: decompose on the non-superkey determinant OrganizerID \u2192 OrganizerName",
                "stmt": "In EVENT_flat the key is EventID, but OrganizerID \u2192 OrganizerName holds and OrganizerID is NOT a superkey \u2014 a real BCNF violation. Apply the general algorithm (R1 = X \u222a A, R2 = R \u2212 A):",
                "tables": [
                    ("R1 = (OrganizerID, OrganizerName) \u2014 merges into ALUMNI:",
                     ["OrganizerID", "OrganizerName"],
                     [["1", "Aarav Mehta"], ["2", "Priya Nair"], ["3", "Rohan Gupta"], ["4", "Sneha Reddy"], ["5", "Vikram Singh"]]),
                    ("R2 = EVENT \u2014 final relation (5 records, OrganizerID kept as FK):",
                     ["EventID", "EventName", "EventType", "EventDate", "Venue", "OrganizerID (FK)"],
                     [
                        ["1", "Alumni Reunion 2025", "Reunion", "2025-06-15", "Main Auditorium", "1"],
                        ["2", "AI Workshop", "Workshop", "2025-04-20", "Tech Hall", "2"],
                        ["3", "Career Seminar", "Seminar", "2025-03-10", "Seminar Hall", "3"],
                        ["4", "Startup Networking", "Networking", "2025-05-05", "Innovation Lab", "4"],
                        ["5", "Freshers Meet 2025", "Networking", "2025-08-01", "Main Auditorium", "5"],
                     ]),
                ],
            },
        ],
        bcnf_note="For EVENT the single key EventID does derive all the event facts (2NF is automatic), but it does NOT derive the organizer's name \u2014 that is the BCNF issue, fixed by the decomposition above. OrganizerID is retained in EVENT as the foreign key to ALUMNI.",
    )

    # ---- 2.9 DONATION ----
    relation_section(
        doc, 9, "DONATION",
        "Tracks donations made by alumni (ALUMNI \u2192 makes \u2192 DONATION).",
        "DonationID is a single-attribute primary key. The donor detail chain is a transitive dependency removed by projection; the only determinant left is DonationID \u2014 the relation is in BCNF.",
        "DONATION_flat (DonationID, DonorID, DonorName, DonorEmail, Amount, DonationDate, PaymentMethod)",
        [
            "DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod",
            "DonorID \u2192 DonorName, DonorEmail   (transitive)",
        ],
        "DonationID",
        ["DonationID", "DonorID", "Amount", "DonationDate", "PaymentMethod"],
        [
            ["1", "1", "50000", "2025-01-10", "Online"],
            ["2", "2", "25000", "2025-02-14", "Online"],
            ["3", "3", "100000", "2025-03-01", "Check"],
            ["4", "4", "15000", "2025-04-22", "Cash"],
            ["5", "5", "75000", "2025-06-30", "Online"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic; each donation has a single Amount and PaymentMethod."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "Transitive dependency DonationID \u2192 DonorID \u2192 DonorName removed; DonorID kept as FK."],
            ["BCNF", "\u2713 Pass", "DonationID is the only determinant and is a candidate key."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 3NF: remove the transitive dependency DonationID \u2192 DonorID \u2192 DonorName",
                "stmt": "Project (DonorID, DonorName, DonorEmail) out of the flat relation; it merges into ALUMNI:",
                "tables": [
                    ("DONATION \u2014 final relation (5 records):",
                     ["DonationID", "DonorID (FK)", "Amount", "DonationDate", "PaymentMethod"],
                     [
                        ["1", "1", "50000", "2025-01-10", "Online"],
                        ["2", "2", "25000", "2025-02-14", "Online"],
                        ["3", "3", "100000", "2025-03-01", "Check"],
                        ["4", "4", "15000", "2025-04-22", "Cash"],
                        ["5", "5", "75000", "2025-06-30", "Online"],
                     ]),
                    ("(DonorID, DonorName, DonorEmail) \u2014 merges into ALUMNI:",
                     ["DonorID", "DonorName", "DonorEmail"],
                     [["1", "Aarav Mehta", "aarav.mehta@email.com"], ["2", "Priya Nair", "priya.nair@email.com"], ["3", "Rohan Gupta", "rohan.gupta@email.com"], ["4", "Sneha Reddy", "sneha.reddy@email.com"], ["5", "Vikram Singh", "vikram.singh@email.com"]]),
                ],
            },
        ],
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "In DONATION the only FD is DonationID \u2192 (all attributes), and DonationID is the candidate key. The left side is always a superkey, so no BCNF-violating FD exists \u2014 the general BCNF decomposition algorithm terminates immediately with no split.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod", "Yes \u2014 DonationID is the candidate key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    # ---- 2.10 JOB ----
    relation_section(
        doc, 10, "JOB",
        "Stores job opportunities posted by alumni (ALUMNI \u2192 posts \u2192 JOB). In the finalized ER diagram there is no COMPANY\u2013JOB relationship, so JOB contains no CompanyID.",
        "JobID is a single-attribute primary key. The poster detail chain is a transitive dependency removed by projection; the only determinant left is JobID \u2014 the relation is in BCNF.",
        "JOB_flat (JobID, JobTitle, JobType, Salary, PostedBy, FirstName, LastName, Email, CurrentPosition)",
        [
            "JobID \u2192 JobTitle, JobType, Salary, PostedBy",
            "PostedBy \u2192 FirstName, LastName, Email, CurrentPosition   (transitive \u2014 these are ALUMNI's own attributes, carried in the flat relation)",
        ],
        "JobID",
        ["JobID", "JobTitle", "JobType", "Salary", "PostedBy"],
        [
            ["1", "Software Engineer", "Full-Time", "15-20 LPA", "1"],
            ["2", "Data Analyst", "Full-Time", "10-15 LPA", "2"],
            ["3", "Web Developer Intern", "Internship", "5 LPA", "3"],
            ["4", "Project Manager", "Full-Time", "25-30 LPA", "4"],
            ["5", "ML Engineer", "Contract", "20-25 LPA", "5"],
        ],
        [
            ["1NF", "\u2713 Pass", "All attributes are atomic; each job has a single JobType and Salary."],
            ["2NF", "\u2713 Pass", "Single-attribute primary key \u2014 no partial dependency."],
            ["3NF", "\u2713 Pass", "Transitive dependency JobID \u2192 PostedBy \u2192 FirstName removed; PostedBy kept as FK."],
            ["BCNF", "\u2713 Pass", "JobID is the only determinant and is a candidate key."],
        ],
        decomp=[
            {
                "label": "Step 1 \u2014 3NF: remove the transitive dependency JobID \u2192 PostedBy \u2192 FirstName",
                "stmt": "Project (PostedBy, FirstName, LastName, Email, CurrentPosition) out of the flat relation \u2014 these are ALUMNI's own attributes, so the projection merges back into ALUMNI; JOB keeps only PostedBy as the foreign key:",
                "tables": [
                    ("JOB \u2014 final relation (5 records):",
                     ["JobID", "JobTitle", "JobType", "Salary", "PostedBy (FK)"],
                     [
                        ["1", "Software Engineer", "Full-Time", "15-20 LPA", "1"],
                        ["2", "Data Analyst", "Full-Time", "10-15 LPA", "2"],
                        ["3", "Web Developer Intern", "Internship", "5 LPA", "3"],
                        ["4", "Project Manager", "Full-Time", "25-30 LPA", "4"],
                        ["5", "ML Engineer", "Contract", "20-25 LPA", "5"],
                     ]),
                    ("(PostedBy \u2192 FirstName, LastName, Email, CurrentPosition) \u2014 merges into ALUMNI:",
                     ["PostedBy", "FirstName", "LastName", "Email", "CurrentPosition"],
                     [["1", "Aarav", "Mehta", "aarav.mehta@email.com", "Software Engineer"], ["2", "Priya", "Nair", "priya.nair@email.com", "Data Analyst"], ["3", "Rohan", "Gupta", "rohan.gupta@email.com", "Product Manager"], ["4", "Sneha", "Reddy", "sneha.reddy@email.com", "Systems Engineer"], ["5", "Vikram", "Singh", "vikram.singh@email.com", "Analyst"]]),
                ],
            },
        ],
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "In JOB the only FD is JobID \u2192 (all attributes), and JobID is the candidate key. The left side is always a superkey, so no BCNF-violating FD exists \u2014 no BCNF split is required.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["JobID \u2192 JobTitle, JobType, Salary, PostedBy", "Yes \u2014 JobID is the candidate key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    # ---- 2.11 ALUMNI_SKILL ----
    relation_section(
        doc, 11, "ALUMNI_SKILL (Junction Relation)",
        "Resolves the M:N ALUMNI\u2013SKILL relationship. It has no non-key attributes.",
        "The composite primary key (AlumniID, SkillID) is the only determinant and it is the full key, so no partial, transitive, or non-superkey dependency exists \u2014 the relation is already in BCNF.",
        "ALUMNI_SKILL (AlumniID, SkillID)",
        ["(AlumniID, SkillID) \u2192 \u2205   (no non-key attributes)"],
        "(AlumniID, SkillID) \u2014 composite primary key",
        ["AlumniID", "SkillID"],
        [["1", "1"], ["1", "3"], ["2", "2"], ["3", "1"], ["5", "3"]],
        [
            ["1NF", "\u2713 Pass", "All values are atomic."],
            ["2NF", "\u2713 Pass", "No non-key attribute exists, so a partial dependency is impossible."],
            ["3NF", "\u2713 Pass", "No non-key attribute exists, so a transitive dependency is impossible."],
            ["BCNF", "\u2713 Pass", "The only determinant is the full composite key, a candidate key."],
        ],
        no_decomp_note="No decomposition required: the full composite key is the only determinant, so the relation is already in BCNF.",
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "The only FD has the full composite key on the left, so the left side is always a superkey \u2014 the general BCNF decomposition algorithm finds no violating FD and no split is made.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["(AlumniID, SkillID) \u2192 \u2205", "Yes \u2014 (AlumniID, SkillID) is the composite key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    # ---- 2.12 ALUMNI_EVENT ----
    relation_section(
        doc, 12, "ALUMNI_EVENT (Junction Relation)",
        "Resolves the M:N ALUMNI\u2013EVENT (attends) relationship. It has no non-key attributes.",
        "The composite primary key (AlumniID, EventID) is the only determinant and it is the full key \u2014 so the relation is already in BCNF.",
        "ALUMNI_EVENT (AlumniID, EventID)",
        ["(AlumniID, EventID) \u2192 \u2205   (no non-key attributes)"],
        "(AlumniID, EventID) \u2014 composite primary key",
        ["AlumniID", "EventID"],
        [["1", "1"], ["1", "2"], ["2", "1"], ["3", "3"], ["4", "4"]],
        [
            ["1NF", "\u2713 Pass", "All values are atomic."],
            ["2NF", "\u2713 Pass", "No non-key attribute exists, so a partial dependency is impossible."],
            ["3NF", "\u2713 Pass", "No non-key attribute exists, so a transitive dependency is impossible."],
            ["BCNF", "\u2713 Pass", "The only determinant is the full composite key, a candidate key."],
        ],
        no_decomp_note="No decomposition required: the full composite key is the only determinant, so the relation is already in BCNF.",
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "The only FD has the full composite key (AlumniID, EventID) on the left, so the left side is always a superkey \u2014 no BCNF-violating FD exists and no split is made.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["(AlumniID, EventID) \u2192 \u2205", "Yes \u2014 (AlumniID, EventID) is the composite key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    # ---- 2.13 ALUMNI_PHONE ----
    relation_section(
        doc, 13, "ALUMNI_PHONE (Multivalued Attribute)",
        "Handles the multivalued PhoneNumbers attribute of ALUMNI in the ER diagram.",
        "The composite primary key (AlumniID, PhoneNumber) is the only determinant and it is the full key \u2014 the relation is already in BCNF.",
        "ALUMNI_PHONE (AlumniID, PhoneNumber)",
        ["(AlumniID, PhoneNumber) \u2192 \u2205   (no non-key attributes)"],
        "(AlumniID, PhoneNumber) \u2014 composite primary key",
        ["AlumniID", "PhoneNumber"],
        [["1", "+91-9840012345"], ["1", "+91-9940012345"], ["2", "+91-9880012345"], ["3", "+91-9900012345"], ["4", "+91-9790012345"]],
        [
            ["1NF", "\u2713 Pass", "All values are atomic."],
            ["2NF", "\u2713 Pass", "No non-key attribute exists, so a partial dependency is impossible."],
            ["3NF", "\u2713 Pass", "No non-key attribute exists, so a transitive dependency is impossible."],
            ["BCNF", "\u2713 Pass", "The only determinant is the full composite key, a candidate key."],
        ],
        no_decomp_note="No decomposition required: the full composite key is the only determinant, so the relation is already in BCNF.",
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "The only FD has the full composite key on the left, so the left side is always a superkey \u2014 the general BCNF decomposition algorithm finds no violating FD and no split is made.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["(AlumniID, PhoneNumber) \u2192 \u2205", "Yes \u2014 (AlumniID, PhoneNumber) is the composite key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    # ---- 2.14 STUDENT_EMAIL ----
    relation_section(
        doc, 14, "STUDENT_EMAIL (Multivalued Attribute)",
        "Handles the multivalued e-mail addresses of STUDENT in the ER design.",
        "The composite primary key (StudentID, Email) is the only determinant and it is the full key \u2014 the relation is already in BCNF.",
        "STUDENT_EMAIL (StudentID, Email)",
        ["(StudentID, Email) \u2192 \u2205   (no non-key attributes)"],
        "(StudentID, Email) \u2014 composite primary key",
        ["StudentID", "Email"],
        [["1", "ananya.joshi@email.com"], ["1", "ananya.j@vit.ac.in"], ["2", "karthik.iyer@email.com"], ["3", "meera.pillai@email.com"], ["4", "arjun.desai@email.com"]],
        [
            ["1NF", "\u2713 Pass", "All values are atomic."],
            ["2NF", "\u2713 Pass", "No non-key attribute exists, so a partial dependency is impossible."],
            ["3NF", "\u2713 Pass", "No non-key attribute exists, so a transitive dependency is impossible."],
            ["BCNF", "\u2713 Pass", "The only determinant is the full composite key, a candidate key."],
        ],
        no_decomp_note="No decomposition required: the full composite key is the only determinant, so the relation is already in BCNF.",
        bcnf_decomp=[
            {
                "label": "BCNF check \u2014 for each FD X \u2192 A, is X a superkey?",
                "stmt": "The only FD has the full composite key on the left, so the left side is always a superkey \u2014 the general BCNF decomposition algorithm finds no violating FD and no split is made.",
                "tables": [
                    ("Determinant check:",
                     ["Functional Dependency", "Left side is a superkey?", "BCNF violation?"],
                     [["(StudentID, Email) \u2192 \u2205", "Yes \u2014 (StudentID, Email) is the composite key", "No \u2014 relation stays as it is"]]),
                ],
            },
        ],
    )

    page_break(doc)

    # ================= 3. SUMMARY =================
    heading(doc, "3. Normalization Summary", 1)
    para(doc, "All 14 relations of the finalized design, with the normal form each satisfies. Every relation carries five sample records, so the design can be implemented and queried directly.")
    add_table(
        doc,
        ["Relation", "1NF", "2NF", "3NF", "BCNF", "Type"],
        [
            ["DEPARTMENT", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["BATCH", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["COMPANY", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["ALUMNI", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["STUDENT", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["MENTORSHIP", "\u2713", "\u2713", "\u2713", "\u2713", "Weak entity"],
            ["EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["DONATION", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["JOB", "\u2713", "\u2713", "\u2713", "\u2713", "Core entity"],
            ["ALUMNI_SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "M:N junction relation"],
            ["ALUMNI_EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "M:N junction relation"],
            ["ALUMNI_PHONE", "\u2713", "\u2713", "\u2713", "\u2713", "Multivalued attribute"],
            ["STUDENT_EMAIL", "\u2713", "\u2713", "\u2713", "\u2713", "Multivalued attribute"],
        ],
        font_size=9,
        center_cols={1, 2, 3, 4},
    )
    doc.add_paragraph()
    p = para(doc, "Result: all 14 relations are in BCNF under the primary keys and functional dependencies stated in this report. No further normalization is required.", bold=True, color=GREEN)

    # ================= 4. LOSSLESS JOIN =================
    heading(doc, "4. Lossless Join and Dependency Preservation", 1)
    para(doc, "Every decomposition in this report is by projection on a violating dependency X \u2192 A: R1 = X \u222a A and R2 = R \u2212 A. Such a decomposition always has the lossless (non-additive) join property \u2014 the natural join of the pieces reconstructs the original relation exactly, with no spurious tuples \u2014 because the common attribute X is a superkey of R1.")
    para(doc, "Example \u2014 ALUMNI:", space_after=2)
    code(doc, "Original: ALUMNI_flat (AlumniID, ..., DeptID, DeptName, ...)")
    code(doc, "Decomposed:  ALUMNI (AlumniID, ..., DeptID)  and  DEPARTMENT (DeptID, DeptName)")
    code(doc, "Natural join ALUMNI \u22C8 DEPARTMENT = original \u2713  (lossless)")
    doc.add_paragraph()
    para(doc, "Dependency preservation: after decomposition, every functional dependency can still be checked within a single relation (or through the foreign key that replaces it), so no join is needed merely to verify a dependency.")

    doc.save(OUT)
    print("Saved:", OUT)


if __name__ == "__main__":
    build_document()
