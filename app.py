"""
CareerCompass – AI-Powered Career & Education Advisor
SIH25094 • Course: CSE473 – Agentic AI

Central Streamlit Application & Multi-Agent Orchestration Hub.
"""

import os
import json
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Page Setup
st.set_page_config(
    page_title="CareerCompass – AI Career Advisor",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Stylesheet
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Import Project Services & Pages
from core.llm import LLMProvider
from services.onet_service import ONetService
from services.recommendation_service import RecommendationService
from database.db import DatabaseManager
from core.orchestrator import CareerCompassOrchestrator

from pages.landing import render_landing_page
from pages.dashboard import render_dashboard
from pages.career_discovery import render_career_discovery
from pages.skill_gap import render_skill_gap_analysis
from pages.roadmap import render_learning_roadmap
from pages.chatbot import render_chatbot
from pages.report import render_report_page

# Singleton Resources
@st.cache_resource
def get_services():
    llm = LLMProvider()
    onet = ONetService()
    recommender = RecommendationService()
    db = DatabaseManager()
    orchestrator = CareerCompassOrchestrator(
        llm_provider=llm,
        onet_service=onet,
        recommendation_service=recommender,
        db_manager=db
    )
    return llm, onet, recommender, db, orchestrator

llm, onet, recommender, db, orchestrator = get_services()

# Session State Initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "Landing Page"

if "student_profile" not in st.session_state:
    st.session_state.student_profile = None

if "roadmap_data" not in st.session_state:
    st.session_state.roadmap_data = None

if "agent_execution_logs" not in st.session_state:
    st.session_state.agent_execution_logs = {}

# Helper to load sample roadmap
def load_sample_profile(sample_name: str):
    base_dir = os.path.dirname(__file__)
    file_map = {
        "Sample 1: AI/ML Engineer (Aarav)": "ai_ml_engineer.json",
        "Sample 2: Data Scientist (Priya)": "data_scientist.json",
        "Sample 3: Software & Cloud Engineer (Rohan)": "software_cloud_engineer.json"
    }
    filename = file_map.get(sample_name)
    if filename:
        path = os.path.join(base_dir, "sample_roadmaps", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.roadmap_data = data
                st.session_state.student_profile = data.get("student_profile", {})
                st.session_state.current_page = "Student Dashboard"
                st.toast(f"✅ Successfully loaded {sample_name}!", icon="🎯")

# ====================================================
# SIDEBAR NAVIGATION & CONTROLS
# ====================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        <span style="font-size: 2rem;">🧭</span>
        <div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #1E1B4B; letter-spacing: -0.5px;">CareerCompass</div>
            <div style="font-size: 0.72rem; font-weight: 600; color: #6366F1; letter-spacing: 0.5px;">SIH25094 • CSE473 AGENTIC AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Navigation Menu
    pages = [
        ("🏠 Landing Page", "Landing Page"),
        ("📊 Student Dashboard", "Student Dashboard"),
        ("🧭 Career Discovery", "Career Discovery"),
        ("🔍 Skill Gap Analysis", "Skill Gap Analysis"),
        ("🗺️ Learning Roadmap", "Learning Roadmap"),
        ("💬 AI Career Chat", "AI Career Chat"),
        ("📄 Career Report (PDF)", "Career Report")
    ]

    selected_page = st.radio(
        "Navigation",
        [label for label, val in pages],
        index=[val for label, val in pages].index(st.session_state.current_page) if st.session_state.current_page in [val for label, val in pages] else 0,
        label_visibility="collapsed"
    )
    for label, val in pages:
        if selected_page == label:
            st.session_state.current_page = val

    st.markdown("---")

    # Sample Roadmaps Switcher
    st.markdown("### ⚡ Load Sample Profile")
    st.caption("Demonstrate pre-computed pipeline roadmaps without manual form entry:")
    sample_choice = st.selectbox(
        "Select a Benchmark Profile:",
        [
            "Select Sample...",
            "Sample 1: AI/ML Engineer (Aarav)",
            "Sample 2: Data Scientist (Priya)",
            "Sample 3: Software & Cloud Engineer (Rohan)"
        ],
        label_visibility="collapsed"
    )
    if sample_choice != "Select Sample...":
        load_sample_profile(sample_choice)

    st.markdown("---")

    # LLM Provider Status
    st.markdown("### 🔌 AI Engine Status")
    mode_text = llm.active_mode.upper()
    if "GEMINI" in mode_text:
        badge_color = "#10B981"
        badge_label = "Gemini API (Active)"
    elif "OPENAI" in mode_text:
        badge_color = "#3B82F6"
        badge_label = "OpenAI API (Active)"
    else:
        badge_color = "#8B5CF6"
        badge_label = "Autonomous O*NET Engine"

    st.markdown(f"""
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px; font-size: 0.8rem;">
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: {badge_color}; margin-right: 6px;"></span>
        <b>Provider:</b> {badge_label}
    </div>
    """, unsafe_allow_html=True)
    st.caption("O*NET 28+ Database • 100% Grounded")


# ====================================================
# STUDENT ONBOARDING MODAL / FORM EXPANDER
# ====================================================
show_onboarding = st.sidebar.button("📝 Student Onboarding Form", use_container_width=True, type="secondary")

# Main Onboarding Expander
with st.expander("📝 Student Onboarding & Career Profile Form", expanded=(show_onboarding or st.session_state.student_profile is None)):
    st.markdown("#### Enter your academic background and career aspiration to initialize the 5-Agent pipeline:")
    
    with st.form("student_onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("1. Full Name*", value="Devansh Verma", placeholder="e.g. Rahul Sharma")
            education_level = st.selectbox("2. Current Education Level*", ["Undergraduate", "Postgraduate", "Diploma", "School"], index=0)
            degree_branch = st.selectbox("3. Degree / Branch*", ["CSE", "IT", "ECE", "EEE", "Mechanical", "Other"], index=0)
            current_year = st.selectbox("4. Current Year of Study*", ["1st Year", "2nd Year", "3rd Year", "4th Year / Final Year", "Graduated"], index=2)
            experience_level = st.select_slider("8. Experience Level*", options=["Beginner", "Intermediate", "Advanced"], value="Beginner")

        with col2:
            career_goal = st.text_input("7. Preferred Career Goal*", value="AI & Machine Learning Engineer", placeholder="e.g. Cloud Architect, Data Scientist")
            duration = st.selectbox("9. Preferred Learning Duration*", ["3 Months", "6 Months", "12 Months", "18 Months"], index=1)
            duration_months = int(duration.split()[0])
            learning_pref = st.selectbox("10. Learning Preference*", ["Hands-on Projects", "Video Courses", "Documentation", "Interactive Learning"], index=0)

        # Multi-select Skills and Interests
        st.markdown("**5. Technical Skills** *(Select all that apply and add custom)*")
        common_skills = [
            "Python", "Java", "C++", "SQL", "Machine Learning", 
            "Data Analysis", "Web Development", "Cloud Computing", "Docker", "Git", "React", "Linux"
        ]
        selected_skills = st.multiselect("Pre-defined Skills:", common_skills, default=["Python", "SQL", "Git"])
        custom_skills = st.text_input("Enter additional custom skills (comma-separated):", placeholder="e.g. PyTorch, FastApi, Pandas")
        if custom_skills:
            for s in custom_skills.split(","):
                if s.strip() and s.strip() not in selected_skills:
                    selected_skills.append(s.strip())

        st.markdown("**6. Areas of Interest** *(Select all that apply and add custom)*")
        common_interests = [
            "Artificial Intelligence", "Machine Learning", "Data Science", 
            "Software Development", "Cybersecurity", "Web Development", 
            "Cloud Computing", "Business Analytics", "Robotics"
        ]
        selected_interests = st.multiselect("Pre-defined Interests:", common_interests, default=["Artificial Intelligence", "Machine Learning"])
        custom_interests = st.text_input("Enter additional custom interests (comma-separated):", placeholder="e.g. Deep Learning, NLP")
        if custom_interests:
            for i in custom_interests.split(","):
                if i.strip() and i.strip() not in selected_interests:
                    selected_interests.append(i.strip())

        submitted = st.form_submit_button("⚡ Run Multi-Agent Execution Pipeline", type="primary", use_container_width=True)

        if submitted:
            if not full_name.strip():
                st.error("Please enter candidate's full name.")
            elif not selected_skills:
                st.error("Please specify at least one technical skill.")
            else:
                student_payload = {
                    "full_name": full_name,
                    "education_level": education_level,
                    "degree_branch": degree_branch,
                    "current_year": current_year,
                    "technical_skills": selected_skills,
                    "interests": selected_interests,
                    "career_goal": career_goal,
                    "experience_level": experience_level,
                    "learning_duration_months": duration_months,
                    "learning_preference": learning_pref
                }

                # Visual Agent Execution Monitor Container
                st.markdown("### 🖥️ Agent Execution Monitor (Real-Time Pipeline)")
                monitor_container = st.empty()

                # Execution Callback to update UI in real-time
                agent_states = {
                    "Student Profiling Agent": {"status": "PENDING", "msg": "Queued", "data": None},
                    "Career Discovery Agent": {"status": "PENDING", "msg": "Queued", "data": None},
                    "Skill Gap Analysis Agent": {"status": "PENDING", "msg": "Queued", "data": None},
                    "Learning Recommendation Agent": {"status": "PENDING", "msg": "Queued", "data": None},
                    "Roadmap Planning Agent": {"status": "PENDING", "msg": "Queued", "data": None}
                }

                def update_monitor(agent_name, status, msg, data):
                    agent_states[agent_name] = {"status": status, "msg": msg, "data": data}
                    cards_html = ""
                    for name, state in agent_states.items():
                        st_lower = state["status"].lower()
                        badge_class = "completed" if st_lower == "completed" else ("running" if st_lower == "running" else "pending")
                        cards_html += f"""
                        <div class="agent-node status-{st_lower}">
                            <div class="agent-header">
                                <span class="agent-name">{name}</span>
                                <span class="agent-badge {badge_class}">{state['status']}</span>
                            </div>
                            <div style="font-size: 0.84rem; color: #475569;">{state['msg']}</div>
                        </div>
                        """
                    monitor_container.markdown(cards_html, unsafe_allow_html=True)
                    time.sleep(0.3)  # Visibly demonstrate sequential execution

                with st.spinner("Executing Autonomous Multi-Agent Reasoning Chains..."):
                    generated_roadmap = orchestrator.run_pipeline(
                        raw_student_input=student_payload,
                        progress_callback=update_monitor
                    )

                st.session_state.roadmap_data = generated_roadmap
                st.session_state.student_profile = generated_roadmap.get("student_profile")
                st.session_state.current_page = "Student Dashboard"
                st.success("🎉 Multi-Agent Roadmap Generated & Persisted Successfully!")
                st.rerun()


# ====================================================
# PAGE ROUTING LOGIC
# ====================================================
def nav_to_onboarding():
    st.session_state.current_page = "Student Dashboard"

def on_select_career(career_dict):
    st.session_state.roadmap_data["selected_career"] = career_dict
    # Re-run Skill Gap and Roadmap with the newly targeted role
    with st.spinner(f"Re-aligning roadmap toward {career_dict.get('canonical_name')}..."):
        re_gap = orchestrator.agent_skill_gap.execute(st.session_state.student_profile, career_dict)
        re_recs = orchestrator.agent_learning.execute(st.session_state.student_profile, re_gap)
        re_roadmap = orchestrator.agent_roadmap.execute(
            student_profile=st.session_state.student_profile,
            career_discovery={"selected_career": career_dict, "top_careers": st.session_state.roadmap_data.get("all_recommended_careers", [])},
            skill_gap=re_gap["skill_gap_analysis"],
            learning_recs=re_recs["learning_recommendations"]
        )
        st.session_state.roadmap_data = re_roadmap
        st.toast(f"🎯 Target role updated to {career_dict.get('canonical_name')}!", icon="✅")
        st.rerun()

current = st.session_state.current_page

if current == "Landing Page":
    render_landing_page(on_get_started=lambda: load_sample_profile("Sample 1: AI/ML Engineer (Aarav)"))

elif current == "Student Dashboard":
    render_dashboard(
        student_profile=st.session_state.student_profile,
        roadmap_data=st.session_state.roadmap_data or {},
        db=db
    )

elif current == "Career Discovery":
    render_career_discovery(
        roadmap_data=st.session_state.roadmap_data or {},
        on_select_career=on_select_career
    )

elif current == "Skill Gap Analysis":
    render_skill_gap_analysis(
        roadmap_data=st.session_state.roadmap_data or {}
    )

elif current == "Learning Roadmap":
    render_learning_roadmap(
        roadmap_data=st.session_state.roadmap_data or {},
        db=db
    )

elif current == "AI Career Chat":
    render_chatbot(
        student_profile=st.session_state.student_profile or {},
        roadmap_data=st.session_state.roadmap_data or {},
        llm=llm
    )

elif current == "Career Report":
    render_report_page(
        roadmap_data=st.session_state.roadmap_data or {}
    )

# Footer
st.markdown("<br/><br/>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.8rem; border-top: 1px solid #E2E8F0; padding-top: 20px;">
    CareerCompass AI • SIH25094 • CSE473: Agentic AI Capstone Project<br/>
    Powered by Multi-Agent Architecture & Official O*NET Occupational Database (U.S. Dept. of Labor)
</div>
""", unsafe_allow_html=True)
