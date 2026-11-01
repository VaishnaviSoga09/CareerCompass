"""
Agent 1: Student Profiling Agent
CareerCompass - SIH25094 - CSE473 Agentic AI

Responsibilities:
- Understand student education and academic background.
- Analyze interests, existing skills, experience, and career preferences.
- Identify strengths and areas for improvement.
- Convert student input into a structured student profile.
"""

from typing import Dict, Any, List
from core.llm import LLMProvider
from core.prompts import STUDENT_PROFILING_SYSTEM

class StudentProfilingAgent:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.name = "Student Profiling Agent"

    def execute(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes raw student input and creates an actionable structured profile.
        """
        full_name = raw_input.get("full_name", "Student")
        education_level = raw_input.get("education_level", "Undergraduate")
        degree_branch = raw_input.get("degree_branch", "CSE")
        current_year = raw_input.get("current_year", "3rd Year")
        technical_skills = raw_input.get("technical_skills", [])
        interests = raw_input.get("interests", [])
        career_goal = raw_input.get("career_goal", "")
        experience_level = raw_input.get("experience_level", "Beginner")
        learning_duration = raw_input.get("learning_duration_months", 6)
        learning_preference = raw_input.get("learning_preference", "Hands-on Projects")

        # Prompt LLM if available
        user_prompt = (
            f"Candidate: {full_name}\n"
            f"Education: {education_level} in {degree_branch} ({current_year})\n"
            f"Declared Technical Skills: {', '.join(technical_skills)}\n"
            f"Areas of Interest: {', '.join(interests)}\n"
            f"Career Goal: {career_goal}\n"
            f"Experience: {experience_level}\n"
            f"Target Learning Duration: {learning_duration} months\n"
            f"Learning Format Preference: {learning_preference}"
        )

        llm_output = self.llm.generate_json_response(STUDENT_PROFILING_SYSTEM, user_prompt)

        # Fallback / Deterministic Analysis
        if not llm_output:
            # Deterministic profiling logic grounded in academic parameters
            strengths = []
            improvements = []

            if len(technical_skills) >= 3:
                strengths.append(f"Demonstrated foundational toolkit with {len(technical_skills)} active technical skills")
            else:
                improvements.append("Expand core programming language and tool proficiency")

            if any(k.lower() in ["python", "java", "c++"] for k in technical_skills):
                strengths.append("Established proficiency in core computer science programming language")
            else:
                improvements.append("Formalize mastery of an industry-standard programming language (e.g. Python)")

            if interests:
                strengths.append(f"Clear domain interest in {', '.join(interests[:2])}")
            
            improvements.append("Industry-grade project portfolio and version-controlled repository development")
            improvements.append("Systematic interview preparation and system design fundamentals")

            summary = (
                f"{full_name} is a {current_year} {education_level} student specializing in {degree_branch} "
                f"with a career focus on {career_goal or 'technology roles'}. Current skill set includes "
                f"{', '.join(technical_skills[:4]) if technical_skills else 'entry-level exploration'}."
            )

            readiness = 70
            if experience_level == "Intermediate":
                readiness = 80
            elif experience_level == "Advanced":
                readiness = 90
            if len(technical_skills) > 4:
                readiness += 5

            llm_output = {
                "profile_summary": summary,
                "identified_strengths": strengths,
                "areas_for_improvement": improvements,
                "academic_readiness_score": min(readiness, 95),
                "recommended_pace": f"Targeting {learning_duration} months at ~12-15 hours/week"
            }

        return {
            "agent": self.name,
            "status": "COMPLETED",
            "student_profile": {
                **raw_input,
                "profile_summary": llm_output.get("profile_summary", ""),
                "identified_strengths": llm_output.get("identified_strengths", []),
                "areas_for_improvement": llm_output.get("areas_for_improvement", []),
                "academic_readiness_score": llm_output.get("academic_readiness_score", 75),
                "recommended_pace": llm_output.get("recommended_pace", "Standard")
            }
        }
