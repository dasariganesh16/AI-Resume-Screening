from pydantic import BaseModel


class SkillEvidence(BaseModel):
    strong: list[str]
    moderate: list[str]
    limited: list[str]


class AnalysisResponse(BaseModel):
    filename: str
    ats_score: float
    similarity_score: float
    skill_match_score: float
    resume_skills: list[str]
    job_description_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    bonus_skills: list[str]
    skill_evidence: SkillEvidence
    suggestions: list[str]
    projects_text: str
    experience_text: str
    job_description: str
