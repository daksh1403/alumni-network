#!/usr/bin/env python3
"""Generate Relational Schema diagram in drawio format.

Matches reference image style:
- Blue/purple table headers
- Underlined Primary Keys
- Red (FK) markers for Foreign Keys
- Relationship labels on connecting lines
- Clean left-to-right layout
"""

import xml.sax.saxutils as saxutils

def esc(s):
    return saxutils.escape(s, {'"': '&quot;'})

# Colors
C_HEADER = "#4472C4"  # Blue header
C_HEADER_TEXT = "#FFFFFF"  # White text
C_PK = "#000000"  # Black for PK (underlined)
C_FK = "#FF0000"  # Red for FK
C_ATTR = "#000000"  # Black for regular attributes
C_TABLE_BG = "#FFFFFF"  # White background
C_TABLE_BORDER = "#000000"  # Black border
C_REL_LABEL = "#FF6600"  # Orange for relationship labels
C_LINE = "#000000"  # Black lines

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

def add_edge(id, src, tgt, style, value="", parent="1",
             ex=None, ey=None, enx=None, eny=None):
    s = style
    if ex is not None:
        s += f'exitX={ex};exitY={ey};'
    if enx is not None:
        s += f'entryX={enx};entryY={eny};'
    cells.append(
        f'        <mxCell id="{id}" value="{esc(value)}" style="{esc(s)}" '
        f'edge="1" source="{src}" target="{tgt}" parent="{parent}">'
        f'<mxGeometry relative="1" as="geometry"/></mxCell>'
    )

def create_table(tid, name, attributes, x, y):
    """Create a table with header and attributes displayed horizontally.
    
    attributes: list of tuples (attr_name, is_pk, is_fk)
    """
    # Table dimensions
    header_h = 35
    attr_w = 140  # Width for each attribute column
    table_w = max(280, len(attributes) * attr_w + 20)  # Dynamic width based on attributes
    table_h = header_h + 30  # Header + one row for attributes
    
    # Header style - horizontal text
    header_style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_HEADER};"
                    f"strokeColor={C_TABLE_BORDER};strokeWidth=2;"
                    f"fontColor={C_HEADER_TEXT};fontSize=14;fontStyle=1;"
                    f"verticalAlign=middle;align=center;"
                    f"horizontal=1;writingMode=lr-tb;")
    
    # Add header
    add_cell(tid, f"<b>{name}</b>", header_style, x, y, table_w, header_h)
    
    # Add attributes horizontally (left to right)
    for i, (attr_name, is_pk, is_fk) in enumerate(attributes):
        attr_x = x + 10 + (i * attr_w)  # Position each attribute in columns
        attr_y = y + header_h
        attr_id = f"{tid}_attr_{i}"
        
        # Build attribute value - no FK marker, just underline for PK
        if is_pk:
            # PK - underlined
            value = f"<u>{attr_name}</u>"
            style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_TABLE_BG};"
                     f"strokeColor={C_TABLE_BORDER};strokeWidth=1;"
                     f"fontColor={C_PK};fontSize=10;"
                     f"verticalAlign=middle;align=center;"
                     f"textDecoration=underline;horizontal=1;writingMode=lr-tb;")
        else:
            # Regular attribute (no FK marker)
            value = attr_name
            style = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={C_TABLE_BG};"
                     f"strokeColor={C_TABLE_BORDER};strokeWidth=1;"
                     f"fontColor={C_ATTR};fontSize=10;"
                     f"verticalAlign=middle;align=center;"
                     f"horizontal=1;writingMode=lr-tb;")
        
        add_cell(attr_id, value, style, attr_x, attr_y, attr_w - 10, 30)
    
    # Return table info for connections
    return {
        'id': tid,
        'x': x,
        'y': y,
        'w': table_w,
        'h': table_h,
        'center_x': x + table_w / 2,
        'center_y': y + table_h / 2,
        'right_x': x + table_w,
        'left_x': x
    }

