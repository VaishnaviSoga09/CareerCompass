"""
Agent 5: Roadmap Planning Agent
CareerCompass - SIH25094 - CSE473 Agentic AI

Responsibilities:
- Combine outputs from all previous agents.
- Generate a personalized learning and career roadmap.
- Divide the roadmap into 5 mandated phases:
  Phase 1: Foundation
  Phase 2: Core Skills
  Phase 3: Advanced Skills
  Phase 4: Projects and Practical Experience
  Phase 5: Internship and Job Preparation
- Assign estimated timelines, milestones, and measurable outcomes.
- Generate a final structured roadmap.
"""

from typing import Dict, Any, List
from core.llm import LLMProvider
from core.prompts import ROADMAP_PLANNING_SYSTEM

class RoadmapPlanningAgent:
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        self.name = "Roadmap Planning Agent"

    def execute(
        self,
        student_profile: Dict[str, Any],
        career_discovery: Dict[str, Any],
        skill_gap: Dict[str, Any],
        learning_recs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Orchestrates all prior agent findings into an end-to-end multi-month roadmap.
        """
        target_career = career_discovery.get("selected_career", {})
        career_title = target_career.get("canonical_name") or target_career.get("title", "Software Specialist")
        duration_months = int(student_profile.get("learning_duration_months", 6))
        missing_skills = [
            item["skill"] if isinstance(item, dict) else str(item)
            for item in skill_gap.get("missing_technical_skills", [])
        ]
        existing_skills = skill_gap.get("existing_matching_skills", [])

        # LLM Synthesis Attempt
        user_prompt = (
            f"Candidate: {student_profile.get('full_name')} ({student_profile.get('degree_branch')})\n"
            f"Target Career: {career_title} (O*NET {target_career.get('onetsoc_code')})\n"
            f"Duration: {duration_months} Months\n"
            f"Existing Skills: {', '.join(existing_skills)}\n"
            f"Missing Skills to Acquire: {', '.join(missing_skills[:8])}\n"
            "Build an exact month-by-month roadmap divided across the 5 mandated phases."
        )

        llm_response = self.llm.generate_json_response(ROADMAP_PLANNING_SYSTEM, user_prompt)

        # Fallback / High-Fidelity Deterministic Generator
        if not llm_response or "timeline" not in llm_response:
            llm_response = self._generate_deterministic_roadmap(
                career_title=career_title,
                duration_months=duration_months,
                existing_skills=existing_skills,
                missing_skills=missing_skills
            )

        # Compile Complete Final Structured Dossier
        final_roadmap = {
            "agent": self.name,
            "status": "COMPLETED",
            "student_profile": student_profile,
            "selected_career": target_career,
            "all_recommended_careers": career_discovery.get("top_careers", []),
            "skill_gap_analysis": skill_gap,
            "learning_recommendations": learning_recs,
            "roadmap_title": f"Mastery Roadmap: {career_title} ({duration_months} Months)",
            "phases_summary": llm_response.get("phases_summary", self._default_phases()),
            "timeline": llm_response.get("timeline", [])
        }

        return final_roadmap

    def _default_phases(self) -> List[Dict[str, Any]]:
        return [
            {"phase_number": 1, "phase_name": "Phase 1: Foundation", "focus": "Syntax, core programming, computer science principles & version control"},
            {"phase_number": 2, "phase_name": "Phase 2: Core Skills", "focus": "Essential domain libraries, relational databases, data pipelines & algorithms"},
            {"phase_number": 3, "phase_name": "Phase 3: Advanced Skills", "focus": "Specialized frameworks, architecture design, cloud deployment & optimization"},
            {"phase_number": 4, "phase_name": "Phase 4: Projects & Practical Experience", "focus": "End-to-end capstone systems, production CI/CD, documentation & testing"},
            {"phase_number": 5, "phase_name": "Phase 5: Internship & Job Preparation", "focus": "Technical interviews, LeetCode problem solving, resume refinement & mock interviews"}
        ]

    def _generate_deterministic_roadmap(
        self,
        career_title: str,
        duration_months: int,
        existing_skills: List[str],
        missing_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Creates a granular, high-fidelity month-by-month timeline adapted to duration.
        """
        c_lower = career_title.lower()
        timeline = []

        # Determine domain-specific items
        is_ai_ml = any(x in c_lower for x in ["ai", "machine learning", "data scientist", "deep learning"])
        is_cloud = any(x in c_lower for x in ["cloud", "devops", "systems engineer", "architect"])
        is_cyber = any(x in c_lower for x in ["security", "cyber", "penetration"])

        # Month 1
        if is_ai_ml:
            m1_actions = [
                "Master advanced Python fundamentals: decorators, generators, and object-oriented design.",
                "Review linear algebra & matrix operations with NumPy and vectorization exercises.",
                "Set up Git, GitHub repository workflow, and clean virtual environment isolation.",
                "Solve 20 practice algorithmic problems on arrays, dictionaries, and string manipulation."
            ]
            m1_project = "CLI Numerical Matrix Engine & Algorithmic Problem Solver"
        elif is_cloud:
            m1_actions = [
                "Master Linux command line navigation, shell scripting (Bash), and process management.",
                "Deep dive into networking essentials: TCP/IP, DNS, Subnets, and HTTP/S protocols.",
                "Configure automated Git branching strategies and SSH key-based repository access.",
                "Practice core automation scripts for remote server health checks."
            ]
            m1_project = "Automated Linux Server Provisioning & Health Monitor Script"
        elif is_cyber:
            m1_actions = [
                "Establish fundamentals in computer networking (OSI Model, TCP/IP handshake, ports).",
                "Learn Linux system administration, permission management, and log inspection.",
                "Study cryptography basics: symmetric vs asymmetric encryption, hashing, and TLS.",
                "Set up a dedicated isolated virtual lab using VirtualBox or WSL2."
            ]
            m1_project = "Network Packet Analyzer & Port Scanner in Python"
        else:
            m1_actions = [
                "Solidify Object-Oriented Programming (OOP) in Python or Java with clean code principles.",
                "Learn Git version control, pull requests, semantic commit conventions, and branch management.",
                "Study fundamental Data Structures: Arrays, Linked Lists, Stacks, and Queues.",
                "Solve beginner algorithmic challenges on LeetCode and HackerRank."
            ]
            m1_project = "Modular CLI Task & Inventory Management System with Unit Tests"

        timeline.append({
            "month": 1,
            "phase": "Phase 1: Foundation",
            "phase_number": 1,
            "title": "Core Foundations & Tooling",
            "action_items": m1_actions,
            "project_outcome": m1_project,
            "milestones": ["Environment configured", "20 DSA problems solved", "Initial GitHub repository launched"]
        })

        # Month 2
        if is_ai_ml:
            m2_actions = [
                "Master exploratory data analysis (EDA) with Pandas, Matplotlib, and Seaborn.",
                "Write complex SQL queries (multi-table JOINs, Window functions, aggregations) for analytics.",
                "Clean, impute, and preprocess real-world tabular datasets from Kaggle.",
                "Build statistical hypotheses testing and correlation analysis pipelines."
            ]
            m2_project = "Interactive Exploratory Data Analytics Dashboard on Real-World Datasets"
        elif is_cloud:
            m2_actions = [
                "Master containerization fundamentals with Docker: Dockerfiles, multi-stage builds, and images.",
                "Compose multi-service architectures using Docker Compose (web + Redis + PostgreSQL).",
                "Understand container networking, persistent volume mounts, and security isolation.",
                "Deploy local microservices test suites with Dockerized containers."
            ]
            m2_project = "Multi-Container Microservices Deployment with Docker Compose & Nginx"
        elif is_cyber:
            m2_actions = [
                "Analyze network traffic dumps with Wireshark and conduct vulnerability scans with Nmap.",
                "Study OWASP Top 10 vulnerabilities (SQL Injection, XSS, CSRF, broken access control).",
                "Practice vulnerability identification in controlled TryHackMe / PortSwigger labs.",
                "Implement input sanitization and secure coding defenses in sample web apps."
            ]
            m2_project = "Automated OWASP Web Vulnerability Scanner & Security Audit Report"
        else:
            m2_actions = [
                "Master Relational Database design: 3NF normalization, PostgreSQL schema design, and indexing.",
                "Build RESTful APIs with FastAPI or Spring Boot implementing CRUD and validation.",
                "Implement JWT token authentication and role-based access control.",
                "Deepen DSA proficiency: Trees, Binary Search Trees, and Heaps."
            ]
            m2_project = "RESTful API Backend with PostgreSQL, JWT Auth, and Swagger Documentation"

        timeline.append({
            "month": 2,
            "phase": "Phase 2: Core Skills",
            "phase_number": 2,
            "title": "Core Domain Systems & Data Pipelines",
            "action_items": m2_actions,
            "project_outcome": m2_project,
            "milestones": ["Core API / Pipeline operational", "Database integration complete", "30 LeetCode problems completed"]
        })

        # Month 3
        if is_ai_ml:
            m3_actions = [
                "Implement classical machine learning algorithms from scratch: Linear/Logistic Regression, Decision Trees.",
                "Master Scikit-learn pipelines: Feature scaling, cross-validation, hyperparameter tuning (GridSearchCV).",
                "Study model evaluation metrics: ROC-AUC, Precision-Recall, F1-Score, and Confusion Matrix.",
                "Deploy a trained Scikit-learn classification model via a lightweight FastAPI REST microservice."
            ]
            m3_project = "End-to-End Machine Learning Prediction Web Service with Live Scoring"
        elif is_cloud:
            m3_actions = [
                "Master Infrastructure as Code (IaC) using Terraform: Providers, State files, and Modules.",
                "Provision cloud infrastructure on AWS: EC2 instances, VPC, Subnets, Internet Gateways, and S3.",
                "Implement AWS Identity & Access Management (IAM) least-privilege security policies.",
                "Automate cloud resource provisioning and teardown using Terraform scripts."
            ]
            m3_project = "Terraform-Automated AWS Resilient Multi-Tier Infrastructure Pipeline"
        elif is_cyber:
            m3_actions = [
                "Deploy and configure an open-source Security Information and Event Management (SIEM) tool.",
                "Write custom detection rules for brute-force attacks, port scans, and suspicious authentication.",
                "Analyze malware persistence mechanisms, Windows Event Logs, and Linux audit logs.",
                "Participate in beginner Capture The Flag (CTF) challenges on picoCTF."
            ]
            m3_project = "SOC Log Analysis & Automated SIEM Incident Detection Pipeline"
        else:
            m3_actions = [
                "Learn modern frontend integration with React / Next.js or modern state management.",
                "Connect frontend client to backend REST APIs with optimistic UI and error states.",
                "Implement caching layers with Redis and database query optimization.",
                "Study system design fundamentals: caching, load balancing, and horizontal scaling."
            ]
            m3_project = "Full-Stack Web Application with Caching and Async Job Processing"

        timeline.append({
            "month": 3,
            "phase": "Phase 3: Advanced Skills",
            "phase_number": 3,
            "title": "Advanced Frameworks & Architecture",
            "action_items": m3_actions,
            "project_outcome": m3_project,
            "milestones": ["Advanced framework operational", "Integration testing suite running", "Clean API contract verified"]
        })

        # Month 4
        if is_ai_ml:
            m4_actions = [
                "Deep dive into Neural Networks and Deep Learning using PyTorch.",
                "Train convolutional neural networks (CNNs) for vision or fine-tune Transformers with Hugging Face.",
                "Implement MLOps practices: Model tracking with MLflow/Weights & Biases and Dockerized inference.",
                "Package the solution with an interactive Streamlit UI and comprehensive documentation."
            ]
            m4_project = "Production-Grade AI Capstone System with PyTorch, MLOps Tracking & Streamlit UI"
        elif is_cloud:
            m4_actions = [
                "Master Kubernetes: Pods, Deployments, Services, Ingress Controllers, and ConfigMaps.",
                "Build continuous integration and delivery (CI/CD) pipelines with GitHub Actions.",
                "Implement centralized monitoring and metrics dashboards using Prometheus and Grafana.",
                "Deploy the full containerized stack onto a managed Kubernetes cluster."
            ]
            m4_project = "Production Kubernetes Cluster with GitOps CI/CD & Prometheus Monitoring"
        elif is_cyber:
            m4_actions = [
                "Conduct end-to-end security penetration testing across simulated enterprise environments.",
                "Perform binary analysis and reverse engineering basics with Ghidra.",
                "Document vulnerability findings using standard CVSS scoring and remediation reports.",
                "Harden cloud and Linux servers according to CIS benchmark standards."
            ]
            m4_project = "Enterprise Penetration Test Dossier & Security Hardening Automation Suite"
        else:
            m4_actions = [
                "Build a large-scale capstone project incorporating microservices architecture.",
                "Implement automated CI/CD pipelines with GitHub Actions, linting, and automated testing.",
                "Containerize all services with Docker and optimize container images for production.",
                "Write comprehensive architectural documentation with C4 diagrams and API specifications."
            ]
            m4_project = "Production-Grade Distributed Cloud Microservice System with CI/CD"

        timeline.append({
            "month": 4,
            "phase": "Phase 4: Projects and Practical Experience",
            "phase_number": 4,
            "title": "Comprehensive Capstone Portfolio Project",
            "action_items": m4_actions,
            "project_outcome": m4_project,
            "milestones": ["Live production deployment", "GitHub README with video demo", "100% test coverage for critical paths"]
        })

        # Month 5
        timeline.append({
            "month": 5,
            "phase": "Phase 5: Internship and Job Preparation",
            "phase_number": 5,
            "title": "Technical Interviews & Placement Preparation",
            "action_items": [
                "Complete targeted LeetCode Top 75 / Blind 75 questions (Focus on Graphs, DP, Trees).",
                "Practice mock technical interviews with peers or platforms like Pramp / Interviewing.io.",
                "Format resume using standard single-page tech format highlighting measurable project impacts.",
                "Draft clear answers to behavioral questions using the STAR (Situation, Task, Action, Result) method."
            ],
            "project_outcome": "Polished Industry Resume, Portfolio Website, and Interview Preparation Notes",
            "milestones": ["50+ LeetCode Mediums solved", "3 mock interviews conducted", "Resume peer-reviewed"]
        })

        # Month 6
        timeline.append({
            "month": 6,
            "phase": "Phase 5: Internship and Job Preparation",
            "phase_number": 5,
            "title": "Internship Outreach & Job Placement Drives",
            "action_items": [
                "Apply to 20-30 curated internship and junior engineering openings across LinkedIn, Wellfound, and campus drives.",
                "Engage in targeted professional outreach to hiring managers and tech alumni.",
                "Complete company take-home coding assessments and system architecture design challenges.",
                "Conduct continuous mock HR and managerial interviews to master salary and offer negotiation."
            ],
            "project_outcome": "Active Placement Pipeline & Internship / Junior Role Offers",
            "milestones": ["Applications submitted", "Interview calls secured", "Offer negotiation preparation"]
        })

        # If user selected 3, 12, or 18 months, scale appropriately
        if duration_months == 3:
            return {
                "phases_summary": self._default_phases(),
                "timeline": [
                    timeline[0],  # Month 1: Foundation & Core
                    timeline[2],  # Month 2: Advanced & Projects
                    timeline[4]   # Month 3: Job Prep & Interviews
                ]
            }
        elif duration_months >= 12:
            extended = []
            for m in range(1, duration_months + 1):
                base_idx = min(int((m - 1) / (duration_months / 6)), 5)
                base = timeline[base_idx].copy()
                base["month"] = m
                base["title"] = f"Month {m}: {base['title']} (Extended Mastery)"
                extended.append(base)
            return {
                "phases_summary": self._default_phases(),
                "timeline": extended
            }

        return {
            "phases_summary": self._default_phases(),
            "timeline": timeline
        }
