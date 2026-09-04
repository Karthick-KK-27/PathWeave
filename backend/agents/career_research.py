import json
from llm_client import call_llm
from schemas import PathState

RESEARCH_SYSTEM_PROMPT = """You are a career research analyst. Given a job title and 
optional company, produce the current, realistic skill requirements for that role.

Respond with ONLY valid JSON in this exact shape, no other text:
{
  "role": "string",
  "company": "string or null",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1", "skill2"],
  "seniority": "entry-level | mid-level | senior"
}

Include 5-10 required_skills and 3-6 preferred_skills. Be specific."""

def career_research_node(state: PathState) -> PathState:
    target = state["target_job"]
    result = call_llm(RESEARCH_SYSTEM_PROMPT, f"Target job: {target}")
    cleaned = result.strip().strip("```json").strip("```").strip()
    state["job_requirements"] = json.loads(cleaned)
    return state