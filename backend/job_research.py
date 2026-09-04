import requests
import json
from featherless_client import client, MODEL


def fetch_jobs(role, limit=10):

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": role,
        "limit": limit
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    return data.get("jobs", [])


def analyze_jobs(role, jobs):

    simplified_jobs = []

    for job in jobs:
        simplified_jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("candidate_required_location"),
            "publication_date": job.get("publication_date"),
            "url": job.get("url"),
            "description": job.get("description", "")[:5000]
        })

    prompt = f"""
You are the Job Market Research Agent for SkillGap Navigator.

Target role:
{role}

Here are real job listings collected from a job board:

{json.dumps(simplified_jobs, indent=2)}

Analyze these listings and identify the most common skills and technologies
that employers are asking for.

Return ONLY valid JSON in this exact format:

{{
    "target_role": "{role}",
    "jobs_analyzed": {len(jobs)},
    "most_requested_skills": [],
    "most_requested_tools": [],
    "common_requirements": [],
    "entry_level_signals": []
}}

Focus on skills that appear repeatedly across the listings.

Do not invent information that is not supported by the job descriptions.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an AI job-market research agent. Return concise structured JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1500
    )

    result = response.choices[0].message.content

    return result


if __name__ == "__main__":

    role = input("Enter target career role: ")

    print("\nSearching real job listings...\n")

    jobs = fetch_jobs(role)

    print(f"Found {len(jobs)} job listings.")

    if not jobs:
        print("No jobs found. Try another role.")
    else:

        analysis = analyze_jobs(role, jobs)

        print("\n========== JOB MARKET ANALYSIS ==========\n")
        print(analysis)
        print("\n=========================================\n")
