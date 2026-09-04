from typing import TypedDict, List, Optional

class JobRequirements(TypedDict):
    role: str
    company: Optional[str]
    required_skills: List[str]
    preferred_skills: List[str]
    seniority: str

class StudentProfile(TypedDict):
    name: str
    current_skills: List[str]
    completed_courses: List[str]
    projects: List[str]

class SkillGap(TypedDict):
    skill: str
    severity: str
    reason: str

class Recommendation(TypedDict):
    title: str
    type: str
    gaps_covered: List[str]
    reasoning: str
    leverage_score: float

class PathState(TypedDict):
    target_job: str
    job_requirements: JobRequirements
    student_profile: StudentProfile
    skill_gaps: List[SkillGap]
    recommendations: List[Recommendation]