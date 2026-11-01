"""
Page 2: Student Dashboard
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.db import DatabaseManager

def render_dashboard(student_profile: dict, roadmap_data: dict, db: DatabaseManager):
    st.markdown("## 📊 Student Career & Learning Dashboard")
    st.markdown("Real-time diagnostic profile, career alignment overview, and tracked learning progress.")

    if not student_profile:
        st.info("ℹ️ No student profile loaded. Please complete the **Student Onboarding Form** or load a **Sample Student Profile** to get started.")
        return

    # Metric Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Candidate Profile</div>
            <div class="card-value" style="font-size: 1.3rem;">{student_profile.get('full_name', 'Student')}</div>
            <div style="font-size: 0.8rem; color: #64748B;">{student_profile.get('education_level')} • {student_profile.get('degree_branch')}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        readiness = student_profile.get("academic_readiness_score", 75)
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Readiness Index</div>
            <div class="card-value" style="color: #4F46E5;">{readiness}%</div>
            <div style="font-size: 0.8rem; color: #10B981;">● Academic Baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        target_role = roadmap_data.get("selected_career", {}).get("canonical_name", student_profile.get("career_goal", "Target Career"))
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Target Career</div>
            <div class="card-value" style="font-size: 1.15rem; color: #0F172A;">{target_role[:20]}</div>
            <div style="font-size: 0.8rem; color: #64748B;">O*NET SOC: {roadmap_data.get('selected_career', {}).get('onetsoc_code', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        # Calculate completion %
        roadmap_id = roadmap_data.get("saved_db_id")
        progress_tasks = db.get_task_progress(roadmap_id) if roadmap_id else []
        total_tasks = len(progress_tasks)
        completed_tasks = sum(1 for t in progress_tasks if t.get("is_completed"))
        pct = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0

        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">Roadmap Progress</div>
            <div class="card-value" style="color: #10B981;">{pct}%</div>
            <div style="font-size: 0.8rem; color: #64748B;">{completed_tasks}/{total_tasks} Milestones Done</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Two Column Layout: Profile Diagnostic + Progress Breakdown
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown("### 👤 Diagnostic Student Profile")
        st.markdown(f"**Academic Summary:** {student_profile.get('profile_summary', 'Profile synthesized by Agent 1.')}")

        st.markdown("**Declared Technical Skills:**")
        skills_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in student_profile.get("technical_skills", [])])
        st.markdown(skills_html or "None declared", unsafe_allow_html=True)

        st.markdown("<br/>**Core Areas of Interest:**", unsafe_allow_html=True)
        interests_html = "".join([f"<span class='skill-tag' style='background:#F0FDF4; color:#166534; border-color:#BBF7D0;'>{i}</span>" for i in student_profile.get("interests", [])])
        st.markdown(interests_html or "None declared", unsafe_allow_html=True)

        st.markdown("<br/>**Agent Identified Strengths:**", unsafe_allow_html=True)
        for s in student_profile.get("identified_strengths", []):
            st.markdown(f"✅ {s}")

        st.markdown("<br/>**Target Areas for Growth:**", unsafe_allow_html=True)
        for imp in student_profile.get("areas_for_improvement", []):
            st.markdown(f"📈 {imp}")

    with col_right:
        st.markdown("### 📈 Milestone Execution Gauge")
        # Visual Progress Donut Chart
        if total_tasks > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Completed Milestones', 'Pending Milestones'],
                values=[completed_tasks, total_tasks - completed_tasks],
                hole=.6,
                marker=dict(colors=['#10B981', '#E2E8F0']),
                textinfo='label+percent'
            )])
            fig.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=240,
                annotations=[dict(text=f"{pct}%", x=0.5, y=0.5, font_size=24, showarrow=False, font_family="Inter", font_weight="bold")]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; padding: 24px; border-radius: 12px; text-align: center; color: #64748B;">
                🎯 Complete tasks in the <b>Learning Roadmap</b> tab to track completion progress!
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🗄️ Saved Roadmaps History")
        history = db.list_all_roadmaps()
        if history:
            for item in history[:4]:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem; color: #1E1B4B;">{item.get('career_title')}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">Candidate: {item.get('full_name')} • O*NET: {item.get('career_code')}</div>
                    </div>
                    <div style="background: #ECFDF5; color: #047857; font-weight: 700; font-size: 0.8rem; padding: 4px 8px; border-radius: 6px;">
                        {item.get('compatibility_score')}% Match
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No previous roadmaps recorded yet.")