def add_relationship(src_table, tgt_table, label, src_side='right', tgt_side='left'):
    """Add a relationship line between two tables with label."""
    rid = nid()
    
    # Calculate connection points
    if src_side == 'right':
        src_x = src_table['right_x']
        src_y = src_table['center_y']
        ex = 1
        ey = 0.5
    elif src_side == 'left':
        src_x = src_table['left_x']
        src_y = src_table['center_y']
        ex = 0
        ey = 0.5
    elif src_side == 'bottom':
        src_x = src_table['center_x']
        src_y = src_table['y'] + src_table['h']
        ex = 0.5
        ey = 1
    else:  # top
        src_x = src_table['center_x']
        src_y = src_table['y']
        ex = 0.5
        ey = 0
    
    if tgt_side == 'right':
        enx = 1
        eny = 0.5
    elif tgt_side == 'left':
        enx = 0
        eny = 0.5
    elif tgt_side == 'bottom':
        enx = 0.5
        eny = 1
    else:  # top
        enx = 0.5
        eny = 0
    
    # Edge style
    style = (f"html=1;strokeColor={C_LINE};strokeWidth=2;"
             f"endArrow=none;startArrow=none;"
             f"fontColor={C_REL_LABEL};fontSize=12;fontStyle=1;"
             f"labelPosition=center;verticalLabelPosition=middle;"
             f"align=center;verticalAlign=bottom;")
    
    add_edge(rid, src_table['id'], tgt_table['id'], style, label,
             ex=ex, ey=ey, enx=enx, eny=eny)

# ================================================================
# BUILD THE DIAGRAM
# ================================================================

# Title
add_cell("title",
    '<b style="font-size:28px;">Relational Schema</b>'
    '<br><b style="font-size:18px;">Alumni Network and Engagement Platform</b>',
    "text;html=1;align=center;verticalAlign=middle;resizable=0;"
    "points=[];autosize=1;strokeColor=none;fillColor=none;",
    800, 20, 700, 60)

# ================================================================
# ROW 1: REFERENCE TABLES (spread out with more space)
# ================================================================

# DEPARTMENT
dept = create_table("t_dept", "DEPARTMENT", [
    ("DeptID", True, False),
    ("DeptName", False, False),
    ("DeptCode", False, False),
    ("HODName", False, False),
    ("EstablishedYear", False, False),
], 50, 50)

# BATCH (moved further right)
batch = create_table("t_batch", "BATCH", [
    ("BatchID", True, False),
    ("BatchYear", False, False),
    ("Section", False, False),
    ("TotalStudents", False, False),
    ("DeptID", False, True),
], 850, 50)

# COMPANY (FoundedYear removed - not in ER diagram)
company = create_table("t_company", "COMPANY", [
    ("CompanyID", True, False),
    ("CompanyName", False, False),
    ("Industry", False, False),
    ("CompanySize", False, False),
    ("Website", False, False),
    ("Headquarters", False, False),
], 1650, 50)

# SKILL (on second row)
skill = create_table("t_skill", "SKILL", [
    ("SkillID", True, False),
    ("SkillName", False, False),
    ("SkillCategory", False, False),
    ("Description", False, False),
], 50, 250)

# ================================================================
# ROW 2: MAIN TABLES (spread out vertically)
# ================================================================

# ALUMNI (Phone removed - in ALUMNI_PHONE)
alumni = create_table("t_alumni", "ALUMNI", [
    ("AlumniID", True, False),
    ("FirstName", False, False),
    ("LastName", False, False),
    ("Email", False, False),
    ("DateOfBirth", False, False),
    ("Gender", False, False),
    ("Address_City", False, False),
    ("Address_State", False, False),
    ("Address_PinCode", False, False),
    ("GraduationYear", False, False),
    ("DeptID", False, True),
    ("BatchID", False, True),
    ("CompanyID", False, True),
    ("CurrentPosition", False, False),
    ("LinkedInProfile", False, False),
    ("IsActive", False, False),
], 50, 450)

# STUDENT (Only attributes in ER diagram)
student = create_table("t_student", "STUDENT", [
    ("StudentID", True, False),
    ("FirstName", False, False),
    ("LastName", False, False),
    ("Email", False, False),
    ("EnrollmentYear", False, False),
    ("DeptID", False, True),
    ("CurrentSemester", False, False),
    ("CGPA", False, False),
], 2500, 50)

