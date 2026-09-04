# PathWeave

**SkillGap Navigator** — an AI-powered career guidance platform that analyzes a student's profile against target job requirements and real job listings, identifies skill gaps, and recommends VIT courses, clubs, chapters and teams to close them.

## Architecture

```
frontend/   React 19 + Vite + Tailwind v4 + Recharts + axios
backend/    FastAPI + Featherless (LLM) + Remotive (job listings)
            + eligibility-first VIT opportunity recommender
```

Pipeline (per `POST /api/plan` request):

1. **Profile extraction** — resume text → structured `{skills, projects, education}`
2. **Career research** — target role → required/preferred skills, tools, entry-level expectations
3. **Job-market research** — real Remotive listings → most-requested skills and tools
4. **Skill gap** — profile vs. career + market → matched / partial / missing skills
5. **VIT recommender** — eligibility-first ranking of VIT courses, clubs, chapters, teams that close the top missing skills

## Running locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # then paste your FEATHERLESS_API_KEY into .env
uvicorn main:app --reload --port 8000
```

Sanity check: `curl http://localhost:8000/api/health` → `{"status":"ok",...}`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local          # optional, defaults to http://localhost:8000
npm run dev
```

Open http://localhost:5173.

## API

`POST /api/plan`

```json
{
  "target_job": "Machine Learning Engineer",
  "resume_text": "B.Tech CSE at VIT. Skills: Python, C++, basic ML, Git ...",
  "programme": "B.Tech CSE",
  "year": 2,
  "include_job_market": true
}
```

Response:

```json
{
  "job_requirements": { "role": "...", "required_skills": [], "preferred_skills": [], "tools_and_technologies": [] },
  "skill_gaps": [ { "skill": "Docker", "severity": "critical", "reason": "...", "recommended_action": "..." } ],
  "recommendations": [ { "title": "...", "type": "Course", "reasoning": "...", "leverage": "high", "school": "...", "source_url": "..." } ],
  "extras": { "profile": {...}, "career_requirements": {...}, "job_market": {...}, "gap_analysis": {...}, "vit_opportunities": [...] }
}
```

`GET /api/health` → `{ "status": "ok", "model": "..." }`

## Secrets

`backend/.env` is git-ignored and must never be committed. If a real Featherless key ever lands in a commit, rotate it at featherless.ai immediately.
