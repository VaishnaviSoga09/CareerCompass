"""
Agent 2: Career Discovery Agent
CareerCompass - SIH25094 - CSE473 Agentic AI

Responsibilities:
- Identify suitable career options.
- Match student interests and skills with relevant O*NET occupations.
- Retrieve occupational descriptions, skills, knowledge areas, and job information.
- Calculate career compatibility scores.
- Recommend the top five relevant career paths.
"""

from typing import Dict, Any, List
from services.onet_service import ONetService
from core.llm import LLMProvider
from core.prompts import CAREER_DISCOVERY_SYSTEM

class CareerDiscoveryAgent:
    def __init__(self, llm_provider: LLMProvider, onet_service: ONetService):
        self.llm = llm_provider
        self.onet = onet_service
        self.name = "Career Discovery Agent"

    def execute(self, student_profile_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives structured student profile and matches against O*NET occupational database.
        """
        profile = student_profile_output.get("student_profile", {})
        skills = profile.get("technical_skills", [])
        interests = profile.get("interests", [])
        goal = profile.get("career_goal", "")
        summary = profile.get("profile_summary", "")

        query_text = f"{goal} {' '.join(interests)} {' '.join(skills)} {summary}"

        # Retrieve top 5 matching O*NET occupations
        top_occupations = self.onet.find_top_matching_occupations(
            student_text=query_text,
            user_skills=skills,
            user_interests=interests,
            top_k=5
        )

        # Synthesize rationales using LLM or deterministic fallback
        occ_titles = [f"{o['title']} ({o['onetsoc_code']})" for o in top_occupations]
        prompt = (
            f"Student Goal: {goal}\n"
            f"Skills: {', '.join(skills)}\n"
            f"Interests: {', '.join(interests)}\n"
            f"Top Matches: {', '.join(occ_titles)}\n"
            "Provide rationales for why each occupation matches this candidate."
        )

        llm_response = self.llm.generate_json_response(CAREER_DISCOVERY_SYSTEM, prompt)
        rationales = llm_response.get("career_rationales", {}) if llm_response else {}
        primary_reason = llm_response.get("primary_recommendation_reason", "") if llm_response else ""

        # Enrich occupations with explainable rationale
        enriched_occupations = []
        for idx, occ in enumerate(top_occupations):
            code = occ["onetsoc_code"]
            custom_rationale = (
                rationales.get(code) or 
                rationales.get(occ["title"]) or 
                (
                    f"Strong alignment between your interest in {', '.join(interests[:2])} and "
                    f"O*NET benchmark tasks for {occ['canonical_name']}."
                )
            )
            enriched_occupations.append({
                **occ,
                "why_matched": custom_rationale,
                "rank": idx + 1
            })

        if not primary_reason and enriched_occupations:
            best = enriched_occupations[0]
            primary_reason = (
                f"{best['canonical_name']} is your highest match ({best['compatibility_score']}%) "
                f"based on your technical background and career objectives."
            )

        return {
            "agent": self.name,
            "status": "COMPLETED",
            "top_careers": enriched_occupations,
            "primary_career": enriched_occupations[0] if enriched_occupations else {},
            "discovery_summary": primary_reason
        }
