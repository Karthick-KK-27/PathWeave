import json
from featherless_client import client, MODEL


def analyze_skill_gap(student_profile, career_requirements, job_market):

    prompt = f"""
You are the Skill Gap Analysis Agent for SkillGap Navigator.

Compare the student's current profile with:

1. General career requirements
2. Real job-market requirements

Identify:

- skills the student already has
- skills the student partially knows
- skills the student is missing
- priority of missing skills
- why each missing skill matters
- practical actions to close each gap

================ STUDENT PROFILE ================

{json.dumps(student_profile, indent=2)}

================ CAREER REQUIREMENTS ================

{json.dumps(career_requirements, indent=2)}

================ REAL JOB MARKET ================

{json.dumps(job_market, indent=2)}

====================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "target_role": "Machine Learning Engineer",

    "matched_skills": [],

    "partial_skills": [],

    "missing_skills": [
        {{
            "skill": "",
            "priority": "High",
            "reason": "",
            "recommended_action": ""
        }}
    ],

    "overall_gap_summary": "",

    "top_three_priorities": []
}}

Rules:

- Only mark a skill as matched if it exists in the student profile.
- Treat Basic knowledge as partial knowledge when appropriate.
- Prioritize skills repeatedly requested by employers.
- Priorities must be High, Medium, or Low.
- Recommendations must be realistic for an undergraduate student.
- Do not invent requirements.
- Keep the response concise.
- Return ONLY the JSON object.
- Do not use markdown.
- Do not explain your reasoning.
"""


    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a structured career analysis agent. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1,
           max_tokens=2500,

# Disable Qwen thinking mode
extra_body={
    "chat_template_kwargs": {
        "enable_thinking": False
    }
}
        )


        # -----------------------------------------
        # GET MODEL RESPONSE
        # -----------------------------------------

        message = response.choices[0].message

        result = message.content


        # -----------------------------------------
        # EMPTY RESPONSE CHECK
        # -----------------------------------------

        if not result:

            return {
                "error": "AI returned an empty response.",
                "finish_reason": response.choices[0].finish_reason
            }


        # -----------------------------------------
        # CLEAN RESPONSE
        # -----------------------------------------

        result = result.strip()


        # Remove markdown fences if model accidentally adds them

        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]


        if result.endswith("```"):
            result = result[:-3]


        result = result.strip()


        # -----------------------------------------
        # CONVERT TO JSON
        # -----------------------------------------

        parsed_result = json.loads(result)

        return parsed_result


    except json.JSONDecodeError:

        return {
            "error": "AI returned invalid JSON.",
            "raw_response": result
        }


    except Exception as e:

        return {
            "error": f"AI request failed: {str(e)}"
        }



# ==================================================
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":


    # -----------------------------------------
    # STUDENT PROFILE
    # -----------------------------------------

    student_profile = {

        "education": "Undergraduate Engineering Student",

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


    # -----------------------------------------
    # CAREER REQUIREMENTS
    # -----------------------------------------

    career_requirements = {

        "target_role": "Machine Learning Engineer",

        "required_skills": [
            "Python",
            "Machine Learning",
            "Algorithms and Data Structures",
            "Data Preprocessing",
            "Statistics"
        ],

        "preferred_skills": [
            "Deep Learning",
            "NLP",
            "Computer Vision",
            "Docker",
            "Cloud Computing",
            "MLOps"
        ],

        "tools_and_technologies": [
            "PyTorch",
            "TensorFlow",
            "Scikit-learn",
            "NumPy",
            "Pandas",
            "Git"
        ]
    }


    # -----------------------------------------
    # REAL JOB MARKET
    # -----------------------------------------

    job_market = {

        "target_role": "Machine Learning Engineer",

        "jobs_analyzed": 17,

        "most_requested_skills": [
            "Python",
            "AI/ML Engineering",
            "LLM Integration",
            "Agent Architecture",
            "Data Engineering",
            "Cloud Infrastructure",
            "API Development",
            "System Architecture",
            "Production Deployment",
            "Remote Work"
        ],

        "most_requested_tools": [
            "AWS/GCP/Azure",
            "Kubernetes",
            "Airflow",
            "Databricks",
            "Snowflake",
            "Temporal",
            "Python",
            "SQL",
            "Git",
            "Docker"
        ],

        "common_requirements": [
            "Production AI/ML experience",
            "Ability to work independently",
            "Production deployment",
            "Understanding of AI tradeoffs",
            "Client-facing communication"
        ],

        "entry_level_signals": [
            "No junior positions listed",
            "Production experience is commonly required",
            "Experienced engineers are preferred"
        ]
    }


    # -----------------------------------------
    # START
    # -----------------------------------------

    print("\n")
    print("==============================================")
    print("       SKILLGAP NAVIGATOR")
    print("          SKILL GAP ANALYZER")
    print("==============================================")


    print("\nStudent:")
    print("Undergraduate Engineering Student")


    print("\nTarget Role:")
    print("Machine Learning Engineer")


    print("\nAnalyzing student skill gap...")


    print("\nComparing:")
    print("  -> Student skills")
    print("  -> Career requirements")
    print("  -> Real job-market requirements")


    # -----------------------------------------
    # RUN AI ANALYSIS
    # -----------------------------------------

    result = analyze_skill_gap(
        student_profile,
        career_requirements,
        job_market
    )


    # -----------------------------------------
    # DISPLAY FINAL RESULT
    # -----------------------------------------

    print("\n")
    print("========== SKILL GAP ANALYSIS ==========")
    print()


    print(json.dumps(result, indent=4))


    print("\n========================================")