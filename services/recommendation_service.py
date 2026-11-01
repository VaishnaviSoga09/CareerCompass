"""
Course and Learning Resource Recommendation Service
SIH25094 - CSE473 Agentic AI
"""

import os
import json
from typing import List, Dict, Any, Optional

class RecommendationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecommendationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, catalog_path: Optional[str] = None):
        if getattr(self, "_initialized", False):
            return
            
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.catalog_path = catalog_path or os.path.join(base_dir, "data", "processed", "courses_catalog.json")
        self.courses: List[Dict[str, Any]] = []
        self._load_catalog()
        self._initialized = True

    def _load_catalog(self):
        if os.path.exists(self.catalog_path):
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                self.courses = json.load(f)
        else:
            self.courses = []

    def get_recommendations_for_skills(
        self, 
        missing_skills: List[str], 
        preferred_format: str = "Hands-on Projects",
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Ranks verified courses matching the missing skills and format preferences.
        """
        missing_skills_lower = [s.strip().lower() for s in missing_skills if s.strip()]
        scored_courses = []

        for course in self.courses:
            course_skills = [cs.lower() for cs in course.get("skills", [])]
            
            # Count overlapping skills
            overlap = 0
            for ms in missing_skills_lower:
                if any(ms in cs or cs in ms for cs in course_skills):
                    overlap += 1
                    
            if overlap > 0:
                # Preference boost
                pref_boost = 0.0
                desc = course.get("description", "").lower()
                c_type = course.get("type", "").lower()
                
                if "project" in preferred_format.lower() and ("project" in desc or "hands-on" in desc):
                    pref_boost += 0.5
                elif "video" in preferred_format.lower() and ("video" in c_type or "coursera" in course.get("provider", "").lower()):
                    pref_boost += 0.5
                elif "documentation" in preferred_format.lower() and "documentation" in c_type:
                    pref_boost += 0.5

                score = overlap + pref_boost + (course.get("rating", 4.5) * 0.1)
                scored_courses.append({
                    **course,
                    "relevance_score": round(score, 2),
                    "matched_missing_skills": [
                        ms for ms in missing_skills 
                        if any(ms.lower() in cs for cs in course_skills)
                    ]
                })

        scored_courses.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_courses[:limit]
