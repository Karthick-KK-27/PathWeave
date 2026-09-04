import json
import os
import re


# ============================================================
# SKILLGAP NAVIGATOR
# VIT OPPORTUNITY RECOMMENDER
# VERSION 4 - ELIGIBILITY FIRST
# ============================================================

DATA_DIR = "data"

COURSES_FILE = os.path.join(DATA_DIR, "vit_courses.json")
CLUBS_FILE = os.path.join(DATA_DIR, "vit_clubs.json")
CHAPTERS_FILE = os.path.join(DATA_DIR, "vit_chapters.json")
TEAMS_FILE = os.path.join(DATA_DIR, "vit_teams.json")


# ============================================================
# LOAD JSON
# ============================================================

def load_json_file(filename):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"WARNING: File not found -> {filename}")
        return {}

    except json.JSONDecodeError:
        print(f"WARNING: Invalid JSON -> {filename}")
        return {}


# ============================================================
# LOAD ALL VIT OPPORTUNITIES
# ============================================================

def load_vit_opportunities():

    courses = load_json_file(COURSES_FILE)
    clubs = load_json_file(CLUBS_FILE)
    chapters = load_json_file(CHAPTERS_FILE)
    teams = load_json_file(TEAMS_FILE)

    opportunities = []

    for item in courses.get("courses", []):
        opportunity = dict(item)
        opportunity["opportunity_type"] = "Course"
        opportunities.append(opportunity)

    for item in clubs.get("clubs", []):
        opportunity = dict(item)
        opportunity["opportunity_type"] = "Club"
        opportunities.append(opportunity)

    for item in chapters.get("chapters", []):
        opportunity = dict(item)
        opportunity["opportunity_type"] = "Chapter"
        opportunities.append(opportunity)

    for item in teams.get("teams", []):
        opportunity = dict(item)
        opportunity["opportunity_type"] = "Team"
        opportunities.append(opportunity)

    return opportunities


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):

    text = str(text).lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# PROGRAMME NORMALIZATION
# ============================================================

PROGRAMME_ALIASES = {

    "b.tech eie": [
        "b.tech eie",
        "eie",
        "electronics and instrumentation engineering"
    ],

    "b.tech eee": [
        "b.tech eee",
        "eee",
        "electrical and electronics engineering"
    ],

    "b.tech ece": [
        "b.tech ece",
        "ece",
        "electronics and communication engineering"
    ],

    "b.tech cse": [
        "b.tech cse",
        "cse",
        "computer science and engineering"
    ],

    "b.tech it": [
        "b.tech it",
        "it",
        "information technology"
    ],

    "b.tech cse - ai & ml": [
        "b.tech cse - ai & ml",
        "cse ai ml",
        "cse - ai & ml",
        "ai & ml"
    ],

    "b.tech cse - ai & data engineering": [
        "b.tech cse - ai & data engineering",
        "cse ai data engineering",
        "ai & data engineering"
    ],

    "b.tech cse - cyber security": [
        "b.tech cse - cyber security",
        "cse cyber security",
        "cyber security"
    ]
}


def normalize_programme(programme):

    value = normalize(programme)

    for canonical, aliases in PROGRAMME_ALIASES.items():

        for alias in aliases:

            if value == normalize(alias):
                return canonical

    return value


# ============================================================
# ELIGIBILITY CHECK
# ============================================================

def is_programme_eligible(
    opportunity,
    student_programme
):

    eligible = opportunity.get(
        "eligible_programmes",
        []
    )

    # If no programme restriction exists,
    # treat it as open to the student.

    if not eligible:
        return True


    student = normalize_programme(
        student_programme
    )


    normalized_eligible = [

        normalize_programme(programme)

        for programme in eligible

    ]


    # Exact programme match

    if student in normalized_eligible:
        return True


    return False


# ============================================================
# YEAR ELIGIBILITY
# ============================================================

def is_year_eligible(
    opportunity,
    student_year
):

    constraints = opportunity.get(
        "year_constraints",
        []
    )

    # No year restriction

    if not constraints:
        return True


    if isinstance(
        constraints,
        str
    ):

        constraints = [constraints]


    year_text = str(
        student_year
    )


    for constraint in constraints:

        constraint_text = normalize(
            constraint
        )

        # Examples:
        # "2"
        # "2nd year"
        # "2nd"
        # "2,3,4"

        if year_text in constraint_text:
            return True

        if f"{year_text}nd year" in constraint_text:
            return True

        if f"{year_text}rd year" in constraint_text:
            return True

        if f"{year_text}th year" in constraint_text:
            return True


    return False


# ============================================================
# COMPLETE ELIGIBILITY CHECK
# ============================================================

