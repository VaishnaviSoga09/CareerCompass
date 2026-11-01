"""
PDF Career Report Generator for CareerCompass
SIH25094 - CSE473 Agentic AI
Uses ReportLab to compile a professional, multi-page career advisory dossier.
"""

import os
from io import BytesIO
from typing import Dict, Any, List
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle(
            'DocTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E1B4B'),
            spaceAfter=6
        )
        self.subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#6366F1'),
            spaceAfter=15
        )
        self.h2_style = ParagraphStyle(
            'SectionH2',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1E1B4B'),
            spaceBefore=14,
            spaceAfter=8
        )
        self.h3_style = ParagraphStyle(
            'SectionH3',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#4F46E5'),
            spaceBefore=8,
            spaceAfter=4
        )
        self.body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1F2937')
        )
        self.badge_style = ParagraphStyle(
            'BadgeStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#4338CA')
        )

    def generate_report(self, roadmap_data: Dict[str, Any]) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        story = []

        student = roadmap_data.get("student_profile", {})
        career = roadmap_data.get("selected_career", {})
        gap = roadmap_data.get("skill_gap_analysis", {})
        learning = roadmap_data.get("learning_recommendations", {})
        timeline = roadmap_data.get("timeline", [])

        # 1. Header Banner
        story.append(Paragraph("CareerCompass • Executive Career Advisory Dossier", self.title_style))
        story.append(Paragraph("SIH25094 • CSE473: Agentic AI Autonomous Multi-Agent Advisory System", self.subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceAfter=15))

        # 2. Student Profile Summary Table
        story.append(Paragraph("1. Candidate Background & Target Objectives", self.h2_style))
        profile_data = [
            [
                Paragraph("<b>Full Name:</b>", self.body_style),
                Paragraph(student.get("full_name", "Student Candidate"), self.body_style),
                Paragraph("<b>Target Goal:</b>", self.body_style),
                Paragraph(student.get("career_goal", "Software Specialist"), self.body_style)
            ],
            [
                Paragraph("<b>Education:</b>", self.body_style),
                Paragraph(f"{student.get('education_level', 'UG')} ({student.get('degree_branch', 'CSE')})", self.body_style),
                Paragraph("<b>Current Year:</b>", self.body_style),
                Paragraph(student.get("current_year", "3rd Year"), self.body_style)
            ],
            [
                Paragraph("<b>Experience Level:</b>", self.body_style),
                Paragraph(student.get("experience_level", "Beginner"), self.body_style),
                Paragraph("<b>Roadmap Duration:</b>", self.body_style),
                Paragraph(f"{student.get('learning_duration_months', 6)} Months", self.body_style)
            ],
            [
                Paragraph("<b>Active Skills:</b>", self.body_style),
                Paragraph(", ".join(student.get("technical_skills", [])) or "None listed", self.body_style),
                Paragraph("<b>Primary Interests:</b>", self.body_style),
                Paragraph(", ".join(student.get("interests", [])) or "Technology", self.body_style)
            ]
        ]
        t_profile = Table(profile_data, colWidths=[100, 160, 100, 170])
        t_profile.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_profile)
        story.append(Spacer(1, 15))

        # 3. Selected O*NET Career Path
        story.append(Paragraph("2. Targeted Occupational Benchmark (O*NET 28+)", self.h2_style))
        career_meta = [
            [
                Paragraph("<b>O*NET SOC Code:</b>", self.body_style),
                Paragraph(career.get("onetsoc_code", "N/A"), self.body_style),
                Paragraph("<b>Compatibility Match:</b>", self.body_style),
                Paragraph(f"<font color='#059669'><b>{career.get('compatibility_score', 85)}% Match</b></font>", self.body_style)
            ],
            [
                Paragraph("<b>Occupational Title:</b>", self.body_style),
                Paragraph(f"<b>{career.get('title', 'Target Career')}</b>", self.body_style),
                Paragraph("<b>Job Zone:</b>", self.body_style),
                Paragraph(f"Zone {career.get('job_zone', 4)} (Professional Preparation)", self.body_style)
            ]
        ]
        t_career = Table(career_meta, colWidths=[110, 180, 110, 130])
        t_career.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EEF2FF')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#C7D2FE')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_career)
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"<b>Description:</b> {career.get('description', '')}", self.body_style))
        story.append(Spacer(1, 15))

        # 4. Skill Gap Matrix
        story.append(Paragraph("3. Multi-Agent Skill Gap Matrix", self.h2_style))
        
        missing_tech = gap.get("missing_technical_skills", [])
        gap_rows = [
            [
                Paragraph("<b>Skill Dimension</b>", self.badge_style),
                Paragraph("<b>Identified Gap & Recommended Focus</b>", self.badge_style),
                Paragraph("<b>Priority Level</b>", self.badge_style)
            ]
        ]
        
        for item in missing_tech[:6]:
            skill_name = item.get("skill", "") if isinstance(item, dict) else str(item)
            priority = item.get("priority", "High") if isinstance(item, dict) else "High"
            p_color = '#DC2626' if priority.lower() == 'high' else '#D97706'
            gap_rows.append([
                Paragraph(skill_name, self.body_style),
                Paragraph(f"Industry benchmark core competency for {career.get('title', 'target role')}", self.body_style),
                Paragraph(f"<font color='{p_color}'><b>{priority}</b></font>", self.body_style)
            ])

        t_gap = Table(gap_rows, colWidths=[150, 280, 100])
        t_gap.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_gap)
        story.append(Spacer(1, 15))

        # 5. Recommended Learning Curricula & Certifications
        story.append(Paragraph("4. Curated Courses & Verified Certifications", self.h2_style))
        courses = learning.get("recommended_courses", [])
        c_rows = [
            [
                Paragraph("<b>Curriculum / Certification</b>", self.badge_style),
                Paragraph("<b>Institution / Provider</b>", self.badge_style),
                Paragraph("<b>Format & Level</b>", self.badge_style)
            ]
        ]
        for c in courses[:4]:
            c_rows.append([
                Paragraph(f"<b>{c.get('title', '')}</b>", self.body_style),
                Paragraph(c.get('provider', ''), self.body_style),
                Paragraph(f"{c.get('type', 'Free')} • {c.get('level', 'All')}", self.body_style)
            ])
            
        t_courses = Table(c_rows, colWidths=[240, 160, 130])
        t_courses.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_courses)
        story.append(Spacer(1, 15))

        # 6. Detailed Roadmap Timeline
        story.append(PageBreak())
        story.append(Paragraph("5. Personalized Step-by-Step Learning & Career Roadmap", self.title_style))
        story.append(Paragraph("Five sequential execution phases with measurable milestones and project goals.", self.subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor('#6366F1'), spaceAfter=15))

        for month in timeline:
            m_num = month.get("month", 1)
            title = month.get("title", f"Month {m_num}")
            phase = month.get("phase", "Core Development")
            milestones = month.get("action_items", []) + month.get("milestones", [])
            project_outcome = month.get("project_outcome", "")

            month_block = [
                Paragraph(f"<b>MONTH {m_num}: {title.upper()}</b> (Phase: {phase})", self.h3_style)
            ]
            
            bullet_text = ""
            for item in milestones:
                bullet_text += f"• {item}<br/>"
                
            if project_outcome:
                bullet_text += f"<b>Deliverable Milestone:</b> {project_outcome}<br/>"

            month_block.append(Paragraph(bullet_text, self.body_style))
            month_block.append(Spacer(1, 8))
            story.append(KeepTogether(month_block))

        # 7. Verification Footer
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94A3B8'), spaceAfter=8))
        story.append(Paragraph(
            f"Generated autonomously by CareerCompass Agentic Framework on {datetime.now().strftime('%B %d, %Y')} • "
            "Data grounded in O*NET Content Model 28+ Database.",
            ParagraphStyle('Footer', parent=self.styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))
        ))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
