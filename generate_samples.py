"""
Script to Generate the 3 Required Sample Roadmaps
SIH25094 - CSE473 Agentic AI

Runs the exact CareerCompassOrchestrator pipeline on the 3 required student profiles:
1. AI/ML Engineer Candidate
2. Data Scientist Candidate
3. Software & Cloud Engineer Candidate

Outputs are saved in sample_roadmaps/ for instant zero-latency demonstration.
"""

import os
import json
from core.orchestrator import CareerCompassOrchestrator

def generate_all_samples():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(base_dir, "sample_roadmaps")
    os.makedirs(samples_dir, exist_ok=True)

    orchestrator = CareerCompassOrchestrator()

    # ----------------------------------------------------
    # SAMPLE 1: AI/ML Engineer
    # ----------------------------------------------------
    sample1_input = {
        "full_name": "Aarav Sharma",
        "education_level": "Undergraduate",
        "degree_branch": "CSE",
        "current_year": "3rd Year",
        "technical_skills": ["Python", "SQL", "NumPy"],
        "interests": ["Artificial Intelligence", "Machine Learning"],
        "career_goal": "AI/ML Engineer",
        "experience_level": "Beginner",
        "learning_duration_months": 6,
        "learning_preference": "Hands-on Projects"
    }
    print("[1/3] Generating Roadmap for Sample 1: AI/ML Engineer...")
    res1 = orchestrator.run_pipeline(sample1_input)
    path1 = os.path.join(samples_dir, "ai_ml_engineer.json")
    with open(path1, "w", encoding="utf-8") as f:
        json.dump(res1, f, indent=2)
    print(f"  -> Saved to {path1}")

    # ----------------------------------------------------
    # SAMPLE 2: Data Scientist
    # ----------------------------------------------------
    sample2_input = {
        "full_name": "Priya Patel",
        "education_level": "Undergraduate",
        "degree_branch": "CSE",
        "current_year": "3rd Year",
        "technical_skills": ["Python", "Excel", "SQL"],
        "interests": ["Data Science", "Business Analytics"],
        "career_goal": "Data Scientist",
        "experience_level": "Beginner",
        "learning_duration_months": 6,
        "learning_preference": "Interactive Learning"
    }
    print("[2/3] Generating Roadmap for Sample 2: Data Scientist...")
    res2 = orchestrator.run_pipeline(sample2_input)
    path2 = os.path.join(samples_dir, "data_scientist.json")
    with open(path2, "w", encoding="utf-8") as f:
        json.dump(res2, f, indent=2)
    print(f"  -> Saved to {path2}")

    # ----------------------------------------------------
    # SAMPLE 3: Software / Cloud Developer
    # ----------------------------------------------------
    sample3_input = {
        "full_name": "Rohan Iyer",
        "education_level": "Undergraduate",
        "degree_branch": "CSE",
        "current_year": "4th Year",
        "technical_skills": ["Java", "Python", "HTML", "CSS"],
        "interests": ["Software Development", "Cloud Computing"],
        "career_goal": "Software Engineer / Cloud Developer",
        "experience_level": "Intermediate",
        "learning_duration_months": 6,
        "learning_preference": "Hands-on Projects"
    }
    print("[3/3] Generating Roadmap for Sample 3: Software / Cloud Engineer...")
    res3 = orchestrator.run_pipeline(sample3_input)
    path3 = os.path.join(samples_dir, "software_cloud_engineer.json")
    with open(path3, "w", encoding="utf-8") as f:
        json.dump(res3, f, indent=2)
    print(f"  -> Saved to {path3}")

    print("\n[SUCCESS] All 3 sample roadmaps successfully produced by the live multi-agent pipeline!")

if __name__ == "__main__":
    generate_all_samples()