def is_eligible(
    opportunity,
    student_profile
):

    programme = student_profile.get(
        "programme",
        ""
    )

    year = student_profile.get(
        "year",
        None
    )


    # Programme check

    if programme:

        if not is_programme_eligible(
            opportunity,
            programme
        ):

            return False


    # Year check

    if year is not None:

        if not is_year_eligible(
            opportunity,
            year
        ):

            return False


    return True


# ============================================================
# CONTROLLED SKILL MAPPING
# ============================================================

VIT_SKILL_MAP = {

    # ---------------- COURSES ----------------

    "machine learning": [
        "Machine Learning"
    ],

    "deep learning": [
        "Deep Learning Frameworks"
    ],

    "machine vision": [
        "Computer Vision"
    ],

    "explainable artificial intelligence": [
        "Machine Learning"
    ],

    "speech and language processing": [
        "NLP"
    ],

    "natural language processing": [
        "NLP"
    ],

    "artificial intelligence": [
        "Machine Learning"
    ],

    "principles of cloud computing": [
        "Cloud Infrastructure"
    ],

    "foundations of data engineering": [
        "Data Engineering and Preprocessing"
    ],

    "data science for engineers": [
        "Data Engineering and Preprocessing"
    ],

    "open source programming": [
        "System Architecture"
    ],

    "parallel and distributed computing": [
        "System Architecture"
    ],

    "distributed computing systems": [
        "System Architecture"
    ],

    "internet of things": [
        "IoT"
    ],

    "iot": [
        "IoT"
    ],

    "robotics and its applications": [
        "Robotics"
    ],

    "microprocessor and interfacing": [
        "Embedded Systems"
    ],

    "embedded system design": [
        "Embedded Systems"
    ],

    "fpga design": [
        "Embedded Systems"
    ],

    "neural network and fuzzy control": [
        "Control Systems",
        "Machine Learning"
    ],

    "digital control systems": [
        "Control Systems"
    ],

    "advanced control theory": [
        "Control Systems"
    ],

    "robotics and control": [
        "Robotics",
        "Control Systems"
    ],

    "virtual instrumentation": [
        "Control Systems"
    ],


    # ---------------- CLUBS ----------------

    "the ai & ml club": [
        "Machine Learning",
        "Deep Learning Frameworks"
    ],

    "ai & ml club": [
        "Machine Learning",
        "Deep Learning Frameworks"
    ],

    "developers student club": [
        "REST API Development",
        "System Architecture"
    ],

    "linux user's group": [
        "Cloud Infrastructure",
        "System Architecture"
    ],

    "iotthinc": [
        "IoT"
    ],

    "robovitics": [
        "Robotics",
        "Embedded Systems"
    ],


    # ---------------- TEAMS ----------------

    "projects-lab": [
        "Machine Learning",
        "Robotics",
        "Embedded Systems"
    ],

    "team-vauv": [
        "Robotics",
        "Embedded Systems"
    ]
}


# ============================================================
# GET OPPORTUNITY SKILLS
# ============================================================

def get_opportunity_skills(
    opportunity
):

    name = normalize(
        opportunity.get(
            "name",
            ""
        )
    )


    # First use our explicit mapping

    if name in VIT_SKILL_MAP:

        return VIT_SKILL_MAP[name]


    # Otherwise use structured skill field

    skills = opportunity.get(
        "skills",
        []
    )


    if isinstance(
        skills,
        str
    ):

        skills = [skills]


    return list(
        dict.fromkeys(
            skills
        )
    )


# ============================================================
# MATCH SKILL GAPS
# ============================================================

def calculate_skill_match(
    opportunity,
    missing_skills
):

    opportunity_skills = get_opportunity_skills(
        opportunity
    )


    matched = []


    for gap in missing_skills:

        skill = gap.get(
            "skill",
            ""
        )


        if skill in opportunity_skills:

            matched.append(
                skill
            )


    return matched


# ============================================================
# SCORE
# ============================================================

def score_opportunity(
    opportunity,
    missing_skills
):

    matched = calculate_skill_match(
        opportunity,
        missing_skills
    )


    if not matched:

        return 0, []


    score = 0


    # Skill-gap coverage

    score += (
        len(matched) * 50
    )


    # Opportunity type

    opportunity_type = opportunity.get(
        "opportunity_type",
        ""
    )


    if opportunity_type == "Course":

        score += 30

    elif opportunity_type == "Team":

        score += 25

    elif opportunity_type == "Club":

        score += 20

    elif opportunity_type == "Chapter":

        score += 10


    # High priority gap

    for gap in missing_skills:

        if gap.get(
            "skill"
        ) in matched:

            if gap.get(
                "priority"
            ) == "High":

                score += 20


    return score, matched


