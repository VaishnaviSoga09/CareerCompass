"""
Agent 3: Skill Gap Analysis Agent
CareerCompass - SIH25094 - CSE473 Agentic AI

Responsibilities:
- Compare the student's existing skills with the skills required for the selected occupation.
- Identify missing technical and soft skills.
- Categorize skills as Beginner, Intermediate, or Advanced.
- Prioritize skills according to career relevance.
"""

from typing import Dict, Any, List
from core.llm import LLMProvider
from core.prompts import SKILL_GAP_SYSTEM
from core.matching import compute_skill_overlap_details

class SkillGapAnalysisAgent:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.name = "Skill Gap Analysis Agent"

    def execute(
        self, 
        student_profile: Dict[str, Any], 
        selected_career: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Performs thorough skill gap comparison between candidate skills and target career requirements.
        """
        user_skills = student_profile.get("technical_skills", [])
        career_tech_skills = selected_career.get("technology_skills", [])
        career_soft_skills = selected_career.get("soft_skills", [])
        career_title = selected_career.get("title", "Target Career")

        # 1. Compute deterministic baseline overlap
        overlap_stats = compute_skill_overlap_details(user_skills, career_tech_skills)
        matched_skills = overlap_stats["matched_skills"]
        missing_tech_raw = overlap_stats["missing_skills"]

        # 2. Query LLM for semantic categorization and prioritization
        prompt = (
            f"Target Career: {career_title}\n"
            f"Candidate Skills: {', '.join(user_skills)}\n"
            f"Required O*NET Tech Skills: {', '.join(career_tech_skills)}\n"
            f"Target Soft Skills: {', '.join(career_soft_skills)}\n"
            f"Raw Missing Skills: {', '.join(missing_tech_raw)}\n"
            "Categorize each missing skill by level (Beginner/Intermediate/Advanced) and priority (High/Medium/Low)."
        )

        llm_response = self.llm.generate_json_response(SKILL_GAP_SYSTEM, prompt)

        # 3. Fallback / Deterministic categorization
        if not llm_response or "missing_technical_skills" not in llm_response:
            categorized_tech = []
            for idx, skill in enumerate(missing_tech_raw):
                # Heuristic categorization based on tool nature
                s_lower = skill.lower()
                if any(x in s_lower for x in ["git", "sql", "linux", "html", "css", "python basics"]):
                    lvl = "Beginner"
                elif any(x in s_lower for x in ["docker", "react", "pandas", "rest", "ci/cd", "selenium"]):
                    lvl = "Intermediate"
                else:
                    lvl = "Advanced"

                prio = "High" if idx < 3 else ("Medium" if idx < 7 else "Low")
                categorized_tech.append({
                    "skill": skill,
                    "level": lvl,
                    "priority": prio,
                    "relevance": f"Key component for {career_title} industry competence."
                })

            categorized_soft = []
            for s in career_soft_skills:
                categorized_soft.append({
                    "skill": s,
                    "priority": "High" if s == career_soft_skills[0] else "Medium",
                    "relevance": f"Essential workplace dynamic for {career_title} teams."
                })

            llm_response = {
                "missing_technical_skills": categorized_tech,
                "missing_soft_skills": categorized_soft,
                "existing_matching_skills": matched_skills,
                "overall_gap_level": "Moderate" if len(matched_skills) >= 2 else "Significant"
            }

        # Compute skill gap coverage metrics for visualization
        total_req = len(career_tech_skills) if career_tech_skills else 1
        matched_count = len(matched_skills)
        gap_percentage = round((len(llm_response.get("missing_technical_skills", [])) / total_req) * 100, 1)

        return {
            "agent": self.name,
            "status": "COMPLETED",
            "skill_gap_analysis": {
                "target_career": career_title,
                "onetsoc_code": selected_career.get("onetsoc_code", ""),
                "existing_matching_skills": matched_skills,
                "missing_technical_skills": llm_response.get("missing_technical_skills", []),
                "missing_soft_skills": llm_response.get("missing_soft_skills", []),
                "overall_gap_level": llm_response.get("overall_gap_level", "Moderate"),
                "total_skills_required": total_req,
                "total_skills_matched": matched_count,
                "gap_percentage": gap_percentage
            }
        }
