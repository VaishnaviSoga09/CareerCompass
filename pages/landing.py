"""
Page 1: Landing Page
CareerCompass - SIH25094 - CSE473 Agentic AI
"""

import streamlit as st

def render_landing_page(on_get_started):
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">🚀 SIH25094 • CSE473 AGENTIC AI CAPSTONE</div>
        <div class="hero-title">CareerCompass</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: #E0E7FF; margin-bottom: 14px;">
            AI-Powered Career & Education Advisory System
        </div>
        <div class="hero-subtitle">
            Autonomous multi-agent intelligence meets the official <b>O*NET Occupational Database</b>. 
            Transform your academic background, current technical skills, and career goals into an actionable, 
            personalized 5-phase career mastery roadmap with precision skill-gap diagnostics.
        </div>
        <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 9999px; font-size: 0.85rem;">
                🧠 5 Specialized AI Agents
            </span>
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 9999px; font-size: 0.85rem;">
                📊 O*NET 28+ Database Grounded
            </span>
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 9999px; font-size: 0.85rem;">
                🎯 Explainable Skill-Gap Matrix
            </span>
            <span style="background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 9999px; font-size: 0.85rem;">
                📄 Instant PDF Dossier
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("🚀 Get Started Now", type="primary", use_container_width=True):
            on_get_started()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Multi-Agent Architecture Flow Diagram
    st.markdown("### 🤖 Autonomous Multi-Agent Advisory Architecture")
    st.markdown(
        "CareerCompass operates a sequential multi-agent pipeline where each specialized agent "
        "executes distinct responsibilities and transfers structured outputs down the reasoning chain."
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #6366F1;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">👤</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E1B4B;">Agent 1: Profiling</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 6px;">
                Synthesizes academic background, skills, and readiness scores.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #3B82F6;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🧭</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E1B4B;">Agent 2: Discovery</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 6px;">
                Matches against official O*NET occupational benchmarks.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #EC4899;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🔍</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E1B4B;">Agent 3: Skill Gap</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 6px;">
                Isolates missing technical & soft skills by priority level.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #F59E0B;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📚</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E1B4B;">Agent 4: Learning</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 6px;">
                Curates verified free/paid courses and certifications.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="metric-card" style="border-top: 4px solid #10B981;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🗺️</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E1B4B;">Agent 5: Roadmap</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 6px;">
                Builds 5-phase month-by-month actionable timeline.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Key Features Section
    st.markdown("### ✨ Platform Capabilities & Scientific Grounding")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #4F46E5; margin-bottom: 8px;">📊 Real O*NET 28+ Integration</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Direct integration with the U.S. Department of Labor's O*NET Occupational Database. 
                Utilizes official SOC codes, job zones, and technology skill taxonomies.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with f_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #4F46E5; margin-bottom: 8px;">🎯 Explainable Matching Engine</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Hybrid scoring powered by TF-IDF corpus vectorization, cosine similarity, 
                and Jaccard technology overlap. No black-box or fabricated metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with f_col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #4F46E5; margin-bottom: 8px;">⚡ 5-Phase Progressive Timeline</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Roadmaps are divided into Foundation, Core Skills, Advanced Skills, Capstones, 
                and Placement Preparation with measurable monthly deliverables.
            </p>
        </div>
        """, unsafe_allow_html=True)