# ============================================================
# RECOMMENDATIONS
# ============================================================

def recommend_vit_opportunities(

    student_profile,
    gap_analysis,
    target_role,
    top_n=10

):

    all_opportunities = (
        load_vit_opportunities()
    )


    missing_skills = (
        gap_analysis.get(
            "missing_skills",
            []
        )
    )


    # ========================================================
    # STEP 1: FILTER ELIGIBILITY FIRST
    # ========================================================

    eligible_opportunities = []


    for opportunity in all_opportunities:

        if is_eligible(
            opportunity,
            student_profile
        ):

            eligible_opportunities.append(
                opportunity
            )


    print(
        f"\nTotal VIT opportunities: "
        f"{len(all_opportunities)}"
    )

    print(
        f"Eligible for student: "
        f"{len(eligible_opportunities)}"
    )


    # ========================================================
    # STEP 2: SKILL MATCH ONLY AFTER ELIGIBILITY
    # ========================================================

    ranked = []


    for opportunity in eligible_opportunities:

        score, matched = (
            score_opportunity(
                opportunity,
                missing_skills
            )
        )


        if not matched:
            continue


        ranked.append({

            "name":
                opportunity.get(
                    "name",
                    "Unknown"
                ),

            "type":
                opportunity.get(
                    "opportunity_type",
                    "Unknown"
                ),

            "school":
                opportunity.get(
                    "school",
                    ""
                ),

            "score":
                score,

            "skills_addressed":
                matched,

            "eligible_programmes":
                opportunity.get(
                    "eligible_programmes",
                    []
                ),

            "year_constraints":
                opportunity.get(
                    "year_constraints",
                    []
                ),

            "description":
                opportunity.get(
                    "description",
                    ""
                ),

            "source_url":
                opportunity.get(
                    "source_url",
                    ""
                )

        })


    # ========================================================
    # SORT
    # ========================================================

    ranked.sort(

        key=lambda item:
            item["score"],

        reverse=True

    )


    # ========================================================
    # TOP N
    # ========================================================

    recommendations = []


    for rank, item in enumerate(

        ranked[:top_n],

        start=1

    ):

        item["rank"] = rank

        recommendations.append(
            item
        )


    return recommendations


# ============================================================
# DISPLAY
# ============================================================

def display_recommendations(
    recommendations
):

    print("\n")

    print("=" * 70)

    print(
        "       VIT OPPORTUNITY RECOMMENDATIONS"
    )

    print("=" * 70)


    if not recommendations:

        print(
            "\nNo suitable VIT opportunities found."
        )

        return


    for item in recommendations:

        print()

        print(
            f"#{item['rank']} "
            f"{item['name']}"
        )

        print(
            f"   Type: "
            f"{item['type']}"
        )


        if item["school"]:

            print(
                f"   School: "
                f"{item['school']}"
            )


        print(
            f"   Score: "
            f"{item['score']}"
        )


        print(
            "   Addresses: "
            + ", ".join(
                item[
                    "skills_addressed"
                ]
            )
        )


        if item[
            "eligible_programmes"
        ]:

            print(
                "   Eligible: "
                + ", ".join(
                    item[
                        "eligible_programmes"
                    ]
                )
            )


# ============================================================
# TEST STUDENT
# ============================================================

if __name__ == "__main__":

    student_profile = {

        "name":
            "Test Student",

        "programme":
            "B.Tech EIE",

        "year":
            2,

        "education":
            "Undergraduate Engineering Student",

        "skills": [

            "Python",
            "C++",
            "Basic SQL",
            "Basic Machine Learning",
            "Git"

        ],

        "projects": [

            "Student Attendance System",
            "Basic Image Classification Project"

        ]

    }


    gap_analysis = {

        "missing_skills": [

            {
                "skill":
                    "Cloud Infrastructure",

                "priority":
                    "High"
            },

            {
                "skill":
                    "Data Engineering and Preprocessing",

                "priority":
                    "High"
            },

            {
                "skill":
                    "Deep Learning Frameworks",

                "priority":
                    "High"
            },

            {
                "skill":
                    "REST API Development",

                "priority":
                    "Medium"
            },

            {
                "skill":
                    "Docker",

                "priority":
                    "Medium"
            }

        ]

    }


    target_role = (
        "Machine Learning Engineer"
    )


    recommendations = (
        recommend_vit_opportunities(

            student_profile,

            gap_analysis,

            target_role,

            top_n=10

        )
    )


    display_recommendations(
        recommendations
    )