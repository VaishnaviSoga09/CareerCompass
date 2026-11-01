"""
Unit and Integration Tests for Matching & O*NET Service
SIH25094 - CSE473 Agentic AI
"""

import pytest
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.matching import compute_jaccard_similarity, compute_skill_overlap_details
from services.onet_service import ONetService

def test_jaccard_similarity():
    set_a = {"python", "sql", "git"}
    set_b = {"python", "docker", "git"}
    sim = compute_jaccard_similarity(set_a, set_b)
    assert 0.49 < sim < 0.51  # 2/4 = 0.5

def test_jaccard_empty():
    assert compute_jaccard_similarity(set(), {"python"}) == 0.0

def test_skill_overlap_details():
    user_skills = ["Python", "SQL", "Pandas"]
    target_skills = ["Python", "Docker", "Kubernetes", "SQL"]
    overlap = compute_skill_overlap_details(user_skills, target_skills)

    assert "Python" in overlap["matched_skills"]
    assert "SQL" in overlap["matched_skills"]
    assert "Docker" in overlap["missing_skills"]
    assert overlap["total_matched"] == 2
    assert overlap["total_required"] == 4
    assert overlap["coverage_ratio"] == 0.5

def test_onet_service_loading():
    service = ONetService()
    occupations = service.get_all_occupations()
    assert len(occupations) >= 10
    
    # Check for core occupations
    codes = [o["onetsoc_code"] for o in occupations]
    assert "15-2051.00" in codes  # Data Scientists
    assert "15-1252.00" in codes  # Software Developers

def test_onet_matching_query():
    service = ONetService()
    top_matches = service.find_top_matching_occupations(
        student_text="machine learning deep learning python neural networks",
        user_skills=["Python", "NumPy", "TensorFlow"],
        user_interests=["Artificial Intelligence", "Machine Learning"],
        top_k=3
    )

    assert len(top_matches) == 3
    top_titles = [m["canonical_name"].lower() for m in top_matches]
    assert any("artificial intelligence" in t or "machine learning" in t or "data scientist" in t for t in top_titles)
    assert top_matches[0]["compatibility_score"] > 60.0
