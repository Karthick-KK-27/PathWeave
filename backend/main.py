from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import app_graph
from agents.student_profile import profile_node
from schemas import PathState

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    target_job: str
    resume_text: str

@app.post("/api/plan")
def generate_plan(req: PlanRequest):
    try:
        state: PathState = {
            "target_job": req.target_job,
            "job_requirements": {},
            "student_profile": {},
            "skill_gaps": [],
            "recommendations": []
        }
        state = profile_node(state, req.resume_text)
        result = app_graph.invoke(state)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/health")
def health():
    return {"status": "ok"}