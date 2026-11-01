"""
O*NET Occupational Database Service for CareerCompass
SIH25094 - CSE473 Agentic AI

Integrates official O*NET-SOC 2019/2020 taxonomy, computes TF-IDF + cosine similarity,
and extracts occupational skills, knowledge, abilities, and technology requirements.
"""

import os
import json
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ONetService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ONetService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, data_path: Optional[str] = None):
        if getattr(self, "_initialized", False):
            return
            
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = data_path or os.path.join(base_dir, "data", "processed", "onet_occupations.json")
        self.occupations: List[Dict[str, Any]] = []
        self.code_to_occupation: Dict[str, Dict[str, Any]] = {}
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = None
        self._load_dataset()
        self._initialized = True

    def _load_dataset(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(
                f"O*NET dataset not found at {self.data_path}. "
                "Please run data/preprocess_onet.py to generate dataset files."
            )
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.occupations = json.load(f)
            
        self.code_to_occupation = {occ["onetsoc_code"]: occ for occ in self.occupations}
        
        # Build search corpus for TF-IDF
        corpus = []
        for occ in self.occupations:
            search_str = (
                f"{occ.get('title', '')} "
                f"{occ.get('canonical_name', '')} "
                f"{occ.get('description', '')} "
                f"{' '.join(occ.get('technology_skills', []))} "
                f"{' '.join(occ.get('skills', []))} "
                f"{' '.join(occ.get('knowledge', []))} "
                f"{' '.join(occ.get('sample_job_titles', []))}"
            )
            corpus.append(search_str)
            
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def get_all_occupations(self) -> List[Dict[str, Any]]:
        return self.occupations

    def get_occupation_by_code(self, onetsoc_code: str) -> Optional[Dict[str, Any]]:
        return self.code_to_occupation.get(onetsoc_code)

    def find_top_matching_occupations(
        self, 
        student_text: str, 
        user_skills: List[str], 
        user_interests: List[str], 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculates hybrid compatibility:
        1. TF-IDF Semantic similarity over O*NET occupational corpus
        2. Direct Skill overlap with O*NET Technology Skills & Core Skills
        3. Interest alignment
        """
        # 1. Text Similarity (TF-IDF Cosine)
        query_vec = self.vectorizer.transform([student_text])
        cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        user_skills_lower = {s.strip().lower() for s in user_skills if s.strip()}
        user_interests_lower = {i.strip().lower() for i in user_interests if i.strip()}
        
        scored_results = []
        for idx, occ in enumerate(self.occupations):
            text_score = float(cosine_sims[idx])
            
            # 2. Skill Overlap Score
            tech_skills = {s.lower() for s in occ.get("technology_skills", [])}
            matched_tech = [s for s in user_skills if s.lower() in tech_skills]
            skill_score = len(matched_tech) / max(len(tech_skills), 1)
            
            # 3. Interest Overlap
            occ_desc_lower = (
                occ["title"].lower() + " " + 
                occ["canonical_name"].lower() + " " + 
                occ["description"].lower()
            )
            matched_interests = [
                i for i in user_interests 
                if i.lower() in occ_desc_lower or any(i.lower() in t for t in tech_skills)
            ]
            interest_score = min(len(matched_interests) / max(len(user_interests_lower), 1), 1.0)
            
            # Weighted Hybrid Score (0 to 100%)
            # Text similarity: 40%, Skill match: 35%, Interest match: 25%
            hybrid_score = (text_score * 0.40) + (skill_score * 0.35) + (interest_score * 0.25)
            
            # Normalize to 50% - 98% range for realistic human perception
            compatibility_pct = round(min(max(hybrid_score * 100 + 40, 48.0), 98.5), 1)
            
            scored_results.append({
                "onetsoc_code": occ["onetsoc_code"],
                "title": occ["title"],
                "canonical_name": occ["canonical_name"],
                "description": occ["description"],
                "job_zone": occ["job_zone"],
                "median_salary_usd": occ.get("median_salary_usd", 100000),
                "compatibility_score": compatibility_pct,
                "matched_skills": matched_tech,
                "matched_interests": matched_interests,
                "technology_skills": occ.get("technology_skills", []),
                "soft_skills": occ.get("soft_skills", []),
                "skills": occ.get("skills", []),
                "knowledge": occ.get("knowledge", []),
                "abilities": occ.get("abilities", []),
                "work_activities": occ.get("work_activities", []),
                "related_occupations": occ.get("related_occupations", [])
            })
            
        # Sort by compatibility descending
        scored_results.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return scored_results[:top_k]
