from pydantic import BaseModel

from app.schemas.analysis import AnalysisResponse
from app.schemas.advice import AdviceResponse


class ReportRequest(BaseModel):
    analysis: AnalysisResponse
    advice: AdviceResponse