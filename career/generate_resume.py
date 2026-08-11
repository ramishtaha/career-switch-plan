from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

output_path = "/root/career-switch-plan/career/Ramish_Taha_Resume.pdf"

DARK_BLUE = HexColor("#1a3a5c")
ACCENT = HexColor("#2c5f8a")
LIGHT_GRAY = HexColor("#4a4a4a")
RULE_COLOR = HexColor("#cccccc")

styles = getSampleStyleSheet()

name_style = ParagraphStyle('NameStyle', parent=styles['Title'], fontSize=19, textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=1, fontName='Helvetica-Bold')
contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontSize=8.5, textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=3, fontName='Helvetica')
section_header_style = ParagraphStyle('SectionHeader', parent=styles['Heading1'], fontSize=10, textColor=DARK_BLUE, fontName='Helvetica-Bold', spaceBefore=4, spaceAfter=1)
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=8.5, textColor=black, fontName='Helvetica', spaceAfter=0.5, leading=11, alignment=TA_LEFT)
bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=8.5, textColor=black, fontName='Helvetica', spaceAfter=0.5, leading=10.5, leftIndent=12, bulletIndent=2, alignment=TA_LEFT)
sub_header_style = ParagraphStyle('SubHeader', parent=styles['Heading2'], fontSize=9, textColor=ACCENT, fontName='Helvetica-Bold', spaceBefore=2, spaceAfter=0)
date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=8, textColor=LIGHT_GRAY, fontName='Helvetica-Oblique', spaceAfter=0.5, alignment=TA_LEFT)
skill_cat_style = ParagraphStyle('SkillCat', parent=styles['Normal'], fontSize=8.5, fontName='Helvetica-Bold', textColor=black, spaceAfter=0, leading=10.5)

def hr_line():
    t = Table([['']], colWidths=[7.3*inch], rowHeights=[0.5])
    t.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 0.5, RULE_COLOR)]))
    return t

def section_header(title):
    return [hr_line(), Paragraph(title, section_header_style)]

def bullet(text):
    return Paragraph(text, bullet_style, bulletText='\u2022')

doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.35*inch, bottomMargin=0.35*inch)

story = []

# HEADER
story.append(Paragraph("RAMISH TAHA", name_style))
story.append(Paragraph("Mumbai, Maharashtra &nbsp;|&nbsp; ramishtaha1@gmail.com &nbsp;|&nbsp; +91 78579 42538 &nbsp;|&nbsp; linkedin.com/in/ramish-taha &nbsp;|&nbsp; github.com/ramishtaha", contact_style))

# SUMMARY
story.extend(section_header("PROFESSIONAL SUMMARY"))
story.append(Paragraph(
    "Java backend engineer with 3+ years of experience building and modernizing enterprise banking platforms at TCS. "
    "Led migration of TCS BaNCS from monolithic architecture to cloud-native microservices, driving 40%+ improvement in "
    "system resilience and 65% reduction in deployment times. Hands-on expertise in Spring Boot, Kafka event-driven "
    "architecture, REST API design, and hybrid cloud deployment (AWS/GCP). Banking domain depth in risk management, "
    "market data, and payment systems. Seeking backend engineering roles at BFSI GCCs and product companies.",
    body_style
))

# SKILLS
story.extend(section_header("TECHNICAL SKILLS"))
skills_data = [
    [Paragraph("<b>Languages:</b>", skill_cat_style), Paragraph("Java (17, 21), SQL, Python, Shell Scripting", body_style)],
    [Paragraph("<b>Frameworks:</b>", skill_cat_style), Paragraph("Spring Boot, Spring Cloud (Gateway, Eureka), Spring Data JPA, REST API Design", body_style)],
    [Paragraph("<b>DevOps &amp; Cloud:</b>", skill_cat_style), Paragraph("AWS (EC2, S3, Lambda, IAM, VPC, CloudFormation), Docker, Jenkins, Kubernetes, DigitalOcean", body_style)],
    [Paragraph("<b>Messaging &amp; Data:</b>", skill_cat_style), Paragraph("Apache Kafka, PostgreSQL, H2, PGAdmin, DBeaver", body_style)],
    [Paragraph("<b>Tools:</b>", skill_cat_style), Paragraph("Git, Maven, IntelliJ IDEA, Postman, Swagger", body_style)],
    [Paragraph("<b>Practices:</b>", skill_cat_style), Paragraph("Microservices Architecture, Event-Driven Design, CI/CD Automation, Code Review, Agile", body_style)],
    [Paragraph("<b>Domain:</b>", skill_cat_style), Paragraph("Banking &amp; Financial Services (TCS BaNCS), Risk Management, Market Data, Fund Transfer, Limits Management", body_style)],
]
skills_table = Table(skills_data, colWidths=[1.1*inch, 6.2*inch])
skills_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 2)]))
story.append(skills_table)

