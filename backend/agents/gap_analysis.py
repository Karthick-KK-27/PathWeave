import json
from llm_client import call_llm
from schemas import PathState

GAP_SYSTEM_PROMPT = """You compare a target job's requirements against a student's 
current skill profile and identify the gaps. Assess severity based on how core the 
skill is to the role and how far the student is from having it.

Respond with ONLY valid JSON, a list in this exact shape, no other text:
[
  {"skill": "string", "severity": "critical | moderate | minor", "reason": "one sentence explanation"}
]"""

def gap_analysis_node(state: PathState) -> PathState:
    payload = {
        "job_requirements": state["job_requirements"],
        "student_profile": state["student_profile"]
    }
    result = call_llm(GAP_SYSTEM_PROMPT, json.dumps(payload))
    cleaned = result.strip().strip("```json").strip("```").strip()
    state["skill_gaps"] = json.loads(cleaned)
    return state