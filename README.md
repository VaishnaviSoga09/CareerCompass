# CareerCompass – AI-Powered Career & Education Advisor
### Project ID: SIH25094 | Course: CSE473 – Agentic AI

🚀 Live Demo: https://careercompass09.streamlit.app/

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![O*NET 28+](https://img.shields.io/badge/O*NET-Content%20Model%2028+-059669.svg)](https://www.onetcenter.org/database.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests Passing](https://img.shields.io/badge/Tests-13%20Passed-10B981.svg)]()

CareerCompass is an autonomous, multi-agent artificial intelligence web application engineered to solve the disconnect between university curricula, student skill development, and industry hiring standards. Powered by a sequential 5-agent architecture and grounded in the official **U.S. Department of Labor O*NET Occupational Database (Content Model 28+)**, CareerCompass transforms student profiles into personalized, explainable, 5-phase career mastery roadmaps.

---

## 📌 Table of Contents
1. [Problem Statement & Objectives](#-problem-statement--objectives)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Autonomous Multi-Agent Architecture](#-autonomous-multi-agent-architecture)
5. [O*NET Dataset Integration & Grounding](#-onet-dataset-integration--grounding)
6. [Technology Stack](#-technology-stack)
7. [Installation & Setup Guide](#-installation--setup-guide)
8. [Running the Application](#-running-the-application)
9. [Running the Test Suite](#-running-the-test-suite)
10. [Three Pre-Generated Sample Roadmaps](#-three-pre-generated-sample-roadmaps)
11. [Page-by-Page Application Walkthrough](#-page-by-page-application-walkthrough)
12. [Database Schema & Persistence](#-database-schema--persistence)
13. [Limitations & Future Scope](#-limitations--future-scope)

---

## 🎯 Problem Statement & Objectives

### The Problem
Engineering and computer science students frequently struggle to identify viable career trajectories tailored to their specific technical toolkits, academic years, and interests. Generic career advice lacks grounding in empirical occupational data, fails to identify specific technical gaps, and offers vague suggestions rather than actionable, month-by-month roadmaps.

### Project Objectives
- **Empirical Grounding:** Eliminate fabricated occupational statistics by anchoring all career discovery and skill requirements directly in the **O*NET 28+ Occupational Taxonomy**.
- **Agentic AI Pipeline:** Deploy five specialized AI agents that collaborate through structured contracts to diagnose, discover, analyze, curate, and plan student careers.
- **Explainable Matching:** Utilize TF-IDF semantic vectorization, cosine similarity, and technology overlap ratios to provide explainable compatibility ratings.
- **Actionable Execution:** Divide long-term goals into 5 distinct phases (Foundation, Core Skills, Advanced Skills, Capstones, and Placement Prep) with monthly deliverables and checklist tracking.
- **Offline & Fallback Resilience:** Provide guaranteed zero-downtime operation through an autonomous deterministic O*NET reasoning engine when API keys are unconfigured.

---

## 🌟 Key Features

- **Professional Onboarding:** 10-field comprehensive student profile form supporting custom skill tagging and flexible learning durations (3, 6, 12, 18 months).
- **Agent Execution Monitor:** Real-time visual monitor showing all 5 agents transitioning between `PENDING`, `RUNNING`, and `COMPLETED` states with live message logs.
- **Career Discovery & Comparison:** Evaluates candidate profiles against O*NET occupations and provides side-by-side comparison matrices of salary, job zone, and core skills.
- **Multi-Dimensional Skill Gap Analysis:** Categorizes missing technical competencies by difficulty (Beginner, Intermediate, Advanced) and hiring priority (High, Medium, Low), visualized via Plotly radar and bar charts.
- **Curated Courseware Catalog:** Verified courses from Harvard CS50, DeepLearning.AI, Coursera, MIT OpenCourseWare, and official documentation.
- **Interactive Checklists & SQLite Persistence:** Real-time completion checkboxes that store progress across sessions in an embedded SQLite database.
- **Grounded AI Career Chat:** Context-aware interactive assistant maintaining conversation memory of student profiles, target roles, and skill gaps.
- **Downloadable PDF Dossier:** Single-click export of an executive-grade, multi-page career dossier formatted with ReportLab.

---

## 🏗️ System Architecture

```
                                  [ User / Student ]
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │ Streamlit Frontend  │
                               │  Custom CSS Theme   │
                               └──────────┬──────────┘
                                          │
                     ┌────────────────────┴────────────────────┐
                     ▼                                         ▼
         ┌────────────────────────┐                ┌───────────────────────┐
         │ Multi-Agent Pipeline   │                │ SQLite Database (DB)  │
         │ (CareerCompassOrch.)   │                │ Profiles, Roadmaps,   │
         └───────────┬────────────┘                │ Task Progress Tracking│
                     │                             └───────────────────────┘
  ┌──────────────────┼──────────────────┬──────────────────┐
  ▼                  ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Agent 1:    │   │  Agent 2:    │   │  Agent 3:    │   │  Agent 4:    │
│  Student     │──▶│  Career      │──▶│  Skill Gap   │──▶│  Learning    │──▶ [ Agent 5: Roadmap ]
│  Profiling   │   │  Discovery   │   │  Analysis    │   │  Recommender │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
  ▲                  ▲                  ▲                  ▲
  │                  │                  │                  │
  └──────────────────┴─────────┬────────┴──────────────────┘
                               ▼
        ┌──────────────────────────────────────────────┐
        │       Grounded Occupational Services         │
        ├──────────────────────┬───────────────────────┤
        │ ONetService (O*NET)  │ RecommendationService │
        │ TF-IDF + Cosine Sim  │ Verified Courses & DB │
        ├──────────────────────┴───────────────────────┤
        │ LLMProvider: Gemini API / OpenAI / Fallback  │
        └──────────────────────────────────────────────┘
```

---

## 🤖 Autonomous Multi-Agent Architecture

The core intelligence of CareerCompass is divided among five dedicated AI agents, communicating through structured dataclasses and JSON contracts:

| Agent | Name | Role & Core Responsibilities | Input | Output Contract |
|---|---|---|---|---|
| **Agent 1** | **Student Profiling Agent** | Analyzes academic level, degree, existing tools, and career preference; computes academic readiness score (0-100%). | Raw onboarding form dictionary | Structured profile with strengths, growth areas, and baseline readiness score. |
| **Agent 2** | **Career Discovery Agent** | Performs hybrid TF-IDF text matching and skill overlap against O*NET occupations; computes compatibility percentages (50-98%). | Student Profiling output | Top 5 ranked O*NET occupations with compatibility rationales. |
| **Agent 3** | **Skill Gap Analysis Agent** | Compares student skills with official O*NET Technology Skills and Soft Skills; categorizes gaps by difficulty and priority. | Student Profile + Target Career | Categorized missing technical and soft skills, gap intensity, and radar chart data. |
| **Agent 4** | **Learning Recommendation Agent** | Maps identified skill gaps to verified free/paid courseware, certifications, and official technical documentation. | Student Profile + Skill Gap output | Curated courses (Coursera, edX, MIT OCW) and industry certifications (AWS, Google, CNCF). |
| **Agent 5** | **Roadmap Planning Agent** | Synthesizes all prior outputs into a 5-phase month-by-month actionable timeline with measurable monthly deliverables. | Outputs of Agents 1, 2, 3, and 4 | 5-phase timeline with monthly action items, project deliverables, and milestones. |

---

## 📊 O*NET Dataset Integration & Grounding

CareerCompass integrates authentic records from the **O*NET 28+ Content Model** (U.S. Department of Labor):
- **O*NET-SOC Taxonomy:** Direct integration of Standard Occupational Classification codes (e.g. `15-1221.00`, `15-2051.00`, `15-1252.00`, `15-1299.08`, `15-1212.00`).
- **Content Model Elements:** Includes Job Zones (Levels 1 to 5), Median National Salaries, Core Cognitive Skills, Knowledge Areas, Abilities, Work Activities, and In-Demand Hot Technologies.
- **Hybrid Matching Algorithm:**
  $$\text{Score} = (0.40 \times \text{CosineSim}_{\text{TF-IDF}}) + (0.35 \times \text{Overlap}_{\text{Skills}}) + (0.25 \times \text{Alignment}_{\text{Interests}})$$
- **Explainability:** Transparent breakdown of exactly why a career was recommended and which existing skills match the role.

---

## 💻 Technology Stack

- **Frontend & UI:** Streamlit 1.35+, Custom CSS, Plotly Express & Graph Objects (Interactive Radar & Bar Charts).
- **Backend & Logic:** Python 3.11+, Pandas 2.1+, NumPy 1.26+, Scikit-learn 1.4+ (TF-IDF vectorizer, Cosine Similarity).
- **AI & LLM Providers:** Google Gemini API (`google-genai` / `google-generativeai`), OpenAI API (`gpt-4o-mini`), and Autonomous Deterministic Fallback Engine.
- **Database:** SQLite 3 with context-managed connections and foreign key referential integrity.
- **Reporting:** ReportLab 4.1+ for dynamic PDF vector generation.
- **Testing:** Pytest 8.0+ test harness with 100% passing unit and integration suites.

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
- Python 3.11 or higher installed on your machine.
- Git installed.

### 2. Clone or Navigate to the Repository
```bash
cd CareerCompass
```

### 3. Create and Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Copy the example environment file and add your API keys (optional):
```bash
cp .env.example .env
```
Inside `.env`:
```env
# Google Gemini API Key (Primary LLM)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Default LLM Provider ('gemini' or 'openai')
DEFAULT_LLM_PROVIDER=gemini
```
> **Note:** If no API key is provided, CareerCompass runs seamlessly in **Autonomous Grounded Fallback Mode**, ensuring all agents, matching engines, roadmaps, and PDF reports work without external dependencies.

---

## 🖥️ Running the Application

Launch the Streamlit web application with:
```bash
streamlit run app.py
```
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 🧪 Running the Test Suite

Execute the automated test suite with pytest:
```bash
pytest tests -v
```
All 13 tests verify:
1. Agent 1: Student profiling and readiness score generation.
2. Agent 2: O*NET occupational discovery and compatibility scoring.
3. Agent 3: Skill gap analysis and difficulty categorization.
4. Agent 4: Course recommendation and certification mapping.
5. Agent 5: 5-phase roadmap timeline synthesis.
6. Jaccard similarity and skill overlap calculations.
7. O*NET dataset loading and TF-IDF semantic query matching.
8. SQLite database persistence, retrieval, and task progress tracking.
9. ReportLab PDF compilation and byte-stream verification.
10. End-to-end multi-agent orchestration pipeline.

---

## 📑 Three Pre-Generated Sample Roadmaps

To facilitate evaluation without external API calls, three benchmark profiles were generated by the live pipeline and saved under `sample_roadmaps/`:

### Sample 1: AI/ML Engineer
- **Candidate:** Aarav Sharma (3rd Year CSE Undergraduate)
- **Skills:** Python, SQL, NumPy
- **Interests:** Artificial Intelligence, Machine Learning
- **Target Role:** Computer and Information Research Scientists (AI / ML Engineer) - O*NET `15-1221.00`
- **Compatibility:** 81.6% Match
- **File:** `sample_roadmaps/ai_ml_engineer.json`

### Sample 2: Data Scientist
- **Candidate:** Priya Patel (3rd Year CSE Undergraduate)
- **Skills:** Python, Excel, SQL
- **Interests:** Data Science, Business Analytics
- **Target Role:** Data Scientists - O*NET `15-2051.00`
- **Compatibility:** 83.2% Match
- **File:** `sample_roadmaps/data_scientist.json`

### Sample 3: Software & Cloud Developer
- **Candidate:** Rohan Iyer (4th Year CSE Undergraduate)
- **Skills:** Java, Python, HTML, CSS
- **Interests:** Software Development, Cloud Computing
- **Target Role:** Software Developers / Cloud Engineers - O*NET `15-1252.00`
- **Compatibility:** 84.7% Match
- **File:** `sample_roadmaps/software_cloud_engineer.json`

> **Quick Load in UI:** Use the sidebar dropdown **"Load Sample Profile"** to instantly test and explore any of these profiles!

---

## 📱 Page-by-Page Application Walkthrough

1. **Page 1: Landing Page (`pages/landing.py`)**
   - Hero header with project metadata (SIH25094, CSE473).
   - Multi-agent architecture overview and scientific feature breakdown.
   - Quick "Get Started" onboarding trigger.

2. **Page 2: Student Dashboard (`pages/dashboard.py`)**
   - Diagnostic card summarizing academic profile, readiness index, and target role.
   - Plotly interactive progress donut chart showing roadmap task completion percentage.
   - Database history of all previously saved roadmaps.

3. **Page 3: Career Discovery (`pages/career_discovery.py`)**
   - Top 5 ranked O*NET occupations with compatibility percentages.
   - Horizontal Plotly bar chart visualizing relative match strength.
   - Side-by-side comparison tool comparing salaries, job zones, and skills.
   - "Target This Role" button that dynamically re-aligns the roadmap.

4. **Page 4: Skill Gap Analysis (`pages/skill_gap.py`)**
   - Plotly Spider / Radar chart mapping candidate strengths against O*NET targets.
   - Categorized technical gaps broken down by Beginner, Intermediate, and Advanced.
   - Priority indicators (High, Medium, Low) and workplace soft-skill competencies.

5. **Page 5: Learning Roadmap (`pages/roadmap.py`)**
   - 5 sequential phases: Foundation, Core Skills, Advanced Skills, Capstones, and Placement Prep.
   - Interactive task checkboxes persisted in SQLite across browser reloads.
   - Monthly deliverable capstone project descriptions.
   - Verified course cards with direct links to Coursera, edX, MIT OCW, and industry certs.

6. **Page 6: AI Career Chat (`pages/chatbot.py`)**
   - Grounded conversational agent answering student questions about interview prep, capstone design, and certifications.
   - Maintains full conversation context from the student profile and O*NET benchmarks.

7. **Page 7: Report & PDF Export (`pages/report.py`)**
   - Executive dossier preview summarizing the candidate's diagnostic profile.
   - Single-click download button streaming a multi-page PDF generated via ReportLab.

---

## 🗄️ Database Schema & Persistence

CareerCompass utilizes an embedded SQLite database (`careercompass.db`) with three tables:

```sql
-- 1. Student Profiles Table
CREATE TABLE student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    education_level TEXT NOT NULL,
    degree_branch TEXT NOT NULL,
    current_year TEXT NOT NULL,
    technical_skills TEXT NOT NULL,
    interests TEXT NOT NULL,
    career_goal TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    learning_duration_months INTEGER NOT NULL,
    learning_preference TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- 2. Roadmaps Table
CREATE TABLE roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    career_code TEXT NOT NULL,
    career_title TEXT NOT NULL,
    compatibility_score REAL NOT NULL,
    roadmap_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES student_profiles(id)
);

-- 3. Task Progress Table
CREATE TABLE task_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roadmap_id INTEGER NOT NULL,
    phase_number INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    task_id TEXT NOT NULL,
    task_description TEXT NOT NULL,
    is_completed INTEGER DEFAULT 0,
    updated_at TEXT NOT NULL,
    UNIQUE(roadmap_id, task_id),
    FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id)
);
```

---

## 🔍 Limitations & Future Scope

### Current Limitations
1. **O*NET Taxonomy Scope:** The current integration focuses primarily on computing, data science, electronics, robotics, and cloud engineering occupations.
2. **Deterministic Fallback vs Dynamic LLM:** When API keys are absent, roadmap tasks follow pre-compiled O*NET benchmark trajectories rather than dynamically generating customized text for rare custom tools.

### Future Scope
1. **GitHub & LinkedIn Ingestion:** Direct OAuth synchronization to automatically parse existing repositories and course certificates.
2. **AI Mock Interview Simulator:** Voice-based interactive agent conducting STAR-method mock technical interviews.
3. **Live Job Board Matching:** Real-time web scraping of active entry-level job postings matching the student's closing skill gaps.

---

## 👥 Authors & Academic Attribution
- **Course:** CSE473 – Agentic AI
- **Project ID:** SIH25094
- **Occupational Data Source:** O*NET 28+ Database, sponsored by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA).
