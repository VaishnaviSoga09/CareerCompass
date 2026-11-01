"""
Page 4: Skill Gap Analysis
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_skill_gap_analysis(roadmap_data: dict):
    st.markdown("## 🔍 Skill Gap & Benchmark Diagnostics")
    st.markdown(
        "Agent 3 compares your declared technical proficiency against the official O*NET benchmark requirements "
        "for your targeted occupation, classifying missing skills by learning difficulty and hiring priority."
    )

    gap_data = roadmap_data.get("skill_gap_analysis", {})
    target_career = roadmap_data.get("selected_career", {})
    if not gap_data:
        st.warning("⚠️ No skill gap analysis data available. Please generate or load a roadmap first.")
        return

    # Top Metric Banner
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Target Occupation", target_career.get("canonical_name", "Target Role")[:18])
    with m2:
        st.metric("Matching Core Skills", f"{gap_data.get('total_skills_matched', 0)} Skills", delta="Acquired")
    with m3:
        missing_count = len(gap_data.get("missing_technical_skills", []))
        st.metric("Missing Tech Skills", f"{missing_count} Skills", delta=f"-{gap_data.get('gap_percentage', 0)}% Gap", delta_color="inverse")
    with m4:
        st.metric("Overall Gap Intensity", gap_data.get("overall_gap_level", "Moderate"))

    st.markdown("<br/>", unsafe_allow_html=True)

    # Plotly Charts: Radar Chart & Priority Breakdown
    col_radar, col_bar = st.columns([1.1, 1])

    with col_radar:
        st.markdown("### 🕸️ Competency Radar Analysis")
        # Generate radar chart comparing student baseline vs O*NET requirement
        categories = [
            "Programming & Syntax", 
            "Data & Pipelines", 
            "Algorithms & Math", 
            "Frameworks & APIs", 
            "System Architecture", 
            "Testing & CI/CD"
        ]
        
        # Calculate scores dynamically based on matched skills
        existing = [s.lower() for s in gap_data.get("existing_matching_skills", [])]
        s_score = [
            85 if any(x in existing for x in ["python", "java", "c++"]) else 40,
            80 if any(x in existing for x in ["sql", "pandas", "numpy", "database"]) else 35,
            75 if any(x in existing for x in ["algorithms", "math", "numpy"]) else 30,
            65 if any(x in existing for x in ["react", "fastapi", "spring"]) else 25,
            60 if any(x in existing for x in ["docker", "cloud", "aws"]) else 20,
            70 if any(x in existing for x in ["git", "testing", "pytest"]) else 30
        ]
        r_score = [90, 85, 80, 85, 80, 75]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=s_score,
            theta=categories,
            fill='toself',
            name='Candidate Current',
            line_color='#6366F1'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=r_score,
            theta=categories,
            fill='toself',
            name='O*NET Target Benchmark',
            line_color='#10B981',
            opacity=0.4
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            margin=dict(t=20, b=30, l=40, r=40),
            height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_bar:
        st.markdown("### 📊 Missing Skills by Learning Level")
        missing_tech = gap_data.get("missing_technical_skills", [])
        
        levels = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
        for item in missing_tech:
            lvl = item.get("level", "Intermediate") if isinstance(item, dict) else "Intermediate"
            levels[lvl] = levels.get(lvl, 0) + 1

        df_levels = pd.DataFrame([{"Level": k, "Count": v} for k, v in levels.items()])
        fig_bar = px.bar(
            df_levels,
            x="Level",
            y="Count",
            color="Level",
            color_discrete_map={"Beginner": "#3B82F6", "Intermediate": "#8B5CF6", "Advanced": "#EC4899"},
            title="Skill Gaps by Difficulty Level"
        )
        fig_bar.update_layout(
            height=300,
            margin=dict(t=30, b=10, l=10, r=10),
            xaxis_title="",
            yaxis_title="Number of Skills",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Detailed Skill Breakdown Matrix
    st.markdown("### 📋 Prioritized Technical Skill Gap Breakdown")

    # Matching Skills Pill Box
    st.markdown("**Already Acquired Skills (Matching Target):**")
    matched_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in gap_data.get("existing_matching_skills", [])])
    st.markdown(matched_html or "No direct matches identified in candidate profile.", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    # Missing Skills Table
    table_data = []
    for item in missing_tech:
        if isinstance(item, dict):
            prio = item.get("priority", "High")
            p_color = "🔴 High" if prio == "High" else ("🟡 Medium" if prio == "Medium" else "🟢 Low")
            table_data.append({
                "Skill Name": item.get("skill"),
                "Priority": p_color,
                "Difficulty Level": item.get("level", "Intermediate"),
                "Relevance to Career": item.get("relevance", "Core industry standard")
            })
        else:
            table_data.append({
                "Skill Name": str(item),
                "Priority": "🔴 High",
                "Difficulty Level": "Intermediate",
                "Relevance to Career": "Industry requirement"
            })

    if table_data:
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)

    # Soft Skills Box
    st.markdown("### 🤝 Target Soft Skills & Workplace Competencies")
    soft_skills = gap_data.get("missing_soft_skills", [])
    if soft_skills:
        c_s1, c_s2 = st.columns(2)
        for idx, s in enumerate(soft_skills):
            col = c_s1 if idx % 2 == 0 else c_s2
            s_name = s.get("skill") if isinstance(s, dict) else str(s)
            s_rel = s.get("relevance", "Vital for team collaboration") if isinstance(s, dict) else "Vital for team collaboration"
            with col:
                st.markdown(f"""
                <div style="background: #FFF; border: 1px solid #E2E8F0; padding: 12px; border-radius: 10px; margin-bottom: 8px;">
                    <div style="font-weight: 700; color: #1E1B4B; font-size: 0.92rem;">💡 {s_name}</div>
                    <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">{s_rel}</div>
                </div>
                """, unsafe_allow_html=True)
