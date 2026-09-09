#!/usr/bin/env python3
"""Generate Normalization diagram showing progression from UNF to BCNF."""

import xml.sax.saxutils as saxutils

def esc(s):
    return saxutils.escape(s, {'"': '&quot;'})

# Colors
C_HEADER = "#4472C4"
C_HEADER_TEXT = "#FFFFFF"
C_1NF = "#E8F4FD"  # Light blue
C_2NF = "#D5E8D4"  # Light green
C_3NF = "#FFE6CC"  # Light orange
C_BCNF = "#F8CECC"  # Light red/pink
C_TEXT = "#000000"

cells = []
cid = 100

def nid():
    global cid
    cid += 1
    return str(cid)

def add_cell(id, value, style, x, y, w, h, parent="1"):
    cells.append(
        f'        <mxCell id="{id}" value="{esc(value)}" style="{esc(style)}" '
        f'vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" '
        f'width="{w}" height="{h}" as="geometry"/></mxCell>'
    )

def add_arrow(id, src, tgt, style, parent="1"):
    cells.append(
        f'        <mxCell id="{id}" style="{esc(style)}" '
        f'edge="1" source="{src}" target="{tgt}" parent="{parent}">'
        f'<mxGeometry relative="1" as="geometry"/></mxCell>'
    )

# Title
add_cell("title",
    '<b style="font-size:28px;">Normalization Process</b>'
    '<br><b style="font-size:18px;">Alumni Network and Engagement Platform</b>',
    "text;html=1;align=center;verticalAlign=middle;resizable=0;"
    "points=[];autosize=1;strokeColor=none;fillColor=none;",
    600, 20, 700, 60)

# ================================================================
# ALUMNI TABLE NORMALIZATION
# ================================================================

# UNF (Unnormalized)
unf_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;"
             f"strokeColor=#000000;strokeWidth=2;"
             f"fontColor={C_TEXT};fontSize=11;"
             f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("unf_alumni", 
    '<b style="font-size:14px;">UNF (Unnormalized)</b><br><br>'
    '<b>ALUMNI</b>(<u>AlumniID</u>, FirstName, LastName, Email, '
    '<b style="color:red;">Phone1, Phone2, Phone3</b>, '
    'Address, GraduationYear, DeptID, BatchID, CompanyID, ...)<br><br>'
    '<b style="color:red;">Problems:</b><br>'
    '• Repeating group (multiple phones)<br>'
    '• Composite attribute (Address)<br>'
    '• Derived attributes stored',
    unf_style, 50, 120, 350, 200)

# 1NF
one_nf_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_1NF};"
                f"strokeColor=#000000;strokeWidth=2;"
                f"fontColor={C_TEXT};fontSize=11;"
                f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("one_nf_alumni",
    '<b style="font-size:14px;">1NF (First Normal Form)</b><br><br>'
    '<b>ALUMNI</b>(<u>AlumniID</u>, FirstName, LastName, Email, '
    'DateOfBirth, Gender, <b>Address_City, Address_State, Address_PinCode</b>, '
    'GraduationYear, DeptID, BatchID, CompanyID, ...)<br><br>'
    '<b>ALUMNI_PHONE</b>(<u>AlumniID</u>, <u>PhoneNumber</u>)<br><br>'
    '<b style="color:green;">Fixed:</b><br>'
    '• Repeating groups → New table<br>'
    '• Composite → Decomposed<br>'
    '• Derived → Removed',
    one_nf_style, 450, 120, 380, 200)

# Arrow UNF → 1NF
add_arrow("unf_to_1nf", "unf_alumni", "one_nf_alumni",
    "html=1;strokeWidth=2;strokeColor=#000000;endArrow=blockThin;startArrow=none;"
    "labelBackgroundColor=none;fontSize=10;fontStyle=1;fontColor=#CC0000;")

# 2NF
two_nf_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_2NF};"
                f"strokeColor=#000000;strokeWidth=2;"
                f"fontColor={C_TEXT};fontSize=11;"
                f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("two_nf_alumni",
    '<b style="font-size:14px;">2NF (Second Normal Form)</b><br><br>'
    '<b>ALUMNI</b>(<u>AlumniID</u>, FirstName, LastName, Email, ...)<br><br>'
    '<b style="color:green;">✓ Single attribute PK</b><br>'
    '<b style="color:green;">✓ No partial dependencies</b><br><br>'
    'All non-key attributes depend fully on AlumniID',
    two_nf_style, 880, 120, 300, 200)

# Arrow 1NF → 2NF
add_arrow("1nf_to_2nf", "one_nf_alumni", "two_nf_alumni",
    "html=1;strokeWidth=2;strokeColor=#000000;endArrow=blockThin;startArrow=none;"
    "labelBackgroundColor=none;fontSize=10;fontStyle=1;fontColor=#CC0000;")

