from pydantic import BaseModel
from app.schemas.analysis import AnalysisResponse


class InterviewRequest(BaseModel):
    analysis: AnalysisResponse


class InterviewResponse(BaseModel):
    technical_questions: list[str]
    project_questions: list[str]
    behavioral_questions: list[str]
    hr_questions: list[str]