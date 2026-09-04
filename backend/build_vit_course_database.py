import json
import os


OUTPUT_FILE = "data/vit_courses.json"

LAST_VERIFIED = "2026-09-04"


courses = [

    # ============================================================
    # CSE / AI & ML
    # ============================================================

    {
        "name": "Machine Learning",
        "code": "BCSE209L",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Machine Learning",
            "Python",
            "Data Analysis",
            "Model Development"
        ],
        "career_domains": [
            "Machine Learning Engineer",
            "Data Scientist",
            "AI Engineer"
        ],
        "description": "Study of machine learning algorithms, model development and data-driven prediction."
    },

    {
        "name": "Deep Learning",
        "code": "BCSE332L",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Deep Learning",
            "Neural Networks",
            "Python",
            "PyTorch",
            "TensorFlow"
        ],
        "career_domains": [
            "Machine Learning Engineer",
            "AI Engineer",
            "Computer Vision Engineer",
            "NLP Engineer"
        ],
        "description": "Neural network architectures and deep learning techniques for AI applications."
    },

    {
        "name": "Machine Vision",
        "code": "BCSE417L",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Computer Vision",
            "Deep Learning",
            "Image Processing",
            "Python"
        ],
        "career_domains": [
            "Computer Vision Engineer",
            "AI Engineer",
            "Robotics Engineer"
        ],
        "description": "Computer vision techniques for image understanding and intelligent systems."
    },

    {
        "name": "Explainable Artificial Intelligence",
        "code": "BCSE418L",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Explainable AI",
            "Machine Learning",
            "Model Interpretation",
            "Responsible AI"
        ],
        "career_domains": [
            "AI Engineer",
            "Machine Learning Engineer",
            "AI Researcher"
        ],
        "description": "Methods for interpreting and explaining machine learning and AI models."
    },

    {
        "name": "Speech and Language Processing",
        "code": "BCSE419L",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "NLP",
            "Speech Processing",
            "Natural Language Understanding",
            "Deep Learning"
        ],
        "career_domains": [
            "NLP Engineer",
            "AI Engineer",
            "Generative AI Engineer"
        ],
        "description": "Processing and understanding human speech and natural language using computational methods."
    },

    {
        "name": "Artificial Intelligence",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT"
        ],
        "skills": [
            "Artificial Intelligence",
            "Search Algorithms",
            "Knowledge Representation",
            "Problem Solving"
        ],
        "career_domains": [
            "AI Engineer",
            "Machine Learning Engineer",
            "AI Researcher"
        ],
        "description": "Foundational artificial intelligence concepts and intelligent problem solving."
    },

    {
        "name": "Natural Language Processing",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT"
        ],
        "skills": [
            "NLP",
            "Text Processing",
            "Machine Learning",
            "Language Models"
        ],
        "career_domains": [
            "NLP Engineer",
            "AI Engineer",
            "Generative AI Engineer"
        ],
        "description": "Computational techniques for processing and analysing natural language."
    },

    {
        "name": "Image Processing",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech ECE",
            "B.Tech EIE"
        ],
        "skills": [
            "Image Processing",
            "Computer Vision",
            "Signal Processing",
            "Python"
        ],
        "career_domains": [
            "Computer Vision Engineer",
            "AI Engineer",
            "Signal Processing Engineer"
        ],
        "description": "Digital image processing techniques for analysis and intelligent applications."
    },

    # ============================================================
    # DATA / CLOUD / SOFTWARE
    # ============================================================

    {
        "name": "Data Science for Engineers",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech ECE",
            "B.Tech EIE",
            "B.Tech EEE"
        ],
        "skills": [
            "Data Science",
            "Statistics",
            "Python",
            "Data Analysis"
        ],
        "career_domains": [
            "Data Scientist",
            "Data Analyst",
            "Machine Learning Engineer"
        ],
        "description": "Data science concepts and analytical methods for engineering applications."
    },

    {
        "name": "Principles of Cloud Computing",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & Data Engineering"
        ],
        "skills": [
            "Cloud Computing",
            "AWS",
            "Azure",
            "GCP",
            "Cloud Architecture"
        ],
        "career_domains": [
            "Cloud Engineer",
            "Machine Learning Engineer",
            "DevOps Engineer",
            "Software Engineer"
        ],
        "description": "Fundamentals of cloud platforms, services and cloud-based architectures."
    },

    {
        "name": "Parallel and Distributed Computing",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & Data Engineering"
        ],
        "skills": [
            "Distributed Computing",
            "Parallel Computing",
            "Concurrency",
            "High Performance Computing"
        ],
        "career_domains": [
            "Software Engineer",
            "Cloud Engineer",
            "Data Engineer"
        ],
        "description": "Parallel processing and distributed computing architectures."
    },

    {
        "name": "Distributed Computing Systems",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT"
        ],
        "skills": [
            "Distributed Systems",
            "System Architecture",
            "Cloud Computing",
            "Scalability"
        ],
        "career_domains": [
            "Software Engineer",
            "Cloud Engineer",
            "Backend Engineer"
        ],
        "description": "Design and operation of distributed software systems."
    },

    {
        "name": "Open Source Programming",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT"
        ],
        "skills": [
            "Git",
            "GitHub",
            "Open Source",
            "Software Development"
        ],
        "career_domains": [
            "Software Engineer",
            "DevOps Engineer",
            "Open Source Developer"
        ],
        "description": "Development practices and collaboration in open-source software ecosystems."
    },

    {
        "name": "Applied Linear Algebra",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & Data Engineering",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Linear Algebra",
            "Mathematics",
            "Optimization",
            "Machine Learning Foundations"
        ],
        "career_domains": [
            "Machine Learning Engineer",
            "Data Scientist",
            "AI Researcher"
        ],
        "description": "Applied mathematical foundations useful for computing, optimization and machine learning."
    },

    # ============================================================
    # CORE COMPUTER SCIENCE
    # ============================================================

    {
        "name": "Data Structures and Algorithms",
        "code": "BCSE202L",
        "type": "Core Course",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & ML",
            "B.Tech CSE - AI & Data Engineering",
            "B.Tech CSE - Cyber Security"
        ],
        "skills": [
            "Data Structures",
            "Algorithms",
            "Problem Solving",
            "C++",
            "Python"
        ],
        "career_domains": [
            "Software Engineer",
            "Backend Engineer",
            "AI Engineer"
        ],
        "description": "Fundamental data structures and algorithmic problem solving."
    },

    {
        "name": "Database Systems",
        "code": "BACSE202",
        "type": "Core Course",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & ML",
            "B.Tech CSE - AI & Data Engineering"
        ],
        "skills": [
            "SQL",
            "Database Management",
            "Data Modelling",
            "Relational Databases"
        ],
        "career_domains": [
            "Data Engineer",
            "Backend Engineer",
            "Software Engineer"
        ],
        "description": "Database design, SQL and management of structured data."
    },

    {
        "name": "Computer Networks",
        "type": "Core Course",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - Cyber Security",
            "B.Tech ECE",
            "B.Tech EIE"
        ],
        "skills": [
            "Computer Networks",
            "TCP/IP",
            "Networking",
            "Network Security"
        ],
        "career_domains": [
            "Network Engineer",
            "Cyber Security Engineer",
            "Cloud Engineer"
        ],
        "description": "Computer networking concepts, protocols and communication architectures."
    },

    {
        "name": "Software Engineering",
        "type": "Core Course",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - AI & ML",
            "B.Tech CSE - Cyber Security"
        ],
        "skills": [
            "Software Engineering",
            "System Design",
            "Testing",
            "Software Development"
        ],
        "career_domains": [
            "Software Engineer",
            "Backend Engineer",
            "Product Engineer"
        ],
        "description": "Software development methodologies, engineering practices and system development."
    },

    # ============================================================
    # IT / AI & DATA ENGINEERING
    # ============================================================

    {
        "name": "Foundations of Data Engineering",
        "type": "Programme Course",
        "school": "SCORE",
        "eligible_programmes": [
            "B.Tech CSE - AI & Data Engineering",
            "B.Tech IT"
        ],
        "skills": [
            "Data Engineering",
            "ETL",
            "Data Pipelines",
            "Databases"
        ],
        "career_domains": [
            "Data Engineer",
            "Machine Learning Engineer",
            "Cloud Engineer"
        ],
        "description": "Foundations of data engineering, pipelines and data processing systems."
    },

    {
        "name": "Data Visualization and Analytics",
        "type": "Programme Course",
        "school": "SCORE",
        "eligible_programmes": [
            "B.Tech CSE - AI & Data Engineering",
            "B.Tech IT"
        ],
        "skills": [
            "Data Visualization",
            "Data Analytics",
            "Python",
            "Statistics"
        ],
        "career_domains": [
            "Data Scientist",
            "Data Analyst",
            "Business Intelligence Engineer"
        ],
        "description": "Data analysis and visualization techniques for extracting insights."
    },

    {
        "name": "Generative AI and Large Language Models",
        "type": "Programme Course",
        "school": "SCORE",
        "eligible_programmes": [
            "B.Tech CSE - AI & Data Engineering",
            "B.Tech CSE - AI & ML"
        ],
        "skills": [
            "Generative AI",
            "LLMs",
            "Prompt Engineering",
            "AI Agents",
            "NLP"
        ],
        "career_domains": [
            "Generative AI Engineer",
            "AI Engineer",
            "ML Engineer"
        ],
        "description": "Modern generative AI and large language model concepts and applications."
    },

    # ============================================================
    # CYBER SECURITY
    # ============================================================

    {
        "name": "Information Security Analysis and Audit",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - Cyber Security"
        ],
        "skills": [
            "Information Security",
            "Security Auditing",
            "Risk Analysis",
            "Cyber Security"
        ],
        "career_domains": [
            "Cyber Security Engineer",
            "Security Analyst",
            "Security Auditor"
        ],
        "description": "Security analysis, auditing and assessment of information systems."
    },

    {
        "name": "Information Security Management",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech CSE - Cyber Security"
        ],
        "skills": [
            "Cyber Security",
            "Security Management",
            "Risk Management",
            "Information Assurance"
        ],
        "career_domains": [
            "Cyber Security Engineer",
            "Security Analyst",
            "Security Manager"
        ],
        "description": "Management principles and practices for securing information systems."
    },

    # ============================================================
    # EIE / EEE / ELECTRICAL & COMPUTER
    # ============================================================

    {
        "name": "Neural Network and Fuzzy Control",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Electrical and Computer Engineering"
        ],
        "skills": [
            "Neural Networks",
            "Fuzzy Logic",
            "Control Systems",
            "Artificial Intelligence"
        ],
        "career_domains": [
            "Control Engineer",
            "AI Engineer",
            "Robotics Engineer"
        ],
        "description": "Intelligent control techniques using neural networks and fuzzy systems."
    },

    {
        "name": "Advanced Control Theory",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Electrical and Computer Engineering"
        ],
        "skills": [
            "Control Systems",
            "Advanced Control",
            "System Modelling",
            "Automation"
        ],
        "career_domains": [
            "Control Engineer",
            "Automation Engineer",
            "Robotics Engineer"
        ],
        "description": "Advanced mathematical and computational techniques for control systems."
    },

    {
        "name": "Digital Control Systems",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Electrical and Computer Engineering"
        ],
        "skills": [
            "Digital Control",
            "Control Systems",
            "Microcontrollers",
            "Automation"
        ],
        "career_domains": [
            "Control Engineer",
            "Automation Engineer",
            "Embedded Engineer"
        ],
        "description": "Digital implementation of control systems and controllers."
    },

    {
        "name": "Robotics and Control",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Electrical and Computer Engineering",
            "B.Tech ECE"
        ],
        "skills": [
            "Robotics",
            "Control Systems",
            "Sensors",
            "Automation"
        ],
        "career_domains": [
            "Robotics Engineer",
            "Automation Engineer",
            "Control Engineer"
        ],
        "description": "Robotic systems, sensing, modelling and control."
    },

    {
        "name": "Embedded System Design",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech ECE",
            "B.Tech Electrical and Computer Engineering"
        ],
        "skills": [
            "Embedded Systems",
            "Microcontrollers",
            "C/C++",
            "Hardware Programming"
        ],
        "career_domains": [
            "Embedded Engineer",
            "IoT Engineer",
            "Firmware Engineer"
        ],
        "description": "Design and development of embedded computing systems."
    },

    {
        "name": "FPGA Design",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech ECE",
            "B.Tech Electrical and Computer Engineering"
        ],
        "skills": [
            "FPGA",
            "Digital Design",
            "Verilog",
            "Hardware Design"
        ],
        "career_domains": [
            "FPGA Engineer",
            "VLSI Engineer",
            "Embedded Engineer"
        ],
        "description": "Digital system implementation and hardware design using FPGA platforms."
    },

    {
        "name": "IoT Fundamentals",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech ECE",
            "B.Tech Electrical and Computer Engineering",
            "B.Tech CSE"
        ],
        "skills": [
            "IoT",
            "Sensors",
            "Embedded Systems",
            "Networking"
        ],
        "career_domains": [
            "IoT Engineer",
            "Embedded Engineer",
            "Automation Engineer"
        ],
        "description": "Internet of Things architectures, sensors, connectivity and applications."
    },

    {
        "name": "Virtual Instrumentation",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech ECE"
        ],
        "skills": [
            "Instrumentation",
            "LabVIEW",
            "Data Acquisition",
            "Automation"
        ],
        "career_domains": [
            "Instrumentation Engineer",
            "Automation Engineer",
            "Test Engineer"
        ],
        "description": "Computer-based instrumentation, measurement and automation systems."
    },

    # ============================================================
    # COMMON CROSS-DISCIPLINARY
    # ============================================================

    {
        "name": "Internet of Things",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech IT",
            "B.Tech ECE",
            "B.Tech EIE",
            "B.Tech EEE"
        ],
        "skills": [
            "IoT",
            "Sensors",
            "Networking",
            "Cloud Computing",
            "Embedded Systems"
        ],
        "career_domains": [
            "IoT Engineer",
            "Embedded Engineer",
            "Cloud Engineer"
        ],
        "description": "Internet of Things technologies connecting sensing, computing and communication systems."
    },

    {
        "name": "Robotics and its Applications",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech ECE",
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Mechanical"
        ],
        "skills": [
            "Robotics",
            "Programming",
            "Sensors",
            "Automation",
            "Control"
        ],
        "career_domains": [
            "Robotics Engineer",
            "Automation Engineer",
            "AI Engineer"
        ],
        "description": "Robotics concepts and applications integrating software, sensing and control."
    },

    {
        "name": "Microprocessor and Interfacing",
        "type": "Programme Elective",
        "school": "SCOPE",
        "eligible_programmes": [
            "B.Tech CSE",
            "B.Tech ECE",
            "B.Tech EIE",
            "B.Tech EEE"
        ],
        "skills": [
            "Microprocessors",
            "Embedded Systems",
            "Hardware Interfacing",
            "C/C++"
        ],
        "career_domains": [
            "Embedded Engineer",
            "Firmware Engineer",
            "Electronics Engineer"
        ],
        "description": "Microprocessor architecture, interfacing and embedded hardware concepts."
    },

    {
        "name": "Engineering Optimization",
        "type": "Programme Elective",
        "school": "SELECT",
        "eligible_programmes": [
            "B.Tech EIE",
            "B.Tech EEE",
            "B.Tech Mechanical",
            "B.Tech Civil",
            "B.Tech CSE"
        ],
        "skills": [
            "Optimization",
            "Mathematics",
            "Numerical Methods",
            "Problem Solving"
        ],
        "career_domains": [
            "Data Scientist",
            "Control Engineer",
            "Operations Research Engineer"
        ],
        "description": "Optimization methods applied to engineering design and decision making."
    }
]


def build_database():

    os.makedirs("data", exist_ok=True)

    database = {
        "source": "VIT Official Academic Information",
        "institution": "VIT Vellore",
        "last_verified": LAST_VERIFIED,
        "database_type": "Curated VIT-wide undergraduate course database",
        "note": (
            "This is a curated current course/elective seed for the "
            "SkillGap Navigator hackathon prototype. Course availability "
            "and eligibility should be rechecked against the student's "
            "current semester curriculum before actual registration."
        ),
        "courses": courses
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)

    print("=" * 60)
    print("             VIT COURSE DATABASE")
    print("=" * 60)

    print(f"✓ Saved {len(courses)} courses")
    print(f"✓ File: {OUTPUT_FILE}")

    print("=" * 60)
    print("Courses detected:")

    for i, course in enumerate(courses, 1):
        print(
            f"{i:02d}. {course['name']} "
            f"→ {course['school']}"
        )

    print("=" * 60)


if __name__ == "__main__":
    build_database()