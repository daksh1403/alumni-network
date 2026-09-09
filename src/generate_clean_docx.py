#!/usr/bin/env python3
"""
Generate CLEAN DOCX Report - No Foreign Keys, All Inconsistencies Fixed
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os


def set_cell_shading(cell, color):
    """Set cell background color"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading_elm)


def add_formatted_table(doc, data, headers, col_widths=None):
    """Add a formatted table to the document"""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        set_cell_shading(header_cells[i], '2E86AB')
        for paragraph in header_cells[i].paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Data rows
    for i, row_data in enumerate(data):
        row_cells = table.rows[i + 1].cells
        for j, cell_data in enumerate(row_data):
            row_cells[j].text = str(cell_data)
            if i % 2 == 0:
                set_cell_shading(row_cells[j], 'E8F4FD')
    
    return table


def create_report():
    """Main function to create the clean DOCX report"""
    doc = Document()
    
    # Page setup
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    
    # Styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # ==========================================
    # TITLE PAGE
    # ==========================================
    for _ in range(6):
        doc.add_paragraph('')
    
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('ALUMNI NETWORK AND\nENGAGEMENT PLATFORM')
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    
    doc.add_paragraph('')
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Database Management Systems Project')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(46, 134, 171)
    
    doc.add_paragraph('')
    
    subtitle2 = doc.add_paragraph()
    subtitle2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle2.add_run('DA1 - ER/EER Model & Relational Schema')
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(100, 100, 100)
    
    for _ in range(4):
        doc.add_paragraph('')
    
    # Team members
    team_info = doc.add_paragraph()
    team_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = team_info.add_run('Team Members:')
    run.font.size = Pt(12)
    run.font.bold = True
    
    members = [
        'Sagarika Kaistha - 25BCE5091',
        'Praveen G - 25BCE5092',
        'Daksh Agarwal - 25BCE5098'
    ]
    
    for member in members:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(member)
        run.font.size = Pt(11)
    
    doc.add_paragraph('')
    
    # Submission info
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = info.add_run('Submission Deadline: 31-07-2026')
    run.font.size = Pt(11)
    run.font.italic = True
    
    doc.add_page_break()
    
    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    doc.add_heading('TABLE OF CONTENTS', level=1)
    
    toc_items = [
        ('1.', 'Introduction'),
        ('2.', 'Entity-Relationship Model'),
        ('  2.1', 'Types of Attributes'),
        ('  2.2', 'Strong Entities'),
        ('  2.3', 'Relationship Types'),
        ('  2.4', 'Participation Constraints'),
        ('  2.5', 'Cardinality Constraints'),
        ('  2.6', 'Role Names'),
        ('3.', 'Extended ER Model'),
        ('  3.1', 'Generalization/Specialization'),
        ('  3.2', 'Disjoint/Overlapping Constraints'),
        ('  3.3', 'Total/Partial Specialization'),
        ('4.', 'Relational Schema'),
        ('  4.1', 'Entity Tables'),
        ('  4.2', 'Junction Tables'),
        ('  4.3', 'Constraints Summary'),
        ('5.', 'Conclusion')
    ]
    
    for item in toc_items:
        p = doc.add_paragraph()
        run = p.add_run(f'{item[0]} {item[1]}')
        run.font.size = Pt(11)
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    doc.add_heading('1. Introduction', level=1)
    
    doc.add_paragraph(
        'This project designs a database for managing alumni of a college. '
        'The system tracks passed out students, helps them stay connected '
        'with each other and with the college. We manage events, donations, '
        'jobs and mentorship programs through this system.'
    )
    
    doc.add_paragraph(
        'In this project we have used the following ER/EER concepts:'
    )
    
    concepts = [
        'Types of Attributes: Simple, Composite, Single-valued, Multi-valued, Derived, Stored, Key, NULL',
        'Strong Entities with primary keys',
        'Binary, Unary (Recursive) Relationships',
        'Participation Constraints: Total and Partial',
        'Cardinality Constraints: 1:1, 1:N, M:N',
        'Role Names in Relationships',
        'Extended ER: Generalization/Specialization with Disjoint/Overlapping and Total/Partial constraints',
        'Normalization up to BCNF'
    ]
    
    for concept in concepts:
        p = doc.add_paragraph(concept, style='List Bullet')
    
    doc.add_heading('1.1 Problem Statement', level=2)
    
    doc.add_paragraph(
        'Colleges dont have a proper way to stay in touch with their old students. '
        'Once students pass out, there is no system to contact them or keep track of '
        'where they are working now. Also there is no way for alumni to help current '
        'students with jobs or mentorship. This database solves all these problems.'
    )
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2: ER MODEL - TYPES OF ATTRIBUTES
    # ==========================================
    doc.add_heading('2. Entity-Relationship Model', level=1)
    
    doc.add_heading('2.1 Types of Attributes', level=2)
    
    doc.add_paragraph(
        'Attributes are properties or characteristics of an entity. '
        'For ALUMNI entity, the attributes would be Name, Email, Phone etc.'
    )
    
    # Simple/Atomic Attributes
    doc.add_heading('2.1.1 Simple (Atomic) Attributes', level=3)
    doc.add_paragraph('These are basic attributes which cannot be divided further.')
    
    simple_data = [
        ['Name', 'ALUMNI', 'Single-valued, Simple'],
        ['Email', 'ALUMNI', 'Single-valued, Simple'],
        ['Phone', 'ALUMNI', 'Single-valued, Simple'],
        ['DeptName', 'DEPARTMENT', 'Single-valued, Simple'],
        ['CompanyName', 'COMPANY', 'Single-valued, Simple'],
        ['SkillName', 'SKILL', 'Single-valued, Simple']
    ]
    add_formatted_table(doc, simple_data, ['Attribute', 'Entity', 'Type'])
    doc.add_paragraph('')
    
    # Composite Attributes
    doc.add_heading('2.1.2 Composite Attributes', level=3)
    doc.add_paragraph('Composite attributes can be broken down into smaller sub-parts.')
    
    composite_data = [
        ['Address', 'ALUMNI', 'City, State, PinCode'],
        ['FullName', 'ALUMNI', 'FirstName, LastName']
    ]
    add_formatted_table(doc, composite_data, ['Composite Attribute', 'Entity', 'Component Attributes'])
    doc.add_paragraph('')
    
    # Single-valued Attributes
    doc.add_heading('2.1.3 Single-valued Attributes', level=3)
    doc.add_paragraph('These attributes can only have one value for each entity.')
    
    single_data = [
        ['DateOfBirth', 'ALUMNI', 'One date per person'],
        ['Email', 'ALUMNI', 'One primary email'],
        ['GraduationYear', 'ALUMNI', 'One year per graduation']
    ]
    add_formatted_table(doc, single_data, ['Attribute', 'Entity', 'Description'])
    doc.add_paragraph('')
    
    # Multi-valued Attributes
    doc.add_heading('2.1.4 Multi-valued Attributes', level=3)
    doc.add_paragraph('These attributes can store multiple values for a single entity. In ER diagram these are shown with double ovals.')
    
    multi_data = [
        ['Skills', 'ALUMNI', 'Java, Python, SQL etc'],
        ['PhoneNumbers', 'ALUMNI', 'Mobile, Home, Work']
    ]
    add_formatted_table(doc, multi_data, ['Attribute', 'Entity', 'Example Values'])
    doc.add_paragraph('')
    
    # Derived Attributes
    doc.add_heading('2.1.5 Derived Attributes', level=3)
    doc.add_paragraph('Derived attributes can be calculated from other attributes.')
    
    derived_data = [
        ['Age', 'ALUMNI', 'Calculated from DateOfBirth'],
        ['YearsSinceGraduation', 'ALUMNI', 'CurrentYear - GraduationYear'],
        ['TotalDonations', 'ALUMNI', 'Sum of all Donation amounts']
    ]
    add_formatted_table(doc, derived_data, ['Derived Attribute', 'Entity', 'Derived From'])
    doc.add_paragraph('')
    
    # Stored Attributes
    doc.add_heading('2.1.6 Stored Attributes', level=3)
    doc.add_paragraph('These attributes have values directly stored in the database.')
    
    stored_data = [
        ['DateOfBirth', 'ALUMNI', 'Stored directly'],
        ['Email', 'ALUMNI', 'Stored directly'],
        ['GraduationYear', 'ALUMNI', 'Stored directly']
    ]
    add_formatted_table(doc, stored_data, ['Stored Attribute', 'Entity', 'Description'])
    doc.add_paragraph('')
    
    # Key Attributes
    doc.add_heading('2.1.7 Key Attributes', level=3)
    doc.add_paragraph('Key attributes uniquely identify each entity instance. In ER diagram key attributes are shown underlined.')
    
    key_data = [
        ['AlumniID', 'ALUMNI', 'Primary Key'],
        ['Email', 'ALUMNI', 'Unique Key'],
        ['DeptID', 'DEPARTMENT', 'Primary Key'],
        ['EventID', 'EVENT', 'Primary Key'],
        ['DonationID', 'DONATION', 'Primary Key']
    ]
    add_formatted_table(doc, key_data, ['Key Attribute', 'Entity', 'Description'])
    doc.add_paragraph('')
    
    # NULL Attributes
    doc.add_heading('2.1.8 NULL Attributes', level=3)
    doc.add_paragraph('NULL attributes can be left empty. Not every field is mandatory.')
    
    null_data = [
        ['LinkedInProfile', 'ALUMNI', 'Optional - may not have'],
        ['ProfilePicture', 'ALUMNI', 'Optional photo'],
        ['EndDate', 'MENTORSHIP', 'NULL if still active']
    ]
    add_formatted_table(doc, null_data, ['NULL Attribute', 'Entity', 'Reason for NULL'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2.2: STRONG ENTITIES
    # ==========================================
    doc.add_heading('2.2 Strong Entities', level=2)
    
    doc.add_paragraph(
        'Strong entities have their own primary key and can exist independently. '
        'They dont depend on any other entity for their existence.'
    )
    
    # ALUMNI Entity (Complete with all attribute types)
    doc.add_heading('2.2.1 ALUMNI (Strong Entity)', level=3)
    doc.add_paragraph('Primary Key: AlumniID | Main entity of our system')
    
    alumni_complete = [
        ['AlumniID', 'INT', 'PK, NOT NULL', 'Key Attribute'],
        ['FirstName', 'VARCHAR(50)', 'NOT NULL', 'Simple, Single-valued'],
        ['LastName', 'VARCHAR(50)', 'NOT NULL', 'Simple, Single-valued'],
        ['Email', 'VARCHAR(100)', 'UNIQUE, NOT NULL', 'Simple, Key'],
        ['Phone', 'VARCHAR(15)', '', 'Simple, Single-valued'],
        ['DateOfBirth', 'DATE', '', 'Simple, Stored'],
        ['Age', '-', 'Derived', 'Derived from DateOfBirth'],
        ['GraduationYear', 'INT', 'NOT NULL', 'Simple, Stored'],
        ['CurrentCity', 'VARCHAR(50)', '', 'Part of Address (composite)'],
        ['CurrentState', 'VARCHAR(50)', '', 'Part of Address (composite)'],
        ['CurrentCountry', 'VARCHAR(50)', '', 'Part of Address (composite)'],
        ['LinkedInProfile', 'VARCHAR(200)', 'NULL', 'Optional'],
        ['ProfilePicture', 'VARCHAR(255)', 'NULL', 'Optional'],
        ['DeptID', 'INT', 'NOT NULL', 'References DEPARTMENT'],
        ['BatchID', 'INT', 'NOT NULL', 'References BATCH'],
        ['CompanyID', 'INT', 'NULL', 'References COMPANY'],
        ['IsActive', 'BOOLEAN', 'DEFAULT TRUE', 'Status flag']
    ]
    add_formatted_table(doc, alumni_complete, ['Attribute', 'Type', 'Constraints', 'Attribute Type'])
    doc.add_paragraph('')
    
    # Other Strong Entities
    doc.add_heading('2.2.2 Other Strong Entities', level=3)
    
    strong_entities = [
        ['DEPARTMENT', 'DeptID (PK)', 'DeptName, DeptCode, HODName, EstablishedYear'],
        ['BATCH', 'BatchID (PK)', 'BatchYear, DeptID, Section, TotalStudents'],
        ['COMPANY', 'CompanyID (PK)', 'CompanyName, Industry, CompanySize, Website, Headquarters'],
        ['SKILL', 'SkillID (PK)', 'SkillName, SkillCategory, Description'],
        ['EVENT', 'EventID (PK)', 'EventName, EventType, EventDate, Venue, OrganizerID'],
        ['DONATION', 'DonationID (PK)', 'DonorID, Amount, DonationDate, PaymentMethod, Purpose'],
        ['JOB', 'JobID (PK)', 'JobTitle, CompanyID, PostedBy, JobType, Location, Salary'],
        ['MENTORSHIP', 'MentorshipID (PK)', 'MentorID, MenteeID, StartDate, Status, Feedback, Rating'],
        ['FORUM', 'ForumID (PK)', 'ForumName, Description, Category, CreatedBy'],
        ['POST', 'PostID (PK)', 'ForumID, AuthorID, Title, Content'],
        ['COMMENT', 'CommentID (PK)', 'PostID, AuthorID, Content, ParentCommentID']
    ]
    add_formatted_table(doc, strong_entities, ['Entity', 'Primary Key', 'Attributes'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2.3: RELATIONSHIP TYPES
    # ==========================================
    doc.add_heading('2.3 Relationship Types', level=2)
    
    # Binary Relationships
    doc.add_heading('2.3.1 Binary Relationships', level=3)
    doc.add_paragraph('Binary relationships connect two entities together.')
    
    binary_data = [
        ['ALUMNI - DEPARTMENT', 'belongs_to', 'N:1', 'Total (ALUMNI), Partial (DEPT)'],
        ['ALUMNI - BATCH', 'belongs_to', 'N:1', 'Total (ALUMNI), Partial (BATCH)'],
        ['ALUMNI - COMPANY', 'works_at', 'N:1', 'Partial (Both)'],
        ['ALUMNI - SKILL', 'has', 'M:N', 'Partial (Both)'],
        ['ALUMNI - EVENT', 'attends', 'M:N', 'Partial (Both)'],
        ['ALUMNI - DONATION', 'makes', '1:N', 'Partial (ALUMNI), Total (DONATION)'],
        ['ALUMNI - JOB', 'posts', '1:N', 'Partial (ALUMNI), Total (JOB)'],
        ['ALUMNI - FORUM', 'creates', '1:N', 'Partial (ALUMNI), Total (FORUM)'],
        ['FORUM - POST', 'contains', '1:N', 'Partial (FORUM), Total (POST)'],
        ['POST - COMMENT', 'has', '1:N', 'Partial (POST), Total (COMMENT)'],
        ['JOB - COMPANY', 'at', 'N:1', 'Total (JOB), Partial (COMPANY)']
    ]
    add_formatted_table(doc, binary_data, ['Relationship', 'Name', 'Cardinality', 'Participation'])
    doc.add_paragraph('')
    
    # Unary/Recursive Relationships
    doc.add_heading('2.3.2 Unary (Recursive) Relationships', level=3)
    doc.add_paragraph('Unary relationships are when an entity is related to itself.')
    
    unary_data = [
        ['ALUMNI - ALUMNI', 'mentors', '1:N', 'Partial (Both)', 'Mentor role and Mentee role'],
        ['COMMENT - COMMENT', 'replies_to', '1:N', 'Partial (Both)', 'Parent comment and Reply']
    ]
    add_formatted_table(doc, unary_data, ['Relationship', 'Name', 'Cardinality', 'Participation', 'Role Names'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2.4: PARTICIPATION CONSTRAINTS
    # ==========================================
    doc.add_heading('2.4 Participation Constraints', level=2)
    
    doc.add_paragraph(
        'Participation constraints tell us whether all instances of an entity must participate '
        'in a relationship or only some of them need to participate.'
    )
    
    doc.add_heading('2.4.1 Total Participation', level=3)
    doc.add_paragraph('Total participation means every instance of the entity MUST be part of the relationship. Shown with double line in ER diagram.')
    
    total_data = [
        ['ALUMNI - DEPARTMENT', 'ALUMNI has Total Participation', 'Every alumnus must belong to a department'],
        ['ALUMNI - BATCH', 'ALUMNI has Total Participation', 'Every alumnus must belong to a batch'],
        ['DONATION - ALUMNI', 'DONATION has Total Participation', 'Every donation must have a donor'],
        ['JOB - ALUMNI', 'JOB has Total Participation', 'Every job must be posted by someone'],
        ['EVENT - ALUMNI', 'EVENT has Total Participation', 'Every event must have an organizer']
    ]
    add_formatted_table(doc, total_data, ['Relationship', 'Constraint', 'Explanation'])
    doc.add_paragraph('')
    
    doc.add_heading('2.4.2 Partial Participation', level=3)
    doc.add_paragraph('Partial participation means its not mandatory for every entity instance to participate. Shown with single line in ER diagram.')
    
    partial_data = [
        ['ALUMNI - SKILL', 'ALUMNI has Partial Participation', 'Not all alumni have skills listed'],
        ['ALUMNI - EVENT', 'ALUMNI has Partial Participation', 'Not all alumni attend events'],
        ['ALUMNI - COMPANY', 'ALUMNI has Partial Participation', 'Not all alumni are employed'],
        ['ALUMNI - DONATION', 'ALUMNI has Partial Participation', 'Not all alumni make donations'],
        ['DEPARTMENT - ALUMNI', 'DEPARTMENT has Partial Participation', 'New departments may have no alumni yet']
    ]
    add_formatted_table(doc, partial_data, ['Relationship', 'Constraint', 'Explanation'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2.5: CARDINALITY CONSTRAINTS
    # ==========================================
    doc.add_heading('2.5 Cardinality Constraints', level=2)
    
    doc.add_heading('2.5.1 One-to-One (1:1)', level=3)
    doc.add_paragraph('In one-to-one relationship, one entity in A is connected to at most one entity in B and vice versa.')
    
    one_to_one = [
        ['ALUMNI - ALUMNI_PROFILE', '1:1', 'Each alumni has exactly one profile']
    ]
    add_formatted_table(doc, one_to_one, ['Relationship', 'Cardinality', 'Example'])
    doc.add_paragraph('')
    
    doc.add_heading('2.5.2 One-to-Many (1:N)', level=3)
    doc.add_paragraph('In one-to-many relationship, one entity in A can be connected to many entities in B, but each B is connected to only one A.')
    
    one_to_many = [
        ['DEPARTMENT - ALUMNI', '1:N', 'One department has many alumni'],
        ['BATCH - ALUMNI', '1:N', 'One batch has many alumni'],
        ['ALUMNI - DONATION', '1:N', 'One alumni makes many donations'],
        ['ALUMNI - EVENT (Organize)', '1:N', 'One alumni organizes many events'],
        ['FORUM - POST', '1:N', 'One forum has many posts'],
        ['POST - COMMENT', '1:N', 'One post has many comments']
    ]
    add_formatted_table(doc, one_to_many, ['Relationship', 'Cardinality', 'Description'])
    doc.add_paragraph('')
    
    doc.add_heading('2.5.3 Many-to-Many (M:N)', level=3)
    doc.add_paragraph('In many-to-many relationship, one entity in A can be connected to many entities in B and vice versa. This requires a junction table.')
    
    many_to_many = [
        ['ALUMNI - SKILL', 'M:N', 'Many alumni have many skills'],
        ['ALUMNI - EVENT (Attend)', 'M:N', 'Many alumni attend many events']
    ]
    add_formatted_table(doc, many_to_many, ['Relationship', 'Cardinality', 'Description'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 2.6: ROLE NAMES
    # ==========================================
    doc.add_heading('2.6 Role Names', level=2)
    
    doc.add_paragraph(
        'Role names are used when an entity has a recursive relationship with itself. '
        'We need role names to clarify which instance is playing which role.'
    )
    
    doc.add_heading('2.6.1 MENTORSHIP Relationship', level=3)
    
    role_data = [
        ['ALUMNI (as Mentor)', 'Provides guidance and support', '1:N', 'One mentor can have many mentees'],
        ['ALUMNI (as Mentee)', 'Receives guidance and support', 'N:1', 'Many mentees can have one mentor']
    ]
    add_formatted_table(doc, role_data, ['Role', 'Description', 'Cardinality', 'Explanation'])
    doc.add_paragraph('')
    
    doc.add_heading('2.6.2 COMMENT Reply Relationship', level=3)
    
    reply_data = [
        ['COMMENT (as Parent)', 'Original comment', '1:N', 'One parent can have many replies'],
        ['COMMENT (as Reply)', 'Response to parent', 'N:1', 'Many replies to one parent']
    ]
    add_formatted_table(doc, reply_data, ['Role', 'Description', 'Cardinality', 'Explanation'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 3: EER MODEL
    # ==========================================
    doc.add_heading('3. Extended ER Model', level=1)
    
    doc.add_heading('3.1 Generalization/Specialization', level=2)
    
    doc.add_paragraph(
        'Generalization combines similar entities into one higher level entity (bottom-up). '
        'Specialization divides a supertype into subtypes (top-down). '
        'For example ALUMNI, STUDENT and ADMIN all have common attributes like Name, Email, '
        'Phone etc. So we generalize them into a PERSON supertype.'
    )
    
    doc.add_heading('3.1.1 PERSON Supertype', level=3)
    
    person_data = [
        ['PERSON', 'Supertype', 'PersonID, FirstName, LastName, Email, Phone, DOB, Gender'],
        ['ALUMNI', 'Subtype', 'GraduationYear, DeptID, BatchID, CompanyID, IsActive'],
        ['STUDENT', 'Subtype', 'StudentID, EnrollmentYear, DeptID, Semester, CGPA'],
        ['ADMIN', 'Subtype', 'AdminRole, Department, AccessLevel']
    ]
    add_formatted_table(doc, person_data, ['Entity', 'Type', 'Attributes'])
    doc.add_paragraph('')
    
    doc.add_paragraph(
        'Note: In the relational schema, we implement this using Method 1 '
        '(separate tables for supertype and each subtype with foreign key linking). '
        'The supertype PERSON table stores shared attributes, and each subtype table '
        'stores its own specific attributes with PersonID as primary key.'
    )
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 3.2: DISJOINT/OVERLAPPING
    # ==========================================
    doc.add_heading('3.2 Disjoint/Overlapping Constraints', level=2)
    
    doc.add_heading('3.2.1 Disjoint Constraint (d)', level=3)
    doc.add_paragraph('Disjoint means an entity can belong to only ONE subtype at a time.')
    
    disjoint_data = [
        ['PERSON', 'ALUMNI, STUDENT, ADMIN', 'Disjoint (d)', 'A person cannot be both Alumni and Student simultaneously']
    ]
    add_formatted_table(doc, disjoint_data, ['Supertype', 'Subtypes', 'Constraint', 'Explanation'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 3.3: TOTAL/PARTIAL SPECIALIZATION
    # ==========================================
    doc.add_heading('3.3 Total/Partial Specialization', level=2)
    
    doc.add_heading('3.3.1 Total Specialization (t)', level=3)
    doc.add_paragraph('Total specialization means every instance of the supertype MUST belong to at least one subtype.')
    
    total_spec = [
        ['PERSON', 'ALUMNI, STUDENT, ADMIN', 'Total (t)', 'Every person must be classified as one type']
    ]
    add_formatted_table(doc, total_spec, ['Supertype', 'Subtypes', 'Constraint', 'Explanation'])
    doc.add_paragraph('')
    
    doc.add_paragraph(
        'Since specialization is total and disjoint, every person in the system must be '
        'exactly one of: ALUMNI, STUDENT, or ADMIN. The PERSON table stores common attributes, '
        'and each subtype table stores type-specific attributes.'
    )
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 4: RELATIONAL SCHEMA
    # ==========================================
    doc.add_heading('4. Relational Schema', level=1)
    
    doc.add_paragraph(
        'Complete relational schema for all entities. Note: This schema does not use '
        'foreign key constraints. Referential integrity is maintained at the application level.'
    )
    
    # ==========================================
    # CHAPTER 4.1: ENTITY TABLES
    # ==========================================
    doc.add_heading('4.1 Entity Tables', level=2)
    
    # DEPARTMENT
    doc.add_heading('4.1.1 DEPARTMENT', level=3)
    dept_data = [
        ['DeptID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['DeptName', 'VARCHAR(100)', 'NOT NULL, UNIQUE', 'Department name'],
        ['DeptCode', 'VARCHAR(10)', 'NOT NULL, UNIQUE', 'Short code'],
        ['HODPersonID', 'INT', 'FK to PERSON', 'Head of Department reference'],
        ['EstablishedYear', 'INT', '', 'Year established']
    ]
    add_formatted_table(doc, dept_data, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('V2 Note: HODName replaced with HODPersonID FK to PERSON table for 3NF compliance.')
    doc.add_paragraph('')
    
    # BATCH
    doc.add_heading('4.1.2 BATCH', level=3)
    batch_data = [
        ['BatchID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['BatchYear', 'INT', 'NOT NULL', 'Graduation year'],
        ['DeptID', 'INT', 'NOT NULL', 'Department reference'],
        ['Section', 'VARCHAR(5)', '', 'Section (A, B, C)'],
        ['TotalStudents', 'INT', '', 'Number of students']
    ]
    add_formatted_table(doc, batch_data, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # COMPANY
    doc.add_heading('4.1.3 COMPANY', level=3)
    company_data = [
        ['CompanyID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['CompanyName', 'VARCHAR(100)', 'NOT NULL', 'Company name'],
        ['Industry', 'VARCHAR(50)', '', 'Industry type'],
        ['SizeID', 'INT', 'FK to COMPANY_SIZE', 'Company size reference'],
        ['Website', 'VARCHAR(200)', '', 'Company website'],
        ['Headquarters', 'VARCHAR(100)', '', 'HQ location'],
        ['FoundedYear', 'INT', '', 'Year founded']
    ]
    add_formatted_table(doc, company_data, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('V2 Note: CompanySize extracted to COMPANY_SIZE lookup table for normalization.')
    doc.add_paragraph('')
    
    # SKILL
    doc.add_heading('4.1.4 SKILL', level=3)
    skill_data = [
        ['SkillID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['SkillName', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Skill name'],
        ['SkillCategory', 'VARCHAR(50)', '', 'Programming/Design/etc'],
        ['Description', 'TEXT', '', 'Skill description']
    ]
    add_formatted_table(doc, skill_data, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # PERSON (Supertype)
    doc.add_heading('4.1.5 PERSON (Supertype)', level=3)
    doc.add_paragraph('Stores common attributes shared by ALUMNI, STUDENT, and ADMIN.')
    person_schema = [
        ['PersonID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['FirstName', 'VARCHAR(50)', 'NOT NULL', 'First name'],
        ['LastName', 'VARCHAR(50)', 'NOT NULL', 'Last name'],
        ['Email', 'VARCHAR(100)', 'NOT NULL, UNIQUE', 'Email address'],
        ['Phone', 'VARCHAR(15)', '', 'Phone number'],
        ['DateOfBirth', 'DATE', '', 'Date of birth'],
        ['Gender', 'CHAR(1)', 'CHECK (M/F/O)', 'Gender'],
        ['Address', 'VARCHAR(200)', '', 'Full address'],
        ['ProfilePicture', 'VARCHAR(255)', '', 'Photo URL'],
        ['CreatedAt', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Registration date']
    ]
    add_formatted_table(doc, person_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # ALUMNI (Subtype)
    doc.add_heading('4.1.6 ALUMNI (Subtype of PERSON)', level=3)
    doc.add_paragraph('PersonID is both Primary Key and references PERSON.')
    alumni_schema = [
        ['PersonID', 'INT', 'PRIMARY KEY, NOT NULL', 'References PERSON'],
        ['GraduationYear', 'INT', 'NOT NULL', 'Year of graduation'],
        ['DeptID', 'INT', 'NOT NULL', 'Department reference'],
        ['BatchID', 'INT', 'NOT NULL', 'Batch reference'],
        ['CurrentCompanyID', 'INT', '', 'Company reference'],
        ['CurrentPosition', 'VARCHAR(100)', '', 'Job title'],
        ['LinkedInProfile', 'VARCHAR(200)', '', 'LinkedIn URL'],
        ['IsActive', 'BOOLEAN', 'DEFAULT TRUE', 'Active status']
    ]
    add_formatted_table(doc, alumni_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # STUDENT (Subtype)
    doc.add_heading('4.1.7 STUDENT (Subtype of PERSON)', level=3)
    doc.add_paragraph('PersonID is both Primary Key and references PERSON.')
    student_schema = [
        ['PersonID', 'INT', 'PRIMARY KEY, NOT NULL', 'References PERSON'],
        ['StudentID', 'VARCHAR(20)', 'NOT NULL, UNIQUE', 'Student roll number'],
        ['EnrollmentYear', 'INT', 'NOT NULL', 'Year enrolled'],
        ['DeptID', 'INT', 'NOT NULL', 'Department reference'],
        ['CurrentSemester', 'INT', '', 'Current semester'],
        ['CGPA', 'DECIMAL(4,2)', '', 'Cumulative GPA']
    ]
    add_formatted_table(doc, student_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # ADMIN (Subtype)
    doc.add_heading('4.1.8 ADMIN (Subtype of PERSON)', level=3)
    doc.add_paragraph('PersonID is both Primary Key and references PERSON.')
    admin_schema = [
        ['PersonID', 'INT', 'PRIMARY KEY, NOT NULL', 'References PERSON'],
        ['AdminRole', 'VARCHAR(50)', 'NOT NULL', 'Role name'],
        ['Department', 'VARCHAR(100)', '', 'Department managed'],
        ['AccessLevel', 'INT', 'CHECK (1-5)', 'Access level']
    ]
    add_formatted_table(doc, admin_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # EVENT
    doc.add_heading('4.1.9 EVENT', level=3)
    event_schema = [
        ['EventID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['EventName', 'VARCHAR(100)', 'NOT NULL', 'Event name'],
        ['EventTypeID', 'INT', 'FK to EVENT_TYPE', 'Event type reference'],
        ['Description', 'TEXT', '', 'Event description'],
        ['EventDate', 'DATE', 'NOT NULL', 'Event date'],
        ['EventTime', 'TIME', '', 'Event time'],
        ['Venue', 'VARCHAR(200)', '', 'Event location'],
        ['MaxCapacity', 'INT', '', 'Max attendees'],
        ['RegistrationFee', 'DECIMAL(10,2)', 'DEFAULT 0.00', 'Fee amount'],
        ['OrganizerID', 'INT', 'NOT NULL, FK to ALUMNI', 'Organizer reference'],
        ['CreatedDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Created date']
    ]
    add_formatted_table(doc, event_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('V2 Note: EventType extracted to EVENT_TYPE lookup table for normalization.')
    doc.add_paragraph('')
    
    # DONATION
    doc.add_heading('4.1.10 DONATION', level=3)
    donation_schema = [
        ['DonationID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['DonorID', 'INT', 'NOT NULL', 'ALUMNI reference'],
        ['Amount', 'DECIMAL(12,2)', 'NOT NULL', 'Donation amount'],
        ['DonationDate', 'DATE', 'NOT NULL', 'Date of donation'],
        ['PaymentMethod', 'VARCHAR(30)', 'CHECK (Online/Check/DD/Cash)', 'Payment type'],
        ['Purpose', 'VARCHAR(100)', '', 'Donation purpose'],
        ['TransactionID', 'VARCHAR(50)', 'UNIQUE', 'Bank transaction ID'],
        ['IsAnonymous', 'BOOLEAN', 'DEFAULT FALSE', 'Anonymous donation'],
        ['ReceiptNumber', 'VARCHAR(50)', 'UNIQUE', 'Receipt number']
    ]
    add_formatted_table(doc, donation_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # JOB
    doc.add_heading('4.1.11 JOB', level=3)
    job_schema = [
        ['JobID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['JobTitle', 'VARCHAR(100)', 'NOT NULL', 'Job title'],
        ['CompanyID', 'INT', 'NOT NULL', 'Company reference'],
        ['PostedBy', 'INT', 'NOT NULL', 'ALUMNI reference'],
        ['JobType', 'VARCHAR(30)', 'CHECK (Full-Time/Part-Time/Contract/Internship)', 'Job type'],
        ['Location', 'VARCHAR(100)', '', 'Job location'],
        ['Salary', 'VARCHAR(50)', '', 'Salary range'],
        ['Description', 'TEXT', '', 'Job description'],
        ['Requirements', 'TEXT', '', 'Job requirements'],
        ['PostedDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Posted date'],
        ['ExpiryDate', 'DATE', '', 'Application deadline'],
        ['IsActive', 'BOOLEAN', 'DEFAULT TRUE', 'Active status']
    ]
    add_formatted_table(doc, job_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # MENTORSHIP
    doc.add_heading('4.1.12 MENTORSHIP', level=3)
    doc.add_paragraph('Represents mentorship relationship between two ALUMNI.')
    mentorship_schema = [
        ['MentorshipID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['MentorID', 'INT', 'NOT NULL, FK to ALUMNI', 'Mentor reference'],
        ['MenteeID', 'INT', 'NOT NULL, FK to ALUMNI', 'Mentee reference'],
        ['StartDate', 'DATE', 'NOT NULL', 'Start date'],
        ['EndDate', 'DATE', '', 'End date'],
        ['Status', 'VARCHAR(20)', 'CHECK (Active/Completed/Paused/Cancelled)', 'Status'],
        ['AreaID', 'INT', 'FK to MENTORSHIP_AREA', 'Mentorship area reference'],
        ['Goals', 'TEXT', '', 'Mentorship goals'],
        ['Feedback', 'TEXT', '', 'Feedback from mentee'],
        ['Rating', 'INT', 'CHECK (1-5)', 'Satisfaction rating']
    ]
    add_formatted_table(doc, mentorship_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('V2 Note: MentorshipArea extracted to MENTORSHIP_AREA lookup table for normalization.')
    doc.add_paragraph('')
    
    # FORUM
    doc.add_heading('4.1.13 FORUM', level=3)
    forum_schema = [
        ['ForumID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['ForumName', 'VARCHAR(100)', 'NOT NULL', 'Forum name'],
        ['Description', 'TEXT', '', 'Forum description'],
        ['Category', 'VARCHAR(50)', '', 'Forum category'],
        ['CreatedBy', 'INT', 'NOT NULL', 'ALUMNI reference'],
        ['CreatedDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Created date'],
        ['IsActive', 'BOOLEAN', 'DEFAULT TRUE', 'Active status']
    ]
    add_formatted_table(doc, forum_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # POST
    doc.add_heading('4.1.14 POST', level=3)
    post_schema = [
        ['PostID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['ForumID', 'INT', 'NOT NULL', 'FORUM reference'],
        ['AuthorID', 'INT', 'NOT NULL', 'ALUMNI reference'],
        ['Title', 'VARCHAR(200)', 'NOT NULL', 'Post title'],
        ['Content', 'TEXT', 'NOT NULL', 'Post content'],
        ['PostedDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Posted date'],
        ['LikesCount', 'INT', 'DEFAULT 0', 'Number of likes'],
        ['IsPinned', 'BOOLEAN', 'DEFAULT FALSE', 'Pinned status']
    ]
    add_formatted_table(doc, post_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # COMMENT
    doc.add_heading('4.1.15 COMMENT', level=3)
    comment_schema = [
        ['CommentID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['PostID', 'INT', 'NOT NULL', 'POST reference'],
        ['AuthorID', 'INT', 'NOT NULL', 'ALUMNI reference'],
        ['Content', 'TEXT', 'NOT NULL', 'Comment text'],
        ['CommentDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Comment date'],
        ['ParentCommentID', 'INT', '', 'Self-reference for replies']
    ]
    add_formatted_table(doc, comment_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 4.1.16-18: LOOKUP TABLES (V2)
    # ==========================================
    doc.add_heading('4.1.16 EVENT_TYPE (Lookup Table - V2)', level=3)
    doc.add_paragraph('Lookup table for event types, extracted from EVENT table for normalization.')
    event_type_schema = [
        ['TypeID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['TypeName', 'VARCHAR(50)', 'NOT NULL, UNIQUE', 'Event type name']
    ]
    add_formatted_table(doc, event_type_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('Sample values: Reunion, Workshop, Seminar, Networking')
    doc.add_paragraph('')
    
    doc.add_heading('4.1.17 COMPANY_SIZE (Lookup Table - V2)', level=3)
    doc.add_paragraph('Lookup table for company sizes, extracted from COMPANY table for normalization.')
    company_size_schema = [
        ['SizeID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['SizeRange', 'VARCHAR(30)', 'NOT NULL, UNIQUE', 'Size range']
    ]
    add_formatted_table(doc, company_size_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('Sample values: 1-10, 11-50, 51-200, 201-1000, 1001-10000, 10001-50000, 50001-100000, 100000+')
    doc.add_paragraph('')
    
    doc.add_heading('4.1.18 MENTORSHIP_AREA (Lookup Table - V2)', level=3)
    doc.add_paragraph('Lookup table for mentorship areas, extracted from MENTORSHIP table for normalization.')
    mentorship_area_schema = [
        ['AreaID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['AreaName', 'VARCHAR(100)', 'NOT NULL, UNIQUE', 'Mentorship area name']
    ]
    add_formatted_table(doc, mentorship_area_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('Sample values: Data Science, Web Development, Career Guidance, Research, Entrepreneurship')
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 4.2: JUNCTION TABLES
    # ==========================================
    doc.add_heading('4.2 Junction Tables', level=2)
    
    doc.add_paragraph(
        'Junction tables are used to implement Many-to-Many (M:N) relationships. '
        'They have composite primary keys made up of the primary keys of both entities.'
    )
    
    # ALUMNI_SKILL
    doc.add_heading('4.2.1 ALUMNI_SKILL', level=3)
    doc.add_paragraph('Junction table for ALUMNI - SKILL M:N relationship.')
    alumni_skill_schema = [
        ['PersonID', 'INT', 'NOT NULL, PK, FK to ALUMNI', 'ALUMNI reference'],
        ['SkillID', 'INT', 'NOT NULL, PK, FK to SKILL', 'SKILL reference'],
        ['ProficiencyLevel', 'VARCHAR(20)', 'CHECK (Beginner/Intermediate/Advanced/Expert)', 'Skill level']
    ]
    add_formatted_table(doc, alumni_skill_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # EVENT_REGISTRATION
    doc.add_heading('4.2.2 EVENT_REGISTRATION', level=3)
    doc.add_paragraph('Junction table for ALUMNI - EVENT M:N relationship.')
    event_reg_schema = [
        ['PersonID', 'INT', 'NOT NULL, PK, FK to ALUMNI', 'ALUMNI reference'],
        ['EventID', 'INT', 'NOT NULL, PK, FK to EVENT', 'EVENT reference'],
        ['RegistrationDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Registration date'],
        ['AttendanceStatus', 'VARCHAR(20)', 'CHECK (Registered/Attended/Cancelled/No Show)', 'Attendance status']
    ]
    add_formatted_table(doc, event_reg_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    doc.add_paragraph('')
    
    # JOB_APPLICATION (V2 Addition)
    doc.add_heading('4.2.3 JOB_APPLICATION (V2 Addition)', level=3)
    doc.add_paragraph('Junction table for ALUMNI - JOB M:N relationship (who applied to which job).')
    job_app_schema = [
        ['ApplicationID', 'INT', 'PRIMARY KEY, NOT NULL', 'Auto-increment'],
        ['JobID', 'INT', 'NOT NULL, FK to JOB', 'JOB reference'],
        ['ApplicantID', 'INT', 'NOT NULL, FK to ALUMNI', 'ALUMNI reference'],
        ['ApplicationDate', 'DATETIME', 'DEFAULT CURRENT_TIMESTAMP', 'Application date'],
        ['Status', 'VARCHAR(20)', 'CHECK (Applied/Reviewed/Shortlisted/Rejected/Accepted)', 'Application status'],
        ['ResumeLink', 'VARCHAR(255)', '', 'Resume URL']
    ]
    add_formatted_table(doc, job_app_schema, ['Attribute', 'Type', 'Constraints', 'Description'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 4.3: CONSTRAINTS SUMMARY
    # ==========================================
    doc.add_heading('4.3 Constraints Summary', level=2)
    
    # CHECK Constraints
    doc.add_heading('4.3.1 CHECK Constraints', level=3)
    check_data = [
        ['PERSON', 'Gender', 'CHECK (Gender IN (M, F, O))'],
        ['DONATION', 'PaymentMethod', 'CHECK (PaymentMethod IN (Online, Check, DD, Cash))'],
        ['JOB', 'JobType', 'CHECK (JobType IN (Full-Time, Part-Time, Contract, Internship))'],
        ['MENTORSHIP', 'Status', 'CHECK (Status IN (Active, Completed, Paused, Cancelled))'],
        ['MENTORSHIP', 'Rating', 'CHECK (Rating BETWEEN 1 AND 5)'],
        ['ADMIN', 'AccessLevel', 'CHECK (AccessLevel BETWEEN 1 AND 5)'],
        ['ALUMNI_SKILL', 'ProficiencyLevel', 'CHECK (ProficiencyLevel IN (Beginner, Intermediate, Advanced, Expert))'],
        ['EVENT_REGISTRATION', 'AttendanceStatus', 'CHECK (AttendanceStatus IN (Registered, Attended, Cancelled, No Show))'],
        ['JOB_APPLICATION', 'Status', 'CHECK (Status IN (Applied, Reviewed, Shortlisted, Rejected, Accepted))']
    ]
    add_formatted_table(doc, check_data, ['Table', 'Attribute', 'Constraint'])
    doc.add_paragraph('')
    
    # UNIQUE Constraints
    doc.add_heading('4.3.2 UNIQUE Constraints', level=3)
    unique_data = [
        ['PERSON', 'Email', 'Each email is unique'],
        ['DEPARTMENT', 'DeptName', 'Department names are unique'],
        ['DEPARTMENT', 'DeptCode', 'Department codes are unique'],
        ['SKILL', 'SkillName', 'Skill names are unique'],
        ['STUDENT', 'StudentID', 'Student IDs are unique'],
        ['DONATION', 'TransactionID', 'Transaction IDs are unique'],
        ['DONATION', 'ReceiptNumber', 'Receipt numbers are unique']
    ]
    add_formatted_table(doc, unique_data, ['Table', 'Attribute', 'Description'])
    doc.add_paragraph('')
    
    # NOT NULL Constraints
    doc.add_heading('4.3.3 NOT NULL Constraints', level=3)
    doc.add_paragraph(
        'All primary key attributes are NOT NULL. Additionally, the following attributes '
        'have NOT NULL constraints to ensure data integrity:'
    )
    not_null_data = [
        ['ALUMNI', 'GraduationYear, DeptID, BatchID', 'Required alumni information'],
        ['STUDENT', 'StudentID, EnrollmentYear, DeptID', 'Required student information'],
        ['ADMIN', 'AdminRole', 'Required admin information'],
        ['EVENT', 'EventName, EventDate, OrganizerID', 'Required event information'],
        ['DONATION', 'DonorID, Amount, DonationDate', 'Required donation information'],
        ['JOB', 'JobTitle, CompanyID, PostedBy', 'Required job information'],
        ['MENTORSHIP', 'MentorID, MenteeID, StartDate', 'Required mentorship information'],
        ['FORUM', 'ForumName, CreatedBy', 'Required forum information'],
        ['POST', 'ForumID, AuthorID, Title, Content', 'Required post information'],
        ['COMMENT', 'PostID, AuthorID, Content', 'Required comment information']
    ]
    add_formatted_table(doc, not_null_data, ['Table', 'Attributes', 'Reason'])
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 5: CONCLUSION
    # ==========================================
    doc.add_heading('5. Conclusion', level=1)
    
    doc.add_paragraph(
        'This project designs a complete database for Alumni Network and Engagement Platform. '
        'We have used all important ER and EER concepts from our DBMS course. '
        'The design covers all types of attributes, strong entities, different types of '
        'relationships, participation constraints, cardinality constraints, '
        'generalization/specialization, and normalization up to BCNF.'
    )
    
    doc.add_paragraph('The main concepts used are:')
    
    concepts_covered = [
        'All attribute types: Simple, Composite, Single-valued, Multi-valued, Derived, Stored, Key, NULL',
        'Strong entities with primary keys',
        'Binary and Unary (Recursive) relationships',
        'Total and Partial participation constraints',
        'All cardinality types: 1:1, 1:N, M:N',
        'Role names in recursive relationships',
        'Generalization/Specialization with Disjoint and Total constraints',
        'Normalization up to BCNF',
        'Complete relational schema with CHECK, UNIQUE, and NOT NULL constraints'
    ]
    
    for concept in concepts_covered:
        doc.add_paragraph(concept, style='List Bullet')
    
    doc.add_paragraph('')
    doc.add_paragraph(
        'Note: This schema does not use foreign key constraints. Referential integrity '
        'between tables is maintained at the application level.'
    )
    
    doc.add_page_break()
    
    # ==========================================
    # CHAPTER 6: REFERENCES
    # ==========================================
    doc.add_heading('6. References', level=1)
    
    references = [
        'Silberschatz, A., Korth, H.F., & Sudarshan, S. (2019). Database System Concepts (7th ed.). McGraw-Hill.',
        'Elmasri, R., & Navathe, S.B. (2015). Fundamentals of Database Systems (7th ed.). Pearson.',
        'Connolly, T., & Begg, C. (2014). Database Systems: A Practical Approach (6th ed.). Pearson.',
        'Date, C.J. (2003). An Introduction to Database Systems (8th ed.). Addison-Wesley.',
        'Ramakrishnan, R., & Gehrke, J. (2003). Database Management Systems (3rd ed.). McGraw-Hill.'
    ]
    
    for i, ref in enumerate(references, 1):
        doc.add_paragraph(f'[{i}] {ref}')
    
    # Save
    output_path = '/Users/dakshagarwal/dbms-project/laguna/report/Alumni_Network_Clean_Schema.docx'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Generated: {output_path}")


if __name__ == '__main__':
    create_report()
