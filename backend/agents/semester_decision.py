import json
from llm_client import call_llm
from schemas import PathState

DECISION_SYSTEM_PROMPT = """You are a semester-planning advisor. Given a student's 
prioritized skill gaps and a list of available electives, clubs, and projects, 
select the 3 BEST options this student should pursue this semester.

Rank by LEVERAGE: prefer options that close multiple important gaps over options 
that close only one gap. Write specific reasoning referencing the actual gaps closed.

Respond with ONLY valid JSON, a list in this exact shape, no other text:
[
  {"title": "string", "type": "elective | club | project", "gaps_covered": ["skill1"], "reasoning": "specific explanation", "leverage_score": 0.0}
]"""

def decision_node(state: PathState, campus_options: dict) -> PathState:
    payload = {
        "skill_gaps": state["skill_gaps"],
        "campus_options": campus_options
    }
    result = call_llm(DECISION_SYSTEM_PROMPT, json.dumps(payload))
    cleaned = result.strip().strip("```json").strip("```").strip()
    state["recommendations"] = json.loads(cleaned)
    return state