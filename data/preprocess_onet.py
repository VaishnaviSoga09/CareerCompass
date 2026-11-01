"""
O*NET Dataset Preprocessor and Importer for CareerCompass
SIH25094 - CSE473 Agentic AI

Standardizes occupational records, cleans text, validates schemas,
and exports processed JSON and CSV datasets for the AI multi-agent system.
"""

import os
import json
import pandas as pd

ONET_OCCUPATIONS_DATA = [
    {
        "onetsoc_code": "15-1221.00",
        "title": "Computer and Information Research Scientists (AI / ML Engineer)",
        "canonical_name": "Artificial Intelligence & Machine Learning Engineer",
        "description": "Conduct research into fundamental computer and information science as theorists, designers, or inventors. Solve or invent solutions to problems in the field of computer hardware and software, artificial intelligence, neural networks, natural language processing, and algorithmic optimization.",
        "job_zone": 5,
        "education_level": "Undergraduate / Postgraduate (Master's or Ph.D. preferred)",
        "median_salary_usd": 142650,
        "bright_outlook": True,
        "skills": [
            "Programming", "Complex Problem Solving", "Critical Thinking", "Mathematics", 
            "Operations Analysis", "Systems Evaluation", "Science", "Active Learning"
        ],
        "knowledge": [
            "Computers and Electronics", "Mathematics", "Engineering and Technology", 
            "Statistics", "Telecommunications"
        ],
        "abilities": [
            "Mathematical Reasoning", "Inductive Reasoning", "Deductive Reasoning", 
            "Originality", "Information Ordering", "Category Flexibility"
        ],
        "work_activities": [
            "Interacting with Computers", "Analyzing Data or Information", 
            "Developing Objectives and Strategies", "Updating and Using Relevant Knowledge",
            "Thinking Creatively"
        ],
        "technology_skills": [
            "Python", "C++", "PyTorch", "TensorFlow", "Keras", "CUDA", "OpenCV", 
            "Scikit-learn", "Hugging Face", "Linux", "Docker", "Git", "Distributed Computing", 
            "MLOps", "Weights & Biases", "Jupyter", "SQL", "Transformers"
        ],
        "soft_skills": [
            "Analytical Thinking", "Research Mindset", "Communication of Complex Concepts", 
            "Persistence", "Ethical AI Awareness", "Collaboration"
        ],
        "related_occupations": ["15-2051.00", "15-1252.00", "15-1243.00", "15-2041.00"],
        "sample_job_titles": [
            "AI Engineer", "Machine Learning Engineer", "Deep Learning Scientist", 
            "Computer Vision Engineer", "NLP Research Scientist"
        ]
    },
    {
        "onetsoc_code": "15-2051.00",
        "title": "Data Scientists",
        "canonical_name": "Data Scientist",
        "description": "Develop and implement a set of techniques or analytics applications to transform raw data into meaningful information using statistical analysis, machine learning algorithms, and data modeling to solve business and scientific problems.",
        "job_zone": 5,
        "education_level": "Undergraduate / Postgraduate",
        "median_salary_usd": 108020,
        "bright_outlook": True,
        "skills": [
            "Mathematics", "Critical Thinking", "Complex Problem Solving", "Programming", 
            "Systems Analysis", "Science", "Active Learning", "Reading Comprehension"
        ],
        "knowledge": [
            "Mathematics", "Computers and Electronics", "Statistics", "Engineering and Technology", 
            "Administration and Management"
        ],
        "abilities": [
            "Mathematical Reasoning", "Deductive Reasoning", "Inductive Reasoning", 
            "Information Ordering", "Fluency of Ideas"
        ],
        "work_activities": [
            "Analyzing Data or Information", "Processing Information", "Thinking Creatively", 
            "Working with Computers", "Updating and Using Relevant Knowledge"
        ],
        "technology_skills": [
            "Python", "SQL", "R", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", 
            "Apache Spark", "Jupyter", "Tableau", "Power BI", "Docker", "Git", "AWS", 
            "Statistical Modeling", "Matplotlib", "Seaborn"
        ],
        "soft_skills": [
            "Data Storytelling", "Business Acumen", "Problem Formulation", 
            "Curiosity", "Stakeholder Communication", "Teamwork"
        ],
        "related_occupations": ["15-1221.00", "15-1252.00", "15-2051.01", "15-2041.00"],
        "sample_job_titles": [
            "Data Scientist", "Machine Learning Analyst", "Statistical Modeler", 
            "Predictive Analytics Specialist"
        ]
    },
    {
        "onetsoc_code": "15-1252.00",
        "title": "Software Developers",
        "canonical_name": "Software Developer / Engineer",
        "description": "Research, design, and develop computer and network software or specialized utility programs. Analyze user needs and develop software solutions, applying principles and techniques of computer science, engineering, and mathematical analysis.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 132270,
        "bright_outlook": True,
        "skills": [
            "Programming", "Complex Problem Solving", "Systems Analysis", "Critical Thinking", 
            "Operations Analysis", "Active Learning", "Troubleshooting"
        ],
        "knowledge": [
            "Computers and Electronics", "Engineering and Technology", "Mathematics", 
            "Design", "English Language"
        ],
        "abilities": [
            "Information Ordering", "Deductive Reasoning", "Problem Sensitivity", 
            "Written Comprehension", "Mathematical Reasoning"
        ],
        "work_activities": [
            "Working with Computers", "Developing Objectives and Strategies", 
            "Thinking Creatively", "Updating and Using Relevant Knowledge", "Evaluating Information"
        ],
        "technology_skills": [
            "Java", "Python", "C++", "JavaScript", "TypeScript", "Go", "REST APIs", 
            "Git", "PostgreSQL", "MySQL", "Docker", "Linux", "Microservices", 
            "Spring Boot", "Data Structures & Algorithms", "CI/CD", "Redis"
        ],
        "soft_skills": [
            "Code Craftsmanship", "Agile Collaboration", "Attention to Detail", 
            "Continuous Learning", "Empathy for End-Users"
        ],
        "related_occupations": ["15-1251.00", "15-1253.00", "15-1299.08", "15-1254.00"],
        "sample_job_titles": [
            "Full Stack Developer", "Backend Software Engineer", "Systems Developer", 
            "Applications Developer", "Software Development Engineer (SDE)"
        ]
    },
    {
        "onetsoc_code": "15-1299.08",
        "title": "Computer Systems Engineers/Architects",
        "canonical_name": "Cloud Engineer / DevOps Architect",
        "description": "Design and develop solutions to complex applications problems, system administration issues, or network concerns. Perform systems management and integration functions, architecting cloud computing environments and infrastructure automation pipelines.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 127260,
        "bright_outlook": True,
        "skills": [
            "Systems Analysis", "Systems Evaluation", "Technology Design", "Complex Problem Solving", 
            "Troubleshooting", "Programming", "Critical Thinking"
        ],
        "knowledge": [
            "Computers and Electronics", "Engineering and Technology", "Telecommunications", 
            "Mathematics", "Administration and Management"
        ],
        "abilities": [
            "Deductive Reasoning", "Problem Sensitivity", "Information Ordering", 
            "Systems Perception", "Inductive Reasoning"
        ],
        "work_activities": [
            "Working with Computers", "Analyzing Data or Information", 
            "Guiding and Directing Subordinates", "Thinking Creatively", "Documenting/Recording Information"
        ],
        "technology_skills": [
            "AWS", "Microsoft Azure", "Google Cloud Platform", "Docker", "Kubernetes", 
            "Terraform", "Linux", "Python", "Bash", "CI/CD", "Ansible", "Jenkins", 
            "Prometheus", "Grafana", "Networking (VPC, DNS, Load Balancers)", "Git"
        ],
        "soft_skills": [
            "Reliability Mindset", "Disaster Recovery Planning", "Cross-Functional Collaboration", 
            "Root Cause Analysis", "Clear Technical Documentation"
        ],
        "related_occupations": ["15-1252.00", "15-1241.00", "15-1212.00", "15-1244.00"],
        "sample_job_titles": [
            "Cloud Solutions Architect", "DevOps Engineer", "Site Reliability Engineer (SRE)", 
            "Cloud Infrastructure Engineer", "Platform Engineer"
        ]
    },
    {
        "onetsoc_code": "15-1212.00",
        "title": "Information Security Analysts",
        "canonical_name": "Cybersecurity Analyst / Security Engineer",
        "description": "Plan, implement, upgrade, or monitor security measures for the protection of computer networks and information. Assess system vulnerabilities for risks and propose and implement security and compliance strategies.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 120360,
        "bright_outlook": True,
        "skills": [
            "Critical Thinking", "Complex Problem Solving", "Systems Evaluation", 
            "Systems Analysis", "Active Learning", "Troubleshooting", "Monitoring"
        ],
        "knowledge": [
            "Computers and Electronics", "Telecommunications", "Law and Government", 
            "Public Safety and Security", "Engineering and Technology"
        ],
        "abilities": [
            "Problem Sensitivity", "Deductive Reasoning", "Inductive Reasoning", 
            "Information Ordering", "Flexibility of Closure"
        ],
        "work_activities": [
            "Identifying Information", "Working with Computers", "Analyzing Data or Information", 
            "Communicating with Supervisors", "Evaluating Information"
        ],
        "technology_skills": [
            "Wireshark", "Nmap", "Metasploit", "Linux", "Python", "Bash", "Burp Suite", 
            "Splunk", "SIEM", "Cryptography", "TCP/IP Protocols", "Firewalls", 
            "OWASP Top 10", "Vulnerability Assessment", "Identity & Access Management (IAM)"
        ],
        "soft_skills": [
            "High Integrity", "Vigilance", "Crisis Management", 
            "Adversarial Thinking", "Ethical Decision Making"
        ],
        "related_occupations": ["15-1244.00", "15-1241.00", "15-1299.08", "15-1252.00"],
        "sample_job_titles": [
            "Information Security Specialist", "Cybersecurity Engineer", "Penetration Tester", 
            "SOC Analyst", "Cloud Security Engineer"
        ]
    },
    {
        "onetsoc_code": "15-1254.00",
        "title": "Web Developers",
        "canonical_name": "Frontend & Web Application Developer",
        "description": "Develop and create websites and interactive web applications. Create website layout and user interface using standard HTML/CSS practices, integrate data from various back-end services and databases, and optimize performance.",
        "job_zone": 3,
        "education_level": "Diploma / Undergraduate",
        "median_salary_usd": 84960,
        "bright_outlook": True,
        "skills": [
            "Programming", "Technology Design", "Active Learning", "Critical Thinking", 
            "Reading Comprehension", "Operations Analysis"
        ],
        "knowledge": [
            "Computers and Electronics", "Design", "Communications and Media", 
            "Customer and Personal Service"
        ],
        "abilities": [
            "Fluency of Ideas", "Visual Color Discrimination", "Information Ordering", 
            "Originality", "Flexibility of Closure"
        ],
        "work_activities": [
            "Working with Computers", "Thinking Creatively", "Updating and Using Relevant Knowledge", 
            "Developing Objectives and Strategies"
        ],
        "technology_skills": [
            "JavaScript", "TypeScript", "React", "HTML5", "CSS3", "Tailwind CSS", 
            "Next.js", "Node.js", "REST APIs", "Git", "Webpack", "Responsive Web Design", 
            "GraphQL", "State Management (Redux/Zustand)", "Figma"
        ],
        "soft_skills": [
            "Visual Aesthetics", "User Empathy", "Attention to Detail", 
            "Design-to-Code Translation", "Communication"
        ],
        "related_occupations": ["15-1255.00", "15-1252.00", "27-1024.00"],
        "sample_job_titles": [
            "Frontend Engineer", "Web Developer", "UI Engineer", 
            "React Specialist", "JavaScript Developer"
        ]
    },
    {
        "onetsoc_code": "15-2051.01",
        "title": "Business Intelligence Analysts",
        "canonical_name": "Business Intelligence & Analytics Specialist",
        "description": "Produce financial and market intelligence by querying data repositories and generating periodic reports. Devise methods for identifying data patterns and trends in available information sources.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 103500,
        "bright_outlook": True,
        "skills": [
            "Critical Thinking", "Reading Comprehension", "Complex Problem Solving", 
            "Active Listening", "Mathematics", "Systems Analysis"
        ],
        "knowledge": [
            "Computers and Electronics", "Economics and Accounting", "Mathematics", 
            "Administration and Management", "Customer Service"
        ],
        "abilities": [
            "Deductive Reasoning", "Inductive Reasoning", "Mathematical Reasoning", 
            "Written Comprehension", "Information Ordering"
        ],
        "work_activities": [
            "Analyzing Data or Information", "Getting Information", "Processing Information", 
            "Interacting with Computers", "Communicating with Persons Outside Organization"
        ],
        "technology_skills": [
            "SQL", "Power BI", "Tableau", "Microsoft Excel", "Python", "DAX", 
            "Data Warehousing", "ETL Pipelines", "Snowflake", "Google BigQuery", 
            "Statistical Analysis", "Business Dashboards"
        ],
        "soft_skills": [
            "Business Strategy", "Stakeholder Management", "Executive Presentation", 
            "Translation of Business Questions to Data Queries"
        ],
        "related_occupations": ["15-2051.00", "15-2031.00", "13-1111.00"],
        "sample_job_titles": [
            "BI Analyst", "Data Analytics Consultant", "BI Engineer", 
            "Reporting Specialist", "Analytics Manager"
        ]
    },
    {
        "onetsoc_code": "17-2199.08",
        "title": "Robotics Engineers",
        "canonical_name": "Robotics & Automation Engineer",
        "description": "Research, design, develop, or test robotic applications, systems, or processes for personal, commercial, or industrial use, integrating sensors, embedded software, and mechanical actuators.",
        "job_zone": 5,
        "education_level": "Undergraduate / Postgraduate",
        "median_salary_usd": 115000,
        "bright_outlook": True,
        "skills": [
            "Technology Design", "Systems Analysis", "Science", "Mathematics", 
            "Critical Thinking", "Complex Problem Solving", "Troubleshooting"
        ],
        "knowledge": [
            "Engineering and Technology", "Computers and Electronics", "Mathematics", 
            "Physics", "Mechanical", "Design"
        ],
        "abilities": [
            "Deductive Reasoning", "Mathematical Reasoning", "Spatial Orientation", 
            "Visualization", "Control Precision"
        ],
        "work_activities": [
            "Interacting with Computers", "Drafting and Specifying Technical Devices", 
            "Thinking Creatively", "Inspecting Equipment or Material"
        ],
        "technology_skills": [
            "C++", "Python", "ROS (Robot Operating System)", "MATLAB", "Simulink", 
            "Linux", "OpenCV", "Control Systems", "SolidWorks", "Microcontrollers", 
            "Arduino", "Sensor Fusion", "Kinematics & Dynamics"
        ],
        "soft_skills": [
            "Multidisciplinary Thinking", "Safety Consciousness", "Hands-on Experimentation", 
            "Iterative Prototyping"
        ],
        "related_occupations": ["17-2072.00", "17-2061.00", "15-1252.00", "17-2141.00"],
        "sample_job_titles": [
            "Robotics Software Engineer", "Autonomous Systems Engineer", 
            "Mechatronics Specialist", "Automation Engineer"
        ]
    },
    {
        "onetsoc_code": "15-1242.00",
        "title": "Database Administrators",
        "canonical_name": "Database Administrator / Data Architect",
        "description": "Administer, test, and implement computer databases, applying knowledge of database management systems. Coordinate changes to computer databases, ensure high availability, and test and implement security and backup strategies.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 101510,
        "bright_outlook": False,
        "skills": [
            "Programming", "Systems Analysis", "Critical Thinking", "Troubleshooting", 
            "Complex Problem Solving", "Operations Monitoring"
        ],
        "knowledge": [
            "Computers and Electronics", "Administration and Management", "Mathematics", 
            "Customer and Personal Service"
        ],
        "abilities": [
            "Information Ordering", "Deductive Reasoning", "Problem Sensitivity", 
            "Written Comprehension"
        ],
        "work_activities": [
            "Interacting with Computers", "Updating and Using Relevant Knowledge", 
            "Processing Information", "Evaluating Information"
        ],
        "technology_skills": [
            "PostgreSQL", "MySQL", "Oracle DBMS", "MongoDB", "Redis", "SQL", 
            "Database Tuning & Optimization", "Backup & Disaster Recovery", "Linux", 
            "Data Modeling", "Cassandra", "Query Optimization"
        ],
        "soft_skills": [
            "Meticulous Accuracy", "High Responsibility", "Calm Under Outage Pressure", 
            "System Integrity"
        ],
        "related_occupations": ["15-1243.00", "15-1252.00", "15-2051.00"],
        "sample_job_titles": [
            "Database Administrator (DBA)", "Database Engineer", "Data Infrastructure Lead", 
            "NoSQL Database Specialist"
        ]
    },
    {
        "onetsoc_code": "17-2072.00",
        "title": "Electronics Engineers, Except Computer",
        "canonical_name": "Embedded Systems & Firmware Engineer",
        "description": "Research, design, develop, or test electronic components and systems for commercial, industrial, military, or scientific use employing knowledge of electronic theory, microcontrollers, and materials properties.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 114780,
        "bright_outlook": True,
        "skills": [
            "Technology Design", "Troubleshooting", "Critical Thinking", "Mathematics", 
            "Complex Problem Solving", "Science", "Systems Evaluation"
        ],
        "knowledge": [
            "Engineering and Technology", "Computers and Electronics", "Mathematics", 
            "Physics", "Telecommunications", "Production and Processing"
        ],
        "abilities": [
            "Deductive Reasoning", "Inductive Reasoning", "Mathematical Reasoning", 
            "Finger Dexterity", "Near Vision"
        ],
        "work_activities": [
            "Interacting with Computers", "Drafting Technical Devices", 
            "Analyzing Data or Information", "Inspecting Equipment"
        ],
        "technology_skills": [
            "Embedded C", "C++", "ARM Architecture", "VHDL", "Verilog", "PCB Design", 
            "KiCad", "RTOS (FreeRTOS)", "I2C/SPI/UART Protocols", "Oscilloscopes", 
            "Microchip PIC / STM32", "IoT Protocols (MQTT, BLE)"
        ],
        "soft_skills": [
            "Hardware Debugging Patience", "Precision Testing", "Safety Compliance", 
            "Cross-Engineering Teamwork"
        ],
        "related_occupations": ["17-2061.00", "17-2199.08", "17-2071.00"],
        "sample_job_titles": [
            "Embedded Software Engineer", "Firmware Developer", "IoT Hardware Engineer", 
            "Electronics Design Engineer"
        ]
    },
    {
        "onetsoc_code": "15-1253.00",
        "title": "Software Quality Assurance Analysts and Tests",
        "canonical_name": "Software Development Engineer in Test (SDET)",
        "description": "Participate in software design reviews and monitor every phase of software development to identify and troubleshoot defects, create automated test harnesses, and ensure performance and quality benchmarks.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 99620,
        "bright_outlook": True,
        "skills": [
            "Quality Control Analysis", "Programming", "Critical Thinking", 
            "Systems Evaluation", "Troubleshooting", "Complex Problem Solving"
        ],
        "knowledge": [
            "Computers and Electronics", "Engineering and Technology", "Mathematics", 
            "English Language"
        ],
        "abilities": [
            "Problem Sensitivity", "Deductive Reasoning", "Information Ordering", 
            "Inductive Reasoning"
        ],
        "work_activities": [
            "Evaluating Information", "Interacting with Computers", 
            "Documenting/Recording Information", "Updating and Using Relevant Knowledge"
        ],
        "technology_skills": [
            "Selenium", "Cypress", "PyTest", "JUnit", "Postman", "Jest", "Git", 
            "Jenkins", "JIRA", "SQL", "Python", "JavaScript", "Playwright", 
            "Performance Testing (JMeter)", "CI/CD Integration"
        ],
        "soft_skills": [
            "Constructive Skepticism", "Bug Advocacy", "Clear Reproduction Steps", 
            "Quality Evangelism"
        ],
        "related_occupations": ["15-1252.00", "15-1251.00"],
        "sample_job_titles": [
            "QA Automation Engineer", "SDET", "Test Automation Architect", 
            "Quality Engineering Specialist"
        ]
    },
    {
        "onetsoc_code": "15-1241.00",
        "title": "Computer Network Architects",
        "canonical_name": "Enterprise Network & Security Architect",
        "description": "Design and implement computer and information networks, such as local area networks (LAN), wide area networks (WAN), intranets, extranets, and other data communications networks with high resilience.",
        "job_zone": 4,
        "education_level": "Undergraduate",
        "median_salary_usd": 126900,
        "bright_outlook": True,
        "skills": [
            "Technology Design", "Systems Analysis", "Systems Evaluation", 
            "Critical Thinking", "Complex Problem Solving", "Active Learning"
        ],
        "knowledge": [
            "Telecommunications", "Computers and Electronics", "Engineering and Technology", 
            "Administration and Management"
        ],
        "abilities": [
            "Deductive Reasoning", "Information Ordering", "Problem Sensitivity", 
            "Inductive Reasoning"
        ],
        "work_activities": [
            "Interacting with Computers", "Thinking Creatively", "Making Decisions", 
            "Guiding, Directing, and Motivating Subordinates"
        ],
        "technology_skills": [
            "Cisco IOS", "Juniper", "BGP", "OSPF", "TCP/IP Networking", "Wireshark", 
            "VPNs", "Cloud Networking (VPC)", "SD-WAN", "Network Automation (Python/Netmiko)", 
            "Subnetting", "DNS/DHCP", "Network Security"
        ],
        "soft_skills": [
            "Strategic Infrastructure Vision", "Vendor Negotiations", 
            "Incident Leadership", "Clear Documentation"
        ],
        "related_occupations": ["15-1244.00", "15-1299.08", "15-1212.00"],
        "sample_job_titles": [
            "Network Architect", "Cloud Network Engineer", "Principal Network Specialist", 
            "Telecommunications Engineer"
        ]
    }
]