# 3NF
three_nf_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_3NF};"
                  f"strokeColor=#000000;strokeWidth=2;"
                  f"fontColor={C_TEXT};fontSize=11;"
                  f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("three_nf_alumni",
    '<b style="font-size:14px;">3NF (Third Normal Form)</b><br><br>'
    '<b>ALUMNI</b>(<u>AlumniID</u>, FirstName, LastName, Email, ...)<br><br>'
    '<b style="color:green;">✓ No transitive dependencies</b><br><br>'
    'DeptName → DeptID (FK reference)<br>'
    'BatchYear → BatchID (FK reference)<br>'
    'CompanyName → CompanyID (FK reference)',
    three_nf_style, 1230, 120, 300, 200)

# Arrow 2NF → 3NF
add_arrow("2nf_to_3nf", "two_nf_alumni", "three_nf_alumni",
    "html=1;strokeWidth=2;strokeColor=#000000;endArrow=blockThin;startArrow=none;"
    "labelBackgroundColor=none;fontSize=10;fontStyle=1;fontColor=#CC0000;")

# BCNF
bcnf_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_BCNF};"
              f"strokeColor=#000000;strokeWidth=2;"
              f"fontColor={C_TEXT};fontSize=11;"
              f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("bcnf_alumni",
    '<b style="font-size:14px;">BCNF (Boyce-Codd Normal Form)</b><br><br>'
    '<b>ALUMNI</b>(<u>AlumniID</u>, FirstName, LastName, Email, ...)<br><br>'
    '<b style="color:green;">✓ Every determinant is a candidate key</b><br><br>'
    'Candidate Keys:<br>'
    '• AlumniID<br>'
    '• Email<br><br>'
    '<b style="color:green;font-weight:bold;">ALUMNI is in BCNF ✓</b>',
    bcnf_style, 1580, 120, 300, 200)

# Arrow 3NF → BCNF
add_arrow("3nf_to_bcnf", "three_nf_alumni", "bcnf_alumni",
    "html=1;strokeWidth=2;strokeColor=#000000;endArrow=blockThin;startArrow=none;"
    "labelBackgroundColor=none;fontSize=10;fontStyle=1;fontColor=#CC0000;")

# ================================================================
# JUNCTION TABLE NORMALIZATION
# ================================================================

# ALUMNI_SKILL
add_cell("alumni_skill_norm",
    '<b style="font-size:14px;">ALUMNI_SKILL (Junction Table)</b><br><br>'
    '<b>ALUMNI_SKILL</b>(<u>AlumniID</u>, <u>SkillID</u>)<br><br>'
    '<b>Functional Dependencies:</b><br>'
    '(AlumniID, SkillID) → ∅<br><br>'
    '<b>Candidate Key:</b> (AlumniID, SkillID)<br><br>'
    '<b style="color:green;">✓ 1NF</b> - Atomic values<br>'
    '<b style="color:green;">✓ 2NF</b> - No partial deps<br>'
    '<b style="color:green;">✓ 3NF</b> - No transitive deps<br>'
    '<b style="color:green;">✓ BCNF</b> - Determinant is candidate key',
    one_nf_style, 50, 400, 350, 250)

# ALUMNI_EVENT
add_cell("alumni_event_norm",
    '<b style="font-size:14px;">ALUMNI_EVENT (Junction Table)</b><br><br>'
    '<b>ALUMNI_EVENT</b>(<u>AlumniID</u>, <u>EventID</u>, RegistrationDate)<br><br>'
    '<b>Functional Dependencies:</b><br>'
    '(AlumniID, EventID) → RegistrationDate<br><br>'
    '<b>Candidate Key:</b> (AlumniID, EventID)<br><br>'
    '<b style="color:green;">✓ 1NF</b> - Atomic values<br>'
    '<b style="color:green;">✓ 2NF</b> - Full key dependency<br>'
    '<b style="color:green;">✓ 3NF</b> - No transitive deps<br>'
    '<b style="color:green;">✓ BCNF</b> - Determinant is candidate key',
    two_nf_style, 450, 400, 350, 250)

