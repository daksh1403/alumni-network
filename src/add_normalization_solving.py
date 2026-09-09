#!/usr/bin/env python3
"""
Add an actual "Normalization Solving" step-by-step block after every
sample-data table in Alumni_Network_Normalization_Corrected.docx.

Each block shows, with the REAL sample values:
  * the relation before normalization (unnormalized snapshot) where applicable
  * a per-normal-form verification (1NF -> 2NF -> 3NF -> BCNF) explaining
    why each form is satisfied, checked against the actual rows
  * the final BCNF conclusion

Idempotent: if a section already contains a "Normalization Solving" heading,
it is skipped.
"""

import shutil
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCX = "/Users/dakshagarwal/dbms-project/Alumni_Network_Normalization_Corrected.docx"
BACKUP = "/Users/dakshagarwal/dbms-project/Alumni_Network_Normalization_Corrected.bak.docx"

HEADER_FILL = "1F4E78"
ROW_FILL = "EEF5FB"
ACCENT = RGBColor(0x2E, 0x6B, 0x9E)


def set_cell_shading(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def style_cell(cell, text, bold=False, color=None, font_size=9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if bold else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(str(text))
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def make_table(headers, rows, font_size=9, col_widths=None):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    if col_widths:
        tblPr = table._tbl.tblPr
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        tblPr.append(layout)
        tblW = tblPr.find(qn("w:tblW"))
        if tblW is None:
            tblW = OxmlElement("w:tblW")
            tblPr.append(tblW)
        tblW.set(qn("w:w"), str(sum(col_widths)))
        tblW.set(qn("w:type"), "dxa")
        grid = table._tbl.find(qn("w:tblGrid"))
        for gc, w in zip(grid.findall(qn("w:gridCol")), col_widths):
            gc.set(qn("w:w"), str(w))
        for row in table.rows:
            for cell, w in zip(row.cells, col_widths):
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(qn("w:tcW"))
                if tcW is None:
                    tcW = OxmlElement("w:tcW")
                    tcPr.append(tcW)
                tcW.set(qn("w:w"), str(w))
                tcW.set(qn("w:type"), "dxa")

    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        set_cell_shading(cell, HEADER_FILL)
        style_cell(cell, h, bold=True, color="FFFFFF", font_size=font_size)

    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            if i % 2 == 0:
                set_cell_shading(cell, ROW_FILL)
            style_cell(cell, val, font_size=font_size)
    return table


def add_para(text, bold=False, size=10, italic=False, color=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return p


def insert_sequence(anchor_el, elements):
    """Insert a list of elements after anchor_el, in order, returning the last element."""
    cur = anchor_el
    for el in elements:
        cur.addnext(el)
        cur = el
    return cur


def build_solving_block(relation, fd_line, forms, before=None, after_note=None):
    """Return a list of body elements (paragraphs + table xml) for one solving block."""
    elems = []

    # Heading
    h = add_para(f"Normalization Solving \u2014 {relation} (step-by-step)", bold=True, size=11, color=ACCENT)
    elems.append(h._p)

    # Stated FD
    fd = add_para(f"Given FD:  {fd_line}", size=9, italic=True)
    elems.append(fd._p)

    # Before snapshot (only for relations with a real decomposition)
    if before:
        cap = add_para(before["caption"], bold=True, size=9)
        elems.append(cap._p)
        tbl = make_table(before["headers"], before["rows"], font_size=8, col_widths=before.get("widths"))
        elems.append(tbl._tbl)

    # Per-form verification
    for form, text in forms:
        p = add_para(f"{form}:  {text}", size=9)
        p.paragraph_format.left_indent = Pt(6)
        elems.append(p._p)

    if after_note:
        n = add_para(after_note, size=9, italic=True)
        elems.append(n._p)

    # Conclusion
    c = add_para(f"\u2713 Result: {relation} is in BCNF under the stated FDs.", bold=True, size=9, color=RGBColor(0x2C, 0x5F, 0x2D))
    elems.append(c._p)

    return elems


# ---------------------------------------------------------------------------
# Solving definitions per relation
# (relation, fd_line, [(form, explanation)], before-snapshot, after-note)
# ---------------------------------------------------------------------------
SOLVING = [
    (
        "DEPARTMENT",
        "DeptID \u2192 DeptName, DeptCode, HODName, EstablishedYear",
        [
            ("1NF", "Every cell holds one atomic value; no repeating groups exist in the sample rows."),
            ("2NF", "The key is the single attribute DeptID, so a partial dependency is impossible."),
            ("3NF", "DeptName, DeptCode, HODName, and EstablishedYear each depend directly on DeptID; no non-key attribute depends on another non-key attribute (DeptName and DeptCode are candidate keys, not transitive)."),
            ("BCNF", "The only determinant used is DeptID, which is a candidate key."),
        ],
    ),
    (
        "BATCH",
        "BatchID \u2192 BatchYear, Section, TotalStudents, DeptID",
        [
            ("1NF", "All attributes are atomic; each batch row has single values."),
            ("2NF", "Single-attribute key (BatchID); no partial dependency can exist."),
            ("3NF", "BatchYear, Section, and TotalStudents depend directly on BatchID. DeptID is a foreign key to DEPARTMENT, not a transitive dependency."),
            ("BCNF", "The only determinant is BatchID, a candidate key."),
        ],
    ),
    (
        "COMPANY",
        "CompanyID \u2192 CompanyName, Industry, CompanySize, Website, Headquarters",
        [
            ("1NF", "All attributes are atomic (no repeated company rows or lists)."),
            ("2NF", "Single-attribute key; no partial dependency."),
            ("3NF", "CompanyName, Industry, CompanySize, Website, and Headquarters depend directly on CompanyID; none depends on another non-key attribute."),
            ("BCNF", "The only determinant is CompanyID, a candidate key."),
        ],
    ),
    (
        "SKILL",
        "SkillID \u2192 SkillName, SkillCategory, Description",
        [
            ("1NF", "All attributes are atomic."),
            ("2NF", "Single-attribute key; no partial dependency."),
            ("3NF", "SkillName, SkillCategory, and Description depend directly on SkillID; no transitive dependency (SkillName is itself a candidate key)."),
            ("BCNF", "The only determinant used is SkillID, a candidate key."),
        ],
    ),
    (
        "ALUMNI",
        "AlumniID \u2192 FirstName, LastName, Email, DateOfBirth, Gender, Address_City, Address_State, Address_PinCode, GraduationYear, DeptID, BatchID, CompanyID, CurrentPosition, LinkedInProfile, IsActive",
        [
            ("1NF", "In the unnormalized form, each alumnus could have several phone numbers, skills, and attended events packed into one row. In the sample data these are separated into ALUMNI_PHONE, ALUMNI_SKILL, and ALUMNI_EVENT, so ALUMNI now holds only atomic values."),
            ("2NF", "The key is the single attribute AlumniID, so no partial dependency can occur."),
            ("3NF", "Department, Batch, and Company details are not stored here \u2014 DeptID, BatchID, and CompanyID are foreign keys to their own relations, so there is no transitive dependency on AlumniID."),
            ("BCNF", "Every determinant used is AlumniID (a candidate key); Email is also a candidate key."),
        ],
        {
            "caption": "Before 1NF \u2014 ALUMNI with repeating groups (phones, skills, events)",
            "headers": ["AlumniID", "Name", "PhoneNumbers", "Skills", "EventsAttended"],
            "rows": [
                ["1", "Aarav Mehta", "+91-9840012345, +91-9940012345", "Java, SQL", "Reunion2025, AI Workshop"],
                ["2", "Priya Nair", "+91-9880012345", "Python", "Reunion2025"],
                ["3", "Rohan Gupta", "+91-9900012345", "Java", "Career Seminar"],
                ["4", "Sneha Reddy", "+91-9790012345", "\u2014", "Startup Networking"],
                ["5", "Vikram Singh", "\u2014", "SQL", "\u2014"],
            ],
            "widths": [700, 1100, 2100, 1100, 2000],
        },
        "After 1NF: phones \u2192 ALUMNI_PHONE, skills \u2192 ALUMNI_SKILL, events \u2192 ALUMNI_EVENT; ALUMNI keeps only atomic columns.",
    ),
    (
        "STUDENT",
        "StudentID \u2192 FirstName, LastName, Email, DeptID, EnrollmentYear, CurrentSemester, CGPA",
        [
            ("1NF", "All attributes are atomic; Email is a single value (multiple emails are stored in STUDENT_EMAIL)."),
            ("2NF", "Single-attribute key (StudentID); no partial dependency."),
            ("3NF", "All non-key attributes depend directly on StudentID; DeptID is a foreign key to DEPARTMENT."),
            ("BCNF", "The only determinant is StudentID, a candidate key."),
        ],
        {
            "caption": "Before 1NF \u2014 STUDENT with multivalued Email",
            "headers": ["StudentID", "Name", "Emails"],
            "rows": [
                ["1", "Ananya Joshi", "ananya.joshi@email.com, ananya.j@vit.ac.in"],
                ["2", "Karthik Iyer", "karthik.iyer@email.com"],
                ["3", "Meera Pillai", "meera.pillai@email.com"],
                ["4", "Arjun Desai", "arjun.desai@email.com"],
                ["5", "Divya Menon", "divya.menon@email.com"],
            ],
            "widths": [700, 1200, 3100],
        },
        "After 1NF: the multivalued Email is moved to the STUDENT_EMAIL relation.",
    ),
    (
        "MENTORSHIP",
        "MentorshipID \u2192 AlumniID, StudentID, StartDate, EndDate, Status, MentorshipArea, Goals",
        [
            ("1NF", "All attributes are atomic; each mentorship row has one StartDate, one Status, one MentorshipArea."),
            ("2NF", "Single-attribute key (MentorshipID); no partial dependency."),
            ("3NF", "AlumniID and StudentID are foreign keys to ALUMNI and STUDENT; the remaining attributes depend directly on MentorshipID."),
            ("BCNF", "The only determinant is MentorshipID, a candidate key."),
        ],
    ),
    (
        "EVENT",
        "EventID \u2192 EventName, EventType, EventDate, Venue, OrganizerID",
        [
            ("1NF", "All attributes are atomic; each event has a single EventDate and Venue."),
            ("2NF", "Single-attribute key (EventID); no partial dependency."),
            ("3NF", "OrganizerID is a foreign key to ALUMNI; EventName, EventType, EventDate, and Venue depend directly on EventID."),
            ("BCNF", "The only determinant is EventID, a candidate key."),
        ],
    ),
    (
        "DONATION",
        "DonationID \u2192 DonorID, Amount, DonationDate, PaymentMethod",
        [
            ("1NF", "All attributes are atomic; each donation has a single Amount and PaymentMethod."),
            ("2NF", "Single-attribute key (DonationID); no partial dependency."),
            ("3NF", "DonorID is a foreign key to ALUMNI; Amount, DonationDate, and PaymentMethod depend directly on DonationID."),
            ("BCNF", "The only determinant is DonationID, a candidate key."),
        ],
    ),
    (
        "JOB",
        "JobID \u2192 JobTitle, JobType, Salary, PostedBy",
        [
            ("1NF", "All attributes are atomic; each job has a single JobType and Salary."),
            ("2NF", "Single-attribute key (JobID); no partial dependency."),
            ("3NF", "PostedBy is a foreign key to ALUMNI; JobTitle, JobType, and Salary depend directly on JobID. (The COMPANY\u2013JOB relationship has been excluded, so no CompanyID is present.)"),
            ("BCNF", "The only determinant is JobID, a candidate key."),
        ],
    ),
    (
        "ALUMNI_SKILL",
        "(AlumniID, SkillID) \u2192 (no non-key attributes)",
        [
            ("1NF", "The composite key values are atomic; there are no repeating groups."),
            ("2NF", "There are no non-key attributes, so a partial dependency cannot exist."),
            ("3NF", "There are no non-key attributes, so no transitive dependency."),
            ("BCNF", "The only determinant is the full composite key (AlumniID, SkillID), which is a candidate key."),
        ],
    ),
    (
        "ALUMNI_EVENT",
        "(AlumniID, EventID) \u2192 (no non-key attributes)",
        [
            ("1NF", "The composite key values are atomic."),
            ("2NF", "No non-key attributes exist, so no partial dependency."),
            ("3NF", "No non-key attributes exist, so no transitive dependency."),
            ("BCNF", "The only determinant is the full composite key (AlumniID, EventID), a candidate key."),
        ],
    ),
    (
        "ALUMNI_PHONE",
        "(AlumniID, PhoneNumber) \u2192 (no non-key attributes)",
        [
            ("1NF", "Each phone number is stored as one atomic value per row (e.g. +91-9840012345)."),
            ("2NF", "No non-key attributes exist, so no partial dependency."),
            ("3NF", "No non-key attributes exist, so no transitive dependency."),
            ("BCNF", "The only determinant is the full composite key (AlumniID, PhoneNumber), a candidate key."),
        ],
    ),
    (
        "STUDENT_EMAIL",
        "(StudentID, Email) \u2192 (no non-key attributes)",
        [
            ("1NF", "Each email address is stored as one atomic value per row."),
            ("2NF", "No non-key attributes exist, so no partial dependency."),
            ("3NF", "No non-key attributes exist, so no transitive dependency."),
            ("BCNF", "The only determinant is the full composite key (StudentID, Email), a candidate key."),
        ],
    ),
]


def main():
    global doc

    shutil.copy2(DOCX, BACKUP)
    print(f"Backup refreshed: {BACKUP}")

    doc = Document(DOCX)

    inserted = 0
    skipped = 0

    # Find each "Sample Data \u2014 X (5 records)" caption paragraph; the sample
    # table is the next element. We anchor the solving block to the check table
    # that follows the sample table (the 'Normal Form | Status | Reasoning'
    # table), so the solving block appears after the per-form check table.
    for p in list(doc.paragraphs):
        text = p.text
        if not text.startswith("Sample Data \u2014"):
            continue
        relation = text.replace("Sample Data \u2014 ", "").replace(" (5 records)", "").strip()

        # Skip if this section already has a solving block
        if any(pp.text.startswith(f"Normalization Solving \u2014 {relation}") for pp in doc.paragraphs):
            skipped += 1
            continue

        # Find the check table (Normal Form | Status | Reasoning) that follows
        # the sample table in document order.
        check_tbl_el = None
        cur = p._p.getnext()
        while cur is not None:
            if cur.tag == qn("w:tbl"):
                check_tbl_el = cur
                break
            cur = cur.getnext()
        if check_tbl_el is None:
            print(f"  !! no check table found after {text}")
            continue

        # Find matching solving definition
        solving = next((s for s in SOLVING if s[0] == relation), None)
        if solving is None:
            print(f"  !! no solving definition for {relation}")
            continue

        _, fd_line, forms, *rest = solving
        before = rest[0] if rest else None
        after_note = rest[1] if len(rest) > 1 else None

        elems = build_solving_block(relation, fd_line, forms, before, after_note)
        # Insert after the check table
        cur = check_tbl_el
        for el in elems:
            cur.addnext(el)
            cur = el
        inserted += 1
        print(f"  + solving block added after check table of {relation}")

    print(f"\nInserted {inserted} solving blocks, skipped {skipped} (already present).")
    doc.save(DOCX)
    print(f"Saved: {DOCX}")


if __name__ == "__main__":
    main()
