from pydantic import BaseModel


class AdviceRequest(BaseModel):
    ats_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    strong_evidence: list[str]
    limited_evidence: list[str]
    projects_text: str = ""
    experience_text: str = ""


class InterviewReadiness(BaseModel):
    score: float
    level: str
    reason: str


class AdviceResponse(BaseModel):
    strengths: list[str]
    improvement_areas: list[str]
    learning_roadmap: list[str]
    interview_readiness: InterviewReadiness
