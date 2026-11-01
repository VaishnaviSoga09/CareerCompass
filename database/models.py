"""
Database Models and Schemas for CareerCompass
SIH25094 - CSE473 Agentic AI
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

@dataclass
class StudentProfileModel:
    id: Optional[int] = None
    full_name: str = ""
    education_level: str = "Undergraduate"
    degree_branch: str = "CSE"
    current_year: str = "3rd Year"
    technical_skills: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    career_goal: str = ""
    experience_level: str = "Beginner"
    learning_duration_months: int = 6
    learning_preference: str = "Hands-on Projects"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "education_level": self.education_level,
            "degree_branch": self.degree_branch,
            "current_year": self.current_year,
            "technical_skills": self.technical_skills,
            "interests": self.interests,
            "career_goal": self.career_goal,
            "experience_level": self.experience_level,
            "learning_duration_months": self.learning_duration_months,
            "learning_preference": self.learning_preference,
            "created_at": self.created_at
        }

@dataclass
class RoadmapRecordModel:
    id: Optional[int] = None
    student_id: Optional[int] = None
    career_code: str = ""
    career_title: str = ""
    compatibility_score: float = 0.0
    roadmap_json: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class TaskProgressModel:
    id: Optional[int] = None
    roadmap_id: int = 0
    phase_number: int = 1
    month_number: int = 1
    task_id: str = ""
    task_description: str = ""
    is_completed: bool = False
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
