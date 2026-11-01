"""
Multi-Agent Orchestrator for CareerCompass
SIH25094 - CSE473 Agentic AI

Coordinates the 5 specialized AI agents:
1. Student Profiling Agent
2. Career Discovery Agent
3. Skill Gap Analysis Agent
4. Learning Recommendation Agent
5. Roadmap Planning Agent

Provides real-time event hooks for UI agent execution visualization.
"""

from typing import Dict, Any, Callable, Optional, List
import time

from core.llm import LLMProvider
from services.onet_service import ONetService
from services.recommendation_service import RecommendationService
from agents.student_agent import StudentProfilingAgent
from agents.career_agent import CareerDiscoveryAgent
from agents.skill_gap_agent import SkillGapAnalysisAgent
from agents.learning_agent import LearningRecommendationAgent
from agents.roadmap_agent import RoadmapPlanningAgent
from database.db import DatabaseManager
from database.models import StudentProfileModel, RoadmapRecordModel

class CareerCompassOrchestrator:
    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        onet_service: Optional[ONetService] = None,
        recommendation_service: Optional[RecommendationService] = None,
        db_manager: Optional[DatabaseManager] = None
    ):
        self.llm = llm_provider or LLMProvider()
        self.onet = onet_service or ONetService()
        self.recommender = recommendation_service or RecommendationService()
        self.db = db_manager or DatabaseManager()

        # Instantiate 5 specialized agents
        self.agent_profiling = StudentProfilingAgent(self.llm)
        self.agent_career = CareerDiscoveryAgent(self.llm, self.onet)
        self.agent_skill_gap = SkillGapAnalysisAgent(self.llm)
        self.agent_learning = LearningRecommendationAgent(self.llm, self.recommender)
        self.agent_roadmap = RoadmapPlanningAgent(self.llm)

    def run_pipeline(
        self,
        raw_student_input: Dict[str, Any],
        selected_career_override: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[str, str, str, Any], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes the 5-agent sequential pipeline.
        progress_callback(agent_name, status, message, partial_data)
        """
        agent_names = [
            "Student Profiling Agent",
            "Career Discovery Agent",
            "Skill Gap Analysis Agent",
            "Learning Recommendation Agent",
            "Roadmap Planning Agent"
        ]

        def notify(agent_name: str, status: str, message: str, data: Any = None):
            if progress_callback:
                progress_callback(agent_name, status, message, data)

        # Notify initial pending state
        for name in agent_names:
            notify(name, "PENDING", "Waiting in execution queue...")

        # ----------------------------------------------------
        # AGENT 1: Student Profiling Agent
        # ----------------------------------------------------
        notify("Student Profiling Agent", "RUNNING", "Analyzing academic background, skills, and goals...")
        profile_res = self.agent_profiling.execute(raw_student_input)
        student_profile = profile_res["student_profile"]
        notify(
            "Student Profiling Agent", 
            "COMPLETED", 
            f"Readiness Score: {student_profile.get('academic_readiness_score')}% • "
            f"Strengths identified: {len(student_profile.get('identified_strengths', []))}", 
            student_profile
        )

        # ----------------------------------------------------
        # AGENT 2: Career Discovery Agent
        # ----------------------------------------------------
        notify("Career Discovery Agent", "RUNNING", "Querying O*NET 28+ occupational database and calculating compatibility...")
        career_res = self.agent_career.execute(profile_res)
        top_careers = career_res["top_careers"]
        best_career = selected_career_override or career_res["primary_career"]
        career_res["selected_career"] = best_career
        notify(
            "Career Discovery Agent", 
            "COMPLETED", 
            f"Matched top 5 O*NET occupations. Leading match: {best_career.get('canonical_name')} "
            f"({best_career.get('compatibility_score')}%)", 
            career_res
        )

        # ----------------------------------------------------
        # AGENT 3: Skill Gap Analysis Agent
        # ----------------------------------------------------
        notify("Skill Gap Analysis Agent", "RUNNING", f"Benchmarking skills against {best_career.get('canonical_name')} requirements...")
        skill_gap_res = self.agent_skill_gap.execute(student_profile, best_career)
        gap_analysis = skill_gap_res["skill_gap_analysis"]
        notify(
            "Skill Gap Analysis Agent", 
            "COMPLETED", 
            f"Existing skills: {gap_analysis.get('total_skills_matched')}, "
            f"Missing technical skills: {len(gap_analysis.get('missing_technical_skills', []))} (Gap: {gap_analysis.get('gap_percentage')}%)", 
            gap_analysis
        )

        # ----------------------------------------------------
        # AGENT 4: Learning Recommendation Agent
        # ----------------------------------------------------
        notify("Learning Recommendation Agent", "RUNNING", "Querying course catalog for verified courses & certifications...")
        learning_res = self.agent_learning.execute(student_profile, skill_gap_res)
        recs = learning_res["learning_recommendations"]
        notify(
            "Learning Recommendation Agent", 
            "COMPLETED", 
            f"Recommended {len(recs.get('recommended_courses', []))} verified courses and "
            f"{len(recs.get('certifications', []))} professional certifications.", 
            recs
        )

        # ----------------------------------------------------
        # AGENT 5: Roadmap Planning Agent
        # ----------------------------------------------------
        notify("Roadmap Planning Agent", "RUNNING", "Synthesizing 5-phase month-by-month actionable roadmap...")
        final_roadmap = self.agent_roadmap.execute(
            student_profile=student_profile,
            career_discovery=career_res,
            skill_gap=gap_analysis,
            learning_recs=recs
        )
        timeline = final_roadmap.get("timeline", [])
        notify(
            "Roadmap Planning Agent", 
            "COMPLETED", 
            f"Generated {len(timeline)}-month comprehensive learning & career roadmap with milestones.", 
            final_roadmap
        )

        # Persist to SQLite Database
        try:
            profile_model = StudentProfileModel(
                full_name=student_profile.get("full_name", ""),
                education_level=student_profile.get("education_level", "Undergraduate"),
                degree_branch=student_profile.get("degree_branch", "CSE"),
                current_year=student_profile.get("current_year", "3rd Year"),
                technical_skills=student_profile.get("technical_skills", []),
                interests=student_profile.get("interests", []),
                career_goal=student_profile.get("career_goal", ""),
                experience_level=student_profile.get("experience_level", "Beginner"),
                learning_duration_months=int(student_profile.get("learning_duration_months", 6)),
                learning_preference=student_profile.get("learning_preference", "Hands-on Projects")
            )
            student_id = self.db.save_student_profile(profile_model)

            roadmap_record = RoadmapRecordModel(
                student_id=student_id,
                career_code=best_career.get("onetsoc_code", "N/A"),
                career_title=best_career.get("canonical_name", "Target Career"),
                compatibility_score=best_career.get("compatibility_score", 0.0),
                roadmap_json=final_roadmap
            )
            roadmap_id = self.db.save_roadmap(roadmap_record)
            final_roadmap["saved_db_id"] = roadmap_id
            final_roadmap["student_id"] = student_id
        except Exception as e:
            final_roadmap["db_error"] = str(e)

        return final_roadmap
