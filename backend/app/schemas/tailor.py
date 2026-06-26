from pydantic import BaseModel


class TailorResumeRequest(BaseModel):
    projects_text: str = ""
    experience_text: str = ""
    matched_skills: list[str]
    missing_skills: list[str]


class ResumeImprovement(BaseModel):
    original: str
    improved: str


class TailorResumeResponse(BaseModel):
    professional_summary: str
    project_improvements: list[ResumeImprovement]
    experience_improvements: list[ResumeImprovement]
    error: str | None = None
