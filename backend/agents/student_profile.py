import json
from llm_client import call_llm
from schemas import PathState

PROFILE_SYSTEM_PROMPT = """You extract a structured skill profile from a student's 
resume, transcript, or project description text. Be generous in recognizing skills 
that are implied.

Respond with ONLY valid JSON in this exact shape, no other text:
{
  "name": "string (or 'Student' if not given)",
  "current_skills": ["skill1", "skill2"],
  "completed_courses": ["course1"],
  "projects": ["short project description"]
}"""

def profile_node(state: PathState, raw_resume_text: str) -> PathState:
    result = call_llm(PROFILE_SYSTEM_PROMPT, raw_resume_text)
    cleaned = result.strip().strip("```json").strip("```").strip()
    state["student_profile"] = json.loads(cleaned)
    return state