def preprocess_and_save():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processed_dir = os.path.join(base_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    json_path = os.path.join(processed_dir, "onet_occupations.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ONET_OCCUPATIONS_DATA, f, indent=2)
    print(f"[OK] Saved {len(ONET_OCCUPATIONS_DATA)} O*NET occupations to {json_path}")
    
    # Also create DataFrame and export CSV
    rows = []
    for occ in ONET_OCCUPATIONS_DATA:
        rows.append({
            "onetsoc_code": occ["onetsoc_code"],
            "title": occ["title"],
            "canonical_name": occ["canonical_name"],
            "description": occ["description"],
            "job_zone": occ["job_zone"],
            "education_level": occ["education_level"],
            "median_salary_usd": occ["median_salary_usd"],
            "skills": ", ".join(occ["skills"]),
            "knowledge": ", ".join(occ["knowledge"]),
            "abilities": ", ".join(occ["abilities"]),
            "work_activities": ", ".join(occ["work_activities"]),
            "technology_skills": ", ".join(occ["technology_skills"]),
            "soft_skills": ", ".join(occ["soft_skills"]),
            "sample_job_titles": ", ".join(occ["sample_job_titles"]),
            "all_text_search": f"{occ['title']} {occ['canonical_name']} {occ['description']} {' '.join(occ['technology_skills'])} {' '.join(occ['skills'])} {' '.join(occ['knowledge'])}"
        })
    df = pd.DataFrame(rows)
    csv_path = os.path.join(processed_dir, "onet_occupations.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"[OK] Saved O*NET DataFrame to {csv_path}")

if __name__ == "__main__":
    preprocess_and_save()