# ALUMNI_PHONE
add_cell("alumni_phone_norm",
    '<b style="font-size:14px;">ALUMNI_PHONE (Multivalued)</b><br><br>'
    '<b>ALUMNI_PHONE</b>(<u>AlumniID</u>, <u>PhoneNumber</u>)<br><br>'
    '<b>Functional Dependencies:</b><br>'
    '(AlumniID, PhoneNumber) → ∅<br><br>'
    '<b>Candidate Key:</b> (AlumniID, PhoneNumber)<br><br>'
    '<b style="color:green;">✓ 1NF</b> - Atomic values<br>'
    '<b style="color:green;">✓ 2NF</b> - No partial deps<br>'
    '<b style="color:green;">✓ 3NF</b> - No transitive deps<br>'
    '<b style="color:green;">✓ BCNF</b> - Determinant is candidate key',
    three_nf_style, 850, 400, 350, 250)

# ================================================================
# SUMMARY TABLE
# ================================================================

summary_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;"
                 f"strokeColor=#000000;strokeWidth=2;"
                 f"fontColor={C_TEXT};fontSize=10;"
                 f"verticalAlign=top;align=left;spacingLeft=5;spacingTop=5;")
add_cell("summary",
    '<b style="font-size:16px;">Normalization Summary</b><br><hr>'
    '<b>Table | 1NF | 2NF | 3NF | BCNF</b><br>'
    '──────────────────────────────────<br>'
    'DEPARTMENT | ✓ | ✓ | ✓ | ✓<br>'
    'BATCH | ✓ | ✓ | ✓ | ✓<br>'
    'COMPANY | ✓ | ✓ | ✓ | ✓<br>'
    'SKILL | ✓ | ✓ | ✓ | ✓<br>'
    'ALUMNI | ✓ | ✓ | ✓ | ✓<br>'
    'STUDENT | ✓ | ✓ | ✓ | ✓<br>'
    'EVENT | ✓ | ✓ | ✓ | ✓<br>'
    'DONATION | ✓ | ✓ | ✓ | ✓<br>'
    'JOB | ✓ | ✓ | ✓ | ✓<br>'
    'MENTORSHIP | ✓ | ✓ | ✓ | ✓<br>'
    'ALUMNI_SKILL | ✓ | ✓ | ✓ | ✓<br>'
    'ALUMNI_PHONE | ✓ | ✓ | ✓ | ✓<br>'
    'ALUMNI_EVENT | ✓ | ✓ | ✓ | ✓<br>'
    '<br><b style="color:green;font-weight:bold;">All tables in BCNF ✓</b>',
    summary_style, 50, 720, 400, 350)

# ================================================================
# LEGEND
# ================================================================

legend_style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF9E6;"
                f"strokeColor=#000000;strokeWidth=2;"
                f"fontColor={C_TEXT};fontSize=11;"
                f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;")
add_cell("legend",
    '<b style="font-size:14px;">Normalization Forms</b><br><hr><br>'
    '<b style="background-color:#E8F4FD;">1NF</b> - No repeating groups, atomic values<br><br>'
    '<b style="background-color:#D5E8D4;">2NF</b> - No partial dependencies<br><br>'
    '<b style="background-color:#FFE6CC;">3NF</b> - No transitive dependencies<br><br>'
    '<b style="background-color:#F8CECC;">BCNF</b> - Every determinant is a candidate key<br><br>'
    '<b>Key Concepts:</b><br>'
    '• <b>Partial Dependency:</b> Non-key attr depends on part of key<br>'
    '• <b>Transitive Dependency:</b> A→B→C (B depends on A, C depends on B)<br>'
    '• <b>Determinant:</b> Attribute that determines other attributes<br>'
    '• <b>Candidate Key:</b> Minimal superkey',
    legend_style, 500, 720, 400, 300)

# ================================================================
# ASSEMBLE XML
# ================================================================

xml_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<mxfile host="app.diagrams.net">',
    '  <diagram name="Normalization" id="normalization">',
    '    <mxGraphModel dx="100" dy="100" grid="1" gridSize="10" guides="1" '
    'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
    'pageWidth="2000" pageHeight="1100" htmlLabel="1">',
    '      <root>',
    '        <mxCell id="0"/>',
    '        <mxCell id="1" parent="0"/>',
]
xml_parts.extend(cells)
xml_parts.extend([
    '      </root>',
    '    </mxGraphModel>',
    '  </diagram>',
    '</mxfile>',
])

output = '\n'.join(xml_parts)

out_path = "/Users/dakshagarwal/dbms-project/laguna/diagrams/Normalization.drawio"
with open(out_path, 'w') as f:
    f.write(output)

print(f"✅ Generated Normalization Diagram: {out_path}")
print(f"   Size: {len(output)} bytes")
print()
print("Shows normalization process for:")
print("  • ALUMNI table (UNF → 1NF → 2NF → 3NF → BCNF)")
print("  • Junction tables (ALUMNI_SKILL, ALUMNI_EVENT)")
print("  • Multivalued table (ALUMNI_PHONE)")
print("  • Summary table showing all tables are in BCNF")
