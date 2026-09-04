"""
Pathweave FastAPI backend.

Exposes POST /api/plan for the React frontend. Orchestrates the
Skill_Navigator pipeline:
    resume_text -> profile
    target_job  -> career requirements (LLM)
    target_job  -> real job listings + market analysis (Remotive + LLM)
    profile + career + market -> skill gap
    profile + gaps + role -> VIT opportunity recommendations

Response shape is mapped to what the frontend components expect:
    {
        job_requirements: { role, ... },
        skill_gaps:       [ { skill, severity: critical|moderate|minor, reason } ],
        recommendations:  [ { title, reasoning, leverage: high|medium|low } ],
        extras:           { profile, career_requirements, job_market, vit_opportunities }
    }
"""

import json
import os
import traceback
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from career_research import research_career
from job_research import analyze_jobs, fetch_jobs
from gap_analysis import analyze_skill_gap
from vit_recommender import recommend_vit_opportunities
from featherless_client import MODEL, client


# ------------------------------------------------------------------
# App + CORS
# ------------------------------------------------------------------

app = FastAPI(title="Pathweave API", version="0.2.0")

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in FRONTEND_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# Request / response models
# ------------------------------------------------------------------

class PlanRequest(BaseModel):
    target_job: str
    resume_text: str
    programme: Optional[str] = "B.Tech CSE"
    year: Optional[int] = 2
    include_job_market: bool = True


class HealthResponse(BaseModel):
    status: str
    model: str


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _parse_json_response(text: Any) -> Any:
    """LLM outputs are often wrapped in ```json fences — strip and parse."""
    if isinstance(text, (dict, list)):
        return text
    if text is None:
        return {}

    s = str(text).strip()
    if s.startswith("```json"):
        s = s[7:]
    elif s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    s = s.strip()

    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # Last-ditch: try to find the first { ... } or [ ... ] block
        for opener, closer in (("{", "}"), ("[", "]")):
            start = s.find(opener)
            end = s.rfind(closer)
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(s[start : end + 1])
                except json.JSONDecodeError:
                    continue
        return {"_raw": s}


PROFILE_SYSTEM_PROMPT = (
    "You extract a structured student profile from resume, transcript, or "
    "project-description text. Be generous when a skill is clearly implied. "
    "Respond with ONLY valid JSON, no prose, no code fences, in this shape:\n"
    "{\n"
    '  "name": "string (or Student if not given)",\n'
    '  "education": "string",\n'
    '  "skills": ["skill1", "skill2"],\n'
    '  "completed_courses": ["course1"],\n'
    '  "projects": ["short project description"]\n'
    "}"
)


