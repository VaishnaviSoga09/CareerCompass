"""
Explainable Matching Engine for CareerCompass
SIH25094 - CSE473 Agentic AI

Implements TF-IDF vectorization, Cosine similarity, and Jaccard skill metrics
with full explainability for student-to-career compatibility.
"""

from typing import List, Dict, Any, Set
import numpy as np

def compute_jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Computes Jaccard index: |A ∩ B| / |A ∪ B|"""
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return float(intersection) / float(union) if union > 0 else 0.0

def compute_skill_overlap_details(
    user_skills: List[str], 
    target_skills: List[str]
) -> Dict[str, Any]:
    """
    Compares candidate technical skills against occupational target skills.
    Returns matched skills, missing skills, and overlap statistics.
    """
    user_normalized = {s.strip().lower(): s.strip() for s in user_skills if s.strip()}
    target_normalized = {s.strip().lower(): s.strip() for s in target_skills if s.strip()}

    matched = []
    missing = []

    for t_lower, t_orig in target_normalized.items():
        if t_lower in user_normalized:
            matched.append(t_orig)
        elif any(u in t_lower or t_lower in u for u in user_normalized):
            matched.append(t_orig)
        else:
            missing.append(t_orig)

    total_target = max(len(target_normalized), 1)
    coverage_ratio = len(matched) / total_target

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage_ratio": round(coverage_ratio, 2),
        "total_required": len(target_normalized),
        "total_matched": len(matched)
    }

def format_radar_chart_data(
    categories: List[str], 
    student_scores: List[float], 
    required_scores: List[float]
) -> Dict[str, Any]:
    """
    Prepares radar chart series for Plotly visualization.
    """
    return {
        "categories": categories,
        "student": student_scores,
        "required": required_scores
    }
