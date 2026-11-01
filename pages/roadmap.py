"""
Page 5: Learning Roadmap
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
from database.db import DatabaseManager

def render_learning_roadmap(roadmap_data: dict, db: DatabaseManager):
    st.markdown("## 🗺️ Actionable Learning & Career Roadmap")
    st.markdown(
        "A customized 5-phase execution plan synthesized by **Agent 5: Roadmap Planning Agent**. "
        "Complete monthly tasks to track your journey toward career readiness."
    )

    timeline = roadmap_data.get("timeline", [])
    roadmap_id = roadmap_data.get("saved_db_id")
    target_career = roadmap_data.get("selected_career", {})
    learning_recs = roadmap_data.get("learning_recommendations", {})

    if not timeline:
        st.warning("⚠️ No roadmap timeline available. Please generate or load a roadmap first.")
        return

    # Phase Summary Header Pills
    phases = roadmap_data.get("phases_summary", [])
    p_cols = st.columns(len(phases) if phases else 5)
    for idx, p in enumerate(phases):
        with p_cols[idx]:
            st.markdown(f"""
            <div style="background: #EEF2FF; border: 1px solid #C7D2FE; padding: 10px; border-radius: 10px; text-align: center; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #4F46E5;">{p.get('phase_name', f'Phase {idx+1}')}</div>
                <div style="font-size: 0.72rem; color: #475569; margin-top: 4px;">{p.get('focus', '')[:45]}...</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Fetch stored progress tasks from SQLite
    task_progress = db.get_task_progress(roadmap_id) if roadmap_id else []
    progress_lookup = {t["task_id"]: bool(t["is_completed"]) for t in task_progress}

    # Month by Month Timeline Display
    for month_data in timeline:
        m_num = month_data.get("month", 1)
        phase_name = month_data.get("phase", "Core Skills")
        title = month_data.get("title", f"Month {m_num}")
        action_items = month_data.get("action_items", [])
        milestones = month_data.get("milestones", [])
        project_outcome = month_data.get("project_outcome", "")

        with st.container():
            st.markdown(f"""
            <div class="timeline-card">
                <span class="timeline-phase-tag">{phase_name.upper()}</span>
                <div class="timeline-month-title">📅 Month {m_num}: {title}</div>
            </div>
            """, unsafe_allow_html=True)

            col_tasks, col_proj = st.columns([1.5, 1])

            with col_tasks:
                st.markdown("**Actionable Learning Tasks:**")
                all_tasks = action_items + milestones
                for t_idx, task_desc in enumerate(all_tasks):
                    task_id = f"m{m_num}_task{t_idx+1}"
                    current_val = progress_lookup.get(task_id, False)

                    # Interactive checkbox with database persistence
                    cb_key = f"cb_{roadmap_id}_{task_id}"
                    checked = st.checkbox(task_desc, value=current_val, key=cb_key)

                    if checked != current_val and roadmap_id:
                        db.update_task_progress(roadmap_id, task_id, checked)
                        progress_lookup[task_id] = checked
                        st.rerun()

            with col_proj:
                if project_outcome:
                    st.markdown(f"""
                    <div class="project-deliverable-box">
                        <div style="font-weight: 700; color: #4338CA; font-size: 0.85rem; margin-bottom: 4px;">
                            🏆 Deliverable Portfolio Milestone
                        </div>
                        <div style="font-weight: 600; color: #0F172A; font-size: 0.95rem;">
                            {project_outcome}
                        </div>
                        <div style="font-size: 0.78rem; color: #64748B; margin-top: 6px;">
                            Publish to GitHub with a README and automated tests.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr style='border: none; border-top: 1px dashed #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)

    # Curated Courseware and Certifications Section
    st.markdown("### 📚 Curated Courses & Verified Industry Certifications")
    c_tab1, c_tab2 = st.tabs(["🎓 Verified Courses", "📜 Professional Certifications"])

    with c_tab1:
        courses = learning_recs.get("recommended_courses", [])
        if courses:
            for c in courses:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="font-weight: 700; font-size: 1rem; color: #1E1B4B;">
                                <a href="{c.get('url')}" target="_blank" style="text-decoration: none; color: #4F46E5;">
                                    {c.get('title')} ↗
                                </a>
                            </div>
                            <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">
                                🏛️ Provider: <b>{c.get('provider')}</b> • Instructor: {c.get('instructor', 'Expert')}
                            </div>
                        </div>
                        <div style="background: #F1F5F9; color: #334155; font-size: 0.78rem; font-weight: 700; padding: 4px 8px; border-radius: 6px;">
                            ⭐ {c.get('rating', 4.8)}/5.0
                        </div>
                    </div>
                    <p style="font-size: 0.86rem; color: #475569; margin: 8px 0 6px 0;">{c.get('description')}</p>
                    <div style="font-size: 0.78rem; color: #64748B;">
                        ⏱️ Duration: <b>{c.get('duration_weeks', 8)} Weeks</b> • Level: <b>{c.get('level')}</b> • Format: <b>{c.get('type')}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No course catalog matches found.")

    with c_tab2:
        certs = learning_recs.get("certifications", [])
        if certs:
            for cert in certs:
                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px; padding: 12px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: #0F172A; font-size: 0.92rem;">
                                <a href="{cert.get('url')}" target="_blank" style="text-decoration: none; color: #0F172A;">
                                    🛡️ {cert.get('title')} ↗
                                </a>
                            </div>
                            <div style="font-size: 0.8rem; color: #64748B;">Issuer: <b>{cert.get('issuer')}</b></div>
                        </div>
                        <span style="background: #EEF2FF; color: #4338CA; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px;">
                            {cert.get('cost', 'Exam Available')}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
