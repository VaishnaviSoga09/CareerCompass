"""
SQLite Database Operations for CareerCompass
SIH25094 - CSE473 Agentic AI
"""

import sqlite3
import json
import os
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from database.models import StudentProfileModel, RoadmapRecordModel, TaskProgressModel

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "careercompass.db")

class DatabaseManager:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._connection() as conn:
            cursor = conn.cursor()
            
            # 1. Student Profiles Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    education_level TEXT NOT NULL,
                    degree_branch TEXT NOT NULL,
                    current_year TEXT NOT NULL,
                    technical_skills TEXT NOT NULL,
                    interests TEXT NOT NULL,
                    career_goal TEXT NOT NULL,
                    experience_level TEXT NOT NULL,
                    learning_duration_months INTEGER NOT NULL,
                    learning_preference TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # 2. Roadmaps Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS roadmaps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    career_code TEXT NOT NULL,
                    career_title TEXT NOT NULL,
                    compatibility_score REAL NOT NULL,
                    roadmap_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES student_profiles(id)
                )
            """)

            # 3. Task Progress Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roadmap_id INTEGER NOT NULL,
                    phase_number INTEGER NOT NULL,
                    month_number INTEGER NOT NULL,
                    task_id TEXT NOT NULL,
                    task_description TEXT NOT NULL,
                    is_completed INTEGER DEFAULT 0,
                    updated_at TEXT NOT NULL,
                    UNIQUE(roadmap_id, task_id),
                    FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id)
                )
            """)
            conn.commit()

    def save_student_profile(self, profile: StudentProfileModel) -> int:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_profiles (
                    full_name, education_level, degree_branch, current_year,
                    technical_skills, interests, career_goal, experience_level,
                    learning_duration_months, learning_preference, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.full_name,
                profile.education_level,
                profile.degree_branch,
                profile.current_year,
                json.dumps(profile.technical_skills),
                json.dumps(profile.interests),
                profile.career_goal,
                profile.experience_level,
                profile.learning_duration_months,
                profile.learning_preference,
                profile.created_at
            ))
            conn.commit()
            return cursor.lastrowid

    def get_latest_student_profile(self) -> Optional[StudentProfileModel]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_profiles ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if not row:
                return None
            return StudentProfileModel(
                id=row["id"],
                full_name=row["full_name"],
                education_level=row["education_level"],
                degree_branch=row["degree_branch"],
                current_year=row["current_year"],
                technical_skills=json.loads(row["technical_skills"]),
                interests=json.loads(row["interests"]),
                career_goal=row["career_goal"],
                experience_level=row["experience_level"],
                learning_duration_months=row["learning_duration_months"],
                learning_preference=row["learning_preference"],
                created_at=row["created_at"]
            )

    def save_roadmap(self, roadmap_record: RoadmapRecordModel) -> int:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO roadmaps (
                    student_id, career_code, career_title,
                    compatibility_score, roadmap_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                roadmap_record.student_id,
                roadmap_record.career_code,
                roadmap_record.career_title,
                roadmap_record.compatibility_score,
                json.dumps(roadmap_record.roadmap_json),
                roadmap_record.created_at
            ))
            conn.commit()
            roadmap_id = cursor.lastrowid

            # Initialize tasks for progress tracking
            timeline = roadmap_record.roadmap_json.get("timeline", [])
            for month_data in timeline:
                m_num = month_data.get("month", 1)
                phase_num = month_data.get("phase_number", 1)
                milestones = month_data.get("action_items", []) + month_data.get("milestones", [])
                for idx, task_desc in enumerate(milestones):
                    task_id = f"m{m_num}_task{idx+1}"
                    cursor.execute("""
                        INSERT OR IGNORE INTO task_progress (
                            roadmap_id, phase_number, month_number, task_id, task_description, is_completed, updated_at
                        ) VALUES (?, ?, ?, ?, ?, 0, ?)
                    """, (roadmap_id, phase_num, m_num, task_id, task_desc, roadmap_record.created_at))
            conn.commit()
            return roadmap_id

    def get_roadmap_by_id(self, roadmap_id: int) -> Optional[RoadmapRecordModel]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM roadmaps WHERE id = ?", (roadmap_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return RoadmapRecordModel(
                id=row["id"],
                student_id=row["student_id"],
                career_code=row["career_code"],
                career_title=row["career_title"],
                compatibility_score=row["compatibility_score"],
                roadmap_json=json.loads(row["roadmap_json"]),
                created_at=row["created_at"]
            )

    def list_all_roadmaps(self) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id, r.student_id, r.career_code, r.career_title, 
                       r.compatibility_score, r.created_at, s.full_name
                FROM roadmaps r
                LEFT JOIN student_profiles s ON r.student_id = s.id
                ORDER BY r.id DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_task_progress(self, roadmap_id: int, task_id: str, is_completed: bool):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE task_progress
                SET is_completed = ?, updated_at = datetime('now')
                WHERE roadmap_id = ? AND task_id = ?
            """, (1 if is_completed else 0, roadmap_id, task_id))
            conn.commit()

    def get_task_progress(self, roadmap_id: int) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT task_id, phase_number, month_number, task_description, is_completed
                FROM task_progress
                WHERE roadmap_id = ?
                ORDER BY month_number ASC, id ASC
            """, (roadmap_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
