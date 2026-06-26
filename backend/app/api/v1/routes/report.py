from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.report import ReportRequest
from app.services.pdf_report import generate_pdf_report

router = APIRouter(
    prefix="/report",
    tags=["ATS Report"]
)


@router.post("/")
def generate_report(request: ReportRequest):

    pdf = generate_pdf_report(
        final_score=request.analysis.ats_score,

        similarity_score=request.analysis.similarity_score,

        skill_match_score=request.analysis.skill_match_score,

        matched_skills=request.analysis.matched_skills,

        missing_skills=request.analysis.missing_skills,

        bonus_skills=request.analysis.bonus_skills,

        strong_skills=request.analysis.skill_evidence.strong,

        limited_skills=request.analysis.skill_evidence.limited,

        llm_response={
            "strengths": request.advice.strengths,

            "improvement_areas": request.advice.improvement_areas,

            "learning_roadmap": request.advice.learning_roadmap,

            "interview_readiness": {
                "score": request.advice.interview_readiness.score,
                "level": request.advice.interview_readiness.level,
                "reason": request.advice.interview_readiness.reason,
            },
        },
    )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ATS_Report.pdf"
        },
    )