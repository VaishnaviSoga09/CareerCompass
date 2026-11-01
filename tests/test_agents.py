"""
Unit and Integration Tests for the 5 AI Agents
SIH25094 - CSE473 Agentic AI
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm import LLMProvider
from services.onet_service import ONetService
from services.recommendation_service import RecommendationService
from agents.student_agent import StudentProfilingAgent
from agents.career_agent import CareerDiscoveryAgent
from agents.skill_gap_agent import SkillGapAnalysisAgent
from agents.learning_agent import LearningRecommendationAgent
from agents.roadmap_agent import RoadmapPlanningAgent

@pytest.fixture
def test_setup():
    llm = LLMProvider()
    onet = ONetService()
    recommender = RecommendationService()
    return {
        "llm": llm,
        "onet": onet,
        "recommender": recommender
    }

def test_student_profiling_agent(test_setup):
    agent = StudentProfilingAgent(test_setup["llm"])
    raw_input = {
        "full_name": "Test Candidate",
        "education_level": "Undergraduate",
        "degree_branch": "CSE",
        "current_year": "3rd Year",
        "technical_skills": ["Python", "SQL"],
        "interests": ["Machine Learning"],
        "career_goal": "AI Engineer",
        "experience_level": "Beginner",
        "learning_duration_months": 6,
        "learning_preference": "Hands-on Projects"
    }
    result = agent.execute(raw_input)
    assert result["status"] == "COMPLETED"
    profile = result["student_profile"]
    assert profile["full_name"] == "Test Candidate"
    assert "identified_strengths" in profile
    assert profile["academic_readiness_score"] >= 60

def test_career_discovery_agent(test_setup):
    profiling_agent = StudentProfilingAgent(test_setup["llm"])
    career_agent = CareerDiscoveryAgent(test_setup["llm"], test_setup["onet"])
    
    prof_out = profiling_agent.execute({
        "full_name": "Cloud Learner",
        "education_level": "Undergraduate",
        "degree_branch": "IT",
        "current_year": "4th Year",
        "technical_skills": ["Linux", "Docker", "Python"],
        "interests": ["Cloud Computing"],
        "career_goal": "Cloud Architect",
        "experience_level": "Intermediate",
        "learning_duration_months": 6,
        "learning_preference": "Hands-on Projects"
    })

    career_out = career_agent.execute(prof_out)
    assert career_out["status"] == "COMPLETED"
    top_careers = career_out["top_careers"]
    assert len(top_careers) == 5
    assert career_out["primary_career"]["compatibility_score"] > 50

def test_skill_gap_agent(test_setup):
    gap_agent = SkillGapAnalysisAgent(test_setup["llm"])
    student_profile = {
        "technical_skills": ["Python", "SQL"],
        "experience_level": "Beginner"
    }
    selected_career = {
        "title": "Data Scientists",
        "onetsoc_code": "15-2051.00",
        "technology_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow"],
        "soft_skills": ["Data Storytelling", "Curiosity"]
    }
    res = gap_agent.execute(student_profile, selected_career)
    assert res["status"] == "COMPLETED"
    gap = res["skill_gap_analysis"]
    assert "Python" in gap["existing_matching_skills"]
    assert len(gap["missing_technical_skills"]) > 0

def test_learning_recommendation_agent(test_setup):
    learning_agent = LearningRecommendationAgent(test_setup["llm"], test_setup["recommender"])
    student_profile = {"learning_preference": "Hands-on Projects"}
    gap_data = {
        "skill_gap_analysis": {
            "target_career": "Data Scientist",
            "missing_technical_skills": [
                {"skill": "Scikit-learn", "priority": "High"},
                {"skill": "TensorFlow", "priority": "High"}
            ]
        }
    }
    res = learning_agent.execute(student_profile, gap_data)
    assert res["status"] == "COMPLETED"
    recs = res["learning_recommendations"]
    assert len(recs["recommended_courses"]) > 0

def test_roadmap_planning_agent(test_setup):
    roadmap_agent = RoadmapPlanningAgent(test_setup["llm"])
    student_profile = {
        "full_name": "Aarav",
        "degree_branch": "CSE",
        "learning_duration_months": 6
    }
    career_discovery = {
        "selected_career": {
            "canonical_name": "Artificial Intelligence & Machine Learning Engineer",
            "onetsoc_code": "15-1221.00"
        },
        "top_careers": []
    }
    skill_gap = {
        "existing_matching_skills": ["Python"],
        "missing_technical_skills": [{"skill": "PyTorch"}, {"skill": "Docker"}]
    }
    learning_recs = {"recommended_courses": [], "certifications": []}

    res = roadmap_agent.execute(student_profile, career_discovery, skill_gap, learning_recs)
    assert res["status"] == "COMPLETED"
    assert len(res["timeline"]) == 6
    assert len(res["phases_summary"]) == 5
    assert res["timeline"][0]["phase_number"] == 1
