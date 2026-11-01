"""
Page 7: Career Report & PDF Export
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
from services.pdf_service import PDFReportGenerator

def render_report_page(roadmap_data: dict):
    st.markdown("## 📄 Comprehensive Career Advisory Report")
    st.markdown(
        "Generate and download an executive-grade, multi-page career dossier formatted with "
        "ReportLab. Ideal for university faculty review, career counseling sessions, or offline study."
    )

    if not roadmap_data:
        st.warning("⚠️ No roadmap data available to generate report. Please complete onboarding or load a sample first.")
        return

    student = roadmap_data.get("student_profile", {})
    career = roadmap_data.get("selected_career", {})
    gap = roadmap_data.get("skill_gap_analysis", {})
    timeline = roadmap_data.get("timeline", [])

    col_preview, col_action = st.columns([1.5, 1])

    with col_preview:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E1B4B; margin-bottom: 12px;">📑 Dossier Executive Summary</h3>
            <div style="font-size: 0.9rem; line-height: 1.6; color: #334155;">
                <p><b>Candidate:</b> {name} ({degree}, {year})</p>
                <p><b>Target O*NET Career:</b> {career_name} (SOC {soc})</p>
                <p><b>Compatibility Match:</b> <span style="color:#059669; font-weight:700;">{score}%</span></p>
                <p><b>Identified Technical Gaps:</b> {gaps} High-Priority Competencies</p>
                <p><b>Roadmap Scope:</b> {months} Months across 5 Sequential Phases</p>
            </div>
        </div>
        """.format(
            name=student.get("full_name", "Student"),
            degree=student.get("degree_branch", "CSE"),
            year=student.get("current_year", "3rd Year"),
            career_name=career.get("canonical_name", "Target Career"),
            soc=career.get("onetsoc_code", "N/A"),
            score=career.get("compatibility_score", 85),
            gaps=len(gap.get("missing_technical_skills", [])),
            months=len(timeline) or student.get("learning_duration_months", 6)
        ), unsafe_allow_html=True)

    with col_action:
        st.markdown("### 📥 Download PDF Dossier")
        st.write("Click below to generate and stream the official PDF document:")
        
        pdf_gen = PDFReportGenerator()
        try:
            pdf_bytes = pdf_gen.generate_report(roadmap_data)
            candidate_safe = student.get("full_name", "Student").replace(" ", "_")
            file_name = f"CareerCompass_{candidate_safe}_Roadmap.pdf"

            st.download_button(
                label="⬇️ Download PDF Career Dossier",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            st.success("✅ PDF compiled successfully! Ready for immediate download.")
        except Exception as e:
            st.error(f"Error compiling PDF report: {e}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Report Contents Preview Checklist
    st.markdown("### 🔍 Dossier Table of Contents")
    toc_col1, toc_col2 = st.columns(2)
    with toc_col1:
        st.markdown("""
        - **Section 1:** Candidate Background & Academic Diagnostics
        - **Section 2:** Targeted Occupational Benchmark (O*NET 28+ Content Model)
        - **Section 3:** Multi-Agent Skill Gap & Prioritization Matrix
        """)
    with toc_col2:
        st.markdown("""
        - **Section 4:** Curated Courseware & Verified Certifications
        - **Section 5:** 5-Phase Month-by-Month Actionable Execution Timeline
        - **Section 6:** Deliverable Portfolio Capstones & Interview Readiness
        """)