# EVENT (moved to new position)
event = create_table("t_event", "EVENT", [
    ("EventID", True, False),
    ("EventName", False, False),
    ("EventType", False, False),
    ("EventDate", False, False),
    ("Venue", False, False),
    ("OrganizerID", False, True),
], 50, 700)

# DONATION
donation = create_table("t_donation", "DONATION", [
    ("DonationID", True, False),
    ("DonorID", False, True),
    ("Amount", False, False),
    ("DonationDate", False, False),
    ("PaymentMethod", False, False),
], 850, 700)

# JOB
job = create_table("t_job", "JOB", [
    ("JobID", True, False),
    ("JobTitle", False, False),
    ("JobType", False, False),
    ("Salary", False, False),
    ("CompanyID", False, True),
    ("PostedBy", False, True),
], 1650, 700)

# ================================================================
# ROW 3: WEAK & JUNCTION TABLES (bottom row)
# ================================================================

# MENTORSHIP (Weak Entity - MentorshipID as PK)
mentorship = create_table("t_mentorship", "MENTORSHIP", [
    ("MentorshipID", True, False),
    ("MentorID", False, True),
    ("MenteeID", False, True),
    ("StartDate", False, False),
    ("EndDate", False, False),
    ("Status", False, False),
    ("MentorshipArea", False, False),
    ("Goals", False, False),
], 50, 950)

# ALUMNI_SKILL (Junction for ALUMNI ↔ SKILL M:N)
alumni_skill = create_table("t_alumni_skill", "ALUMNI_SKILL", [
    ("AlumniID", True, True),
    ("SkillID", True, True),
], 900, 950)

# ALUMNI_PHONE (Multivalued)
alumni_phone = create_table("t_alumni_phone", "ALUMNI_PHONE", [
    ("AlumniID", True, True),
    ("PhoneNumber", True, False),
], 1350, 950)

# ALUMNI_EVENT (Junction for ALUMNI ↔ EVENT M:N)
alumni_event = create_table("t_alumni_event", "ALUMNI_EVENT", [
    ("AlumniID", True, True),
    ("EventID", True, True),
    ("RegistrationDate", False, False),
], 1350, 950)

# ================================================================
# RELATIONSHIPS (Removed - no connecting lines)
# ================================================================

# ================================================================
# LEGEND
# ================================================================

legend = """<b style="font-size:16px;">Relational Schema Legend</b><hr><br><b>Notation</b><br><u>Underline</u> = Primary Key<br><font color="red">(FK)</font> = Foreign Key<br><br><b>Relationships</b><br>Lines show FK references<br>Labels show FK column name<br><br><b>Tables</b><br>Blue Header = Table Name<br>White rows = Attributes"""

style_legend = (f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF9E6;"
                f"strokeColor=#000000;strokeWidth=2;verticalAlign=top;"
                f"align=left;fontSize=11;spacingLeft=10;spacingTop=6;"
                f"labelBackgroundColor=none;")
add_cell("legend", legend, style_legend, 1450, 120, 280, 200)

# ================================================================
# ASSEMBLE XML
# ================================================================

xml_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<mxfile host="app.diagrams.net">',
    '  <diagram name="Relational-Schema" id="relational-schema">',
    '    <mxGraphModel dx="100" dy="100" grid="1" gridSize="10" guides="1" '
    'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
    'pageWidth="3500" pageHeight="1200" htmlLabel="1">',
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

out_path = "/Users/dakshagarwal/dbms-project/laguna/diagrams/Relational_Schema.drawio"
with open(out_path, 'w') as f:
    f.write(output)

print(f"✅ Generated Relational Schema: {out_path}")
print(f"   Tables: 13")
print(f"   Size: {len(output)} bytes")
print()
print("Tables included:")
print("  1. DEPARTMENT")
print("  2. BATCH")
print("  3. COMPANY")
print("  4. SKILL")
print("  5. ALUMNI")
print("  6. STUDENT")
print("  7. EVENT")
print("  8. DONATION")
print("  9. JOB")
print("  10. MENTORSHIP (Weak)")
print("  11. ALUMNI_SKILL (Junction)")
print("  12. ALUMNI_PHONE (Multivalued)")
print("  13. ALUMNI_EVENT (Junction)")
