"""
Page 3: Career Discovery
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_career_discovery(roadmap_data: dict, on_select_career):
    st.markdown("## 🧭 Career Discovery & Occupational Alignment")
    st.markdown(
        "Top recommended career trajectories matched against the official **O*NET 28+ Database** "
        "using hybrid TF-IDF semantic similarity, technology overlap, and interest alignment."
    )

    all_careers = roadmap_data.get("all_recommended_careers", [])
    if not all_careers:
        selected = roadmap_data.get("selected_career")
        if selected:
            all_careers = [selected]

    if not all_careers:
        st.warning("⚠️ No career recommendations available. Please generate or load a roadmap first.")
        return

    # Compatibility Bar Chart
    df_chart = pd.DataFrame([
        {
            "Career": c.get("canonical_name", c.get("title", "Role")),
            "Compatibility": c.get("compatibility_score", 0),
            "Job Zone": f"Zone {c.get('job_zone', 4)}",
            "Median Salary": f"${c.get('median_salary_usd', 100000):,}"
        }
        for c in all_careers
    ])

    fig = px.bar(
        df_chart,
        x="Compatibility",
        y="Career",
        orientation="h",
        text="Compatibility",
        color="Compatibility",
        color_continuous_scale="Purples",
        title="O*NET Occupational Compatibility Scores (%)"
    )
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=20, t=40, b=10),
        xaxis=dict(range=[0, 100], title="Match Percentage (%)"),
        yaxis=dict(autorange="reversed", title="")
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Tabs for Detailed Career Cards vs Side-by-Side Comparison
    tab_cards, tab_compare = st.tabs(["📋 Top 5 Recommended Roles", "⚖️ Side-by-Side Role Comparison"])

    with tab_cards:
        for idx, career in enumerate(all_careers):
            score = career.get("compatibility_score", 0)
            score_color = "#059669" if score >= 80 else ("#D97706" if score >= 65 else "#4F46E5")
            
            with st.container():
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 16px; border-left: 6px solid {score_color};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">
                                Match Rank #{idx+1} • O*NET SOC: {career.get('onetsoc_code')}
                            </div>
                            <h3 style="margin: 4px 0 8px 0; color: #1E1B4B; font-weight: 800;">
                                {career.get('canonical_name', career.get('title'))}
                            </h3>
                            <div style="font-size: 0.85rem; color: #475569; margin-bottom: 8px;">
                                Official O*NET Title: <i>{career.get('title')}</i>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.8rem; font-weight: 800; color: {score_color};">
                                {score}%
                            </div>
                            <div style="font-size: 0.75rem; font-weight: 600; color: #64748B;">COMPATIBILITY</div>
                        </div>
                    </div>
                    <p style="font-size: 0.92rem; color: #334155; line-height: 1.5; margin-bottom: 12px;">
                        {career.get('description')}
                    </p>
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                        <span style="font-weight: 700; color: #4338CA; font-size: 0.85rem;">Why this matches you:</span>
                        <span style="font-size: 0.88rem; color: #334155;"> {career.get('why_matched', 'Direct alignment with your stated skills and goals.')}</span>
                    </div>
                    <div style="display: flex; gap: 20px; font-size: 0.82rem; color: #64748B; flex-wrap: wrap; margin-bottom: 10px;">
                        <span>🎓 <b>Job Zone:</b> Zone {career.get('job_zone', 4)} (Considerable Preparation)</span>
                        <span>💰 <b>O*NET Median Salary:</b> ${career.get('median_salary_usd', 105000):,} / year</span>
                        <span>🔥 <b>Outlook:</b> High Growth</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_btn, col_rest = st.columns([1.5, 4])
                with col_btn:
                    if st.button(f"🎯 Target This Role", key=f"btn_target_{idx}", use_container_width=True):
                        on_select_career(career)

    with tab_compare:
        st.markdown("#### Side-by-Side Comparison of Top 2 Roles")
        if len(all_careers) >= 2:
            c1, c2 = st.columns(2)
            c_a, c_b = all_careers[0], all_careers[1]

            with c1:
                st.markdown(f"### {c_a.get('canonical_name')}")
                st.metric("Compatibility", f"{c_a.get('compatibility_score')}%")
                st.write(f"**O*NET SOC:** {c_a.get('onetsoc_code')}")
                st.write(f"**Job Zone:** Zone {c_a.get('job_zone')}")
                st.write(f"**Median Salary:** ${c_a.get('median_salary_usd'):,}/yr")
                st.write("**Top Tech Skills:**")
                st.markdown("".join([f"<span class='skill-tag'>{s}</span>" for s in c_a.get('technology_skills', [])[:8]]), unsafe_allow_html=True)

            with c2:
                st.markdown(f"### {c_b.get('canonical_name')}")
                st.metric("Compatibility", f"{c_b.get('compatibility_score')}%")
                st.write(f"**O*NET SOC:** {c_b.get('onetsoc_code')}")
                st.write(f"**Job Zone:** Zone {c_b.get('job_zone')}")
                st.write(f"**Median Salary:** ${c_b.get('median_salary_usd'):,}/yr")
                st.write("**Top Tech Skills:**")
                st.markdown("".join([f"<span class='skill-tag'>{s}</span>" for s in c_b.get('technology_skills', [])[:8]]), unsafe_allow_html=True)
        else:
            st.info("Compare requires at least 2 recommended careers.")

    # O*NET Source Reference Banner
    st.markdown("""
    <div class="onet-source-badge">
        🏛️ <b>Data Grounding:</b> Sourced from U.S. Department of Labor O*NET Occupational Database (Content Model 28+). 
        Official Reference: <a href="https://www.onetcenter.org/database.html" target="_blank" style="color:#4F46E5;">onetcenter.org</a>
    </div>
    """, unsafe_allow_html=True)