# EXPERIENCE
story.extend(section_header("PROFESSIONAL EXPERIENCE"))
story.append(Paragraph("<b>Tata Consultancy Services (TCS)</b> \u2014 Mumbai, India", sub_header_style))
story.append(Paragraph("<b>System Engineer</b> &nbsp;|&nbsp; Oct 2023 \u2013 Present &nbsp;|&nbsp; <i>TCS BaNCS \u2014 Global Banking Platform</i>", date_style))
story.append(Paragraph("<i>Tech: Java, Spring Boot, Kafka, Spring Cloud, AWS/GCP, Docker, Jenkins</i>", body_style))
story.append(Spacer(1,1))
story.append(bullet("Directed a team of 5 junior developers in migrating TCS BaNCS from monolithic to microservices architecture"))
story.append(bullet("Designed and implemented distributed, event-driven architecture using Kafka and Spring Cloud, increasing system fault tolerance by 50%"))
story.append(bullet("Led end-to-end lifecycle for 4+ microservices \u2014 from architectural design to deployment in hybrid cloud environments (AWS/GCP)"))
story.append(bullet("Engineered inter-module communication using scalable event-driven Kafka architecture for real-time data flow"))
story.append(bullet("Championed adoption of new technologies and agile processes under tight delivery deadlines"))
story.append(bullet("Instituted rigorous code reviews and testing frameworks, reducing production bugs by 27%"))
story.append(Paragraph("<b>Domain modules:</b>", body_style))
story.append(bullet("<b>Risk State Management (RSM)</b> \u2014 Led microservices handling risk state transitions and limit enforcement for banking operations"))
story.append(bullet("<b>Market Info Service</b> \u2014 Built real-time market data distribution and pricing service for downstream consumers"))
story.append(bullet("<b>Limits Management</b> \u2014 Developed credit, trading, and exposure limit validation framework with breach notifications"))
story.append(bullet("<b>QPP (Low-Code Platform)</b> \u2014 Built business logic workflows on TCS QPP accelerating feature delivery across banking modules"))
story.append(Spacer(1,3))
story.append(Paragraph("<b>Assistant System Engineer Trainee</b> &nbsp;|&nbsp; Oct 2022 \u2013 Sep 2023 &nbsp;|&nbsp; <i>TCS BaNCS</i>", date_style))
story.append(bullet("Developed and maintained RESTful APIs for mission-critical banking modules: Fund Transfer, Paper Remittance, Account Balance"))
story.append(bullet("Automated build/release management using Shell Scripts, streamlining workflows for 20+ modules"))
story.append(bullet("Used SQL for database querying and Swagger for comprehensive API documentation"))

# PROJECTS
story.extend(section_header("PROJECTS"))
story.append(bullet("<b>High Availability Web App</b> (AWS CloudFormation, EC2, S3, ALB) \u2014 Built HA infrastructure with multi-AZ deployment, auto-scaling, and Application Load Balancer"))
story.append(bullet("<b>Jenkins Multistage Pipeline</b> (Jenkins, AWS S3, Git) \u2014 Implemented automated website deployment with build-triggered CI/CD to AWS S3"))

# CERTIFICATIONS
story.extend(section_header("CERTIFICATIONS"))
story.append(bullet("AWS Certified Cloud Practitioner \u2014 June 2023"))
story.append(bullet("Cloud Engineer Specialization (Google Cloud) \u2014 April 2020"))

# EDUCATION
story.extend(section_header("EDUCATION"))
story.append(Paragraph("<b>Bachelor of Computer Science and Engineering</b> &nbsp;|&nbsp; Integral University, Lucknow, UP &nbsp;|&nbsp; July 2018 \u2013 June 2022", body_style))

doc.build(story)

# Verify
import pdfplumber
with pdfplumber.open(output_path) as pdf:
    pages = len(pdf.pages)
    print(f"PDF generated: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")
    print(f"Pages: {pages}")
    for i, p in enumerate(pdf.pages):
        t = p.extract_text() or ''
        print(f"--- Page {i+1} ({len(t)} chars) ---")
        print(t[:300])