def extract_profile(resume_text: str) -> Dict[str, Any]:
    """Turn free-text resume into the profile dict the pipeline expects."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROFILE_SYSTEM_PROMPT},
            {"role": "user", "content": resume_text},
        ],
        temperature=0.1,
    )
    parsed = _parse_json_response(resp.choices[0].message.content)
    if not isinstance(parsed, dict):
        parsed = {}
    parsed.setdefault("name", "Student")
    parsed.setdefault("education", "Undergraduate Engineering Student")
    parsed.setdefault("skills", [])
    parsed.setdefault("completed_courses", [])
    parsed.setdefault("projects", [])
    return parsed


# Mapping between backend priority and frontend severity
_PRIORITY_TO_SEVERITY = {
    "high": "critical",
    "medium": "moderate",
    "low": "minor",
}


def _severity_from_priority(priority: str) -> str:
    return _PRIORITY_TO_SEVERITY.get(str(priority).strip().lower(), "moderate")


def _leverage_from_score(score: float, max_score: float) -> str:
    """Bucket a numeric recommender score into high/medium/low."""
    if max_score <= 0:
        return "medium"
    ratio = score / max_score
    if ratio >= 0.66:
        return "high"
    if ratio >= 0.33:
        return "medium"
    return "low"


def _map_skill_gaps(gap_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """gap_analysis output -> frontend skill_gaps[]"""
    out: List[Dict[str, Any]] = []
    for m in gap_result.get("missing_skills", []) or []:
        if not isinstance(m, dict):
            continue
        skill = m.get("skill") or m.get("name") or ""
        if not skill:
            continue
        out.append(
            {
                "skill": skill,
                "severity": _severity_from_priority(m.get("priority", "medium")),
                "reason": m.get("reason", ""),
                "recommended_action": m.get("recommended_action", ""),
            }
        )
    return out


def _map_recommendations(vit_recs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """vit_recommender output -> frontend recommendations[]"""
    if not vit_recs:
        return []
    max_score = max((r.get("score", 0) for r in vit_recs), default=0)
    out: List[Dict[str, Any]] = []
    for r in vit_recs:
        skills = r.get("skills_addressed", []) or []
        desc = r.get("description", "") or ""
        reasoning_bits = []
        if skills:
            reasoning_bits.append("Closes: " + ", ".join(skills))
        if desc:
            reasoning_bits.append(desc)
        out.append(
            {
                "title": r.get("name", "Untitled"),
                "type": r.get("type", "Opportunity"),
                "reasoning": " — ".join(reasoning_bits) if reasoning_bits else "Recommended by the VIT opportunity ranker.",
                "leverage": _leverage_from_score(r.get("score", 0), max_score),
                "school": r.get("school", ""),
                "source_url": r.get("source_url", ""),
                "score": r.get("score", 0),
            }
        )
    return out


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model=MODEL)


@app.post("/api/plan")
def generate_plan(req: PlanRequest) -> Dict[str, Any]:
    if not req.target_job.strip():
        raise HTTPException(status_code=400, detail="target_job is required")
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="resume_text is required")

    try:
        # --- 1. Profile from resume ------------------------------------
        profile = extract_profile(req.resume_text)
        # Attach programme/year for the VIT recommender
        profile["programme"] = req.programme or "B.Tech CSE"
        profile["year"] = req.year or 2

        # --- 2. Career requirements ------------------------------------
        career_raw = research_career(req.target_job)
        career_requirements = _parse_json_response(career_raw) or {}
        if not isinstance(career_requirements, dict):
            career_requirements = {}
        # setdefault won't replace an existing but falsy (None/"") role,
        # and job_requirements.role must always be a non-empty string.
        career_requirements["role"] = str(
            career_requirements.get("role") or req.target_job
        )

        # --- 3. Real job market (optional; fails soft) -----------------
        job_market: Dict[str, Any] = {}
        if req.include_job_market:
            try:
                jobs = fetch_jobs(req.target_job)
                if jobs:
                    job_market = _parse_json_response(
                        analyze_jobs(req.target_job, jobs)
                    ) or {}
                    if not isinstance(job_market, dict):
                        job_market = {}
            except Exception as e:  # noqa: BLE001
                # Remotive down, timeout, etc. — continue without market data
                job_market = {"_error": f"job market fetch failed: {e}"}

        # --- 4. Skill gap ---------------------------------------------
        gap_result = analyze_skill_gap(profile, career_requirements, job_market)
        if not isinstance(gap_result, dict):
            gap_result = _parse_json_response(gap_result)
        if not isinstance(gap_result, dict):
            gap_result = {}

        # --- 5. VIT recommendations -----------------------------------
        try:
            vit_recs = recommend_vit_opportunities(
                profile, gap_result, req.target_job, top_n=6
            )
        except Exception as e:  # noqa: BLE001
            vit_recs = []
            gap_result.setdefault("_warnings", []).append(
                f"vit_recommender failed: {e}"
            )

        # --- 6. Map to frontend shape ---------------------------------
        return {
            "job_requirements": {
                "role": career_requirements.get("role", req.target_job),
                "required_skills": career_requirements.get("required_skills", []),
                "preferred_skills": career_requirements.get("preferred_skills", []),
                "tools_and_technologies": career_requirements.get(
                    "tools_and_technologies", []
                ),
            },
            "skill_gaps": _map_skill_gaps(gap_result),
            "recommendations": _map_recommendations(vit_recs),
            "extras": {
                "profile": profile,
                "career_requirements": career_requirements,
                "job_market": job_market,
                "gap_analysis": gap_result,
                "vit_opportunities": vit_recs,
            },
        }

    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"pipeline failed: {e}") from e
