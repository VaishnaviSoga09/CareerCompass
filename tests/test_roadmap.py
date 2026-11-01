"""
End-to-End Pipeline, Database, and PDF Generation Tests
SIH25094 - CSE473 Agentic AI
"""

import pytest
import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.orchestrator import CareerCompassOrchestrator
from database.db import DatabaseManager
from database.models import StudentProfileModel, RoadmapRecordModel
from services.pdf_service import PDFReportGenerator

def test_sqlite_database_lifecycle():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db_path = f.name

    try:
        db = DatabaseManager(db_path=temp_db_path)
        
        # Test student profile insertion
        prof = StudentProfileModel(
            full_name="Database Test User",
            education_level="Undergraduate",
            degree_branch="CSE",
            current_year="2nd Year",
            technical_skills=["Python", "C++"],
            interests=["AI"],
            career_goal="ML Engineer",
            experience_level="Beginner",
            learning_duration_months=6,
            learning_preference="Projects"
        )
        student_id = db.save_student_profile(prof)
        assert student_id > 0

        latest = db.get_latest_student_profile()
        assert latest is not None
        assert latest.full_name == "Database Test User"
        assert "Python" in latest.technical_skills

        # Test roadmap record insertion
        roadmap_rec = RoadmapRecordModel(
            student_id=student_id,
            career_code="15-1221.00",
            career_title="AI Engineer",
            compatibility_score=88.5,
            roadmap_json={
                "timeline": [
                    {
                        "month": 1,
                        "phase_number": 1,
                        "action_items": ["Learn NumPy", "Practice Linear Algebra"],
                        "milestones": ["Milestone 1"]
                    }
                ]
            }
        )
        r_id = db.save_roadmap(roadmap_rec)
        assert r_id > 0

        # Verify task progress initialization
        tasks = db.get_task_progress(r_id)
        assert len(tasks) == 3
        assert tasks[0]["is_completed"] == 0

        # Update task progress
        db.update_task_progress(r_id, tasks[0]["task_id"], True)
        updated_tasks = db.get_task_progress(r_id)
        assert updated_tasks[0]["is_completed"] == 1

    finally:
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

def test_pdf_report_generation():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_path = os.path.join(base_dir, "sample_roadmaps", "ai_ml_engineer.json")
    
    with open(sample_path, "r", encoding="utf-8") as f:
        roadmap_data = json.load(f)

    pdf_gen = PDFReportGenerator()
    pdf_bytes = pdf_gen.generate_report(roadmap_data)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000  # Valid multi-page PDF output
    assert pdf_bytes.startswith(b"%PDF")  # PDF magic number header

def test_full_pipeline_orchestration():
    orchestrator = CareerCompassOrchestrator()
    student_input = {
        "full_name": "Integration Test Student",
        "education_level": "Undergraduate",
        "degree_branch": "CSE",
        "current_year": "3rd Year",
        "technical_skills": ["Python", "SQL", "Pandas"],
        "interests": ["Data Science", "Machine Learning"],
        "career_goal": "Data Scientist",
        "experience_level": "Beginner",
        "learning_duration_months": 6,
        "learning_preference": "Hands-on Projects"
    }

    execution_events = []
    def callback(agent_name, status, msg, data):
        execution_events.append((agent_name, status))

    res = orchestrator.run_pipeline(student_input, progress_callback=callback)

    assert res["status"] == "COMPLETED"
    assert "student_profile" in res
    assert "selected_career" in res
    assert "skill_gap_analysis" in res
    assert "learning_recommendations" in res
    assert len(res["timeline"]) == 6
    assert len(execution_events) >= 10  # Pending, Running, Completed for all 5 agents
