from fastapi import APIRouter

from app.schemas.tailor import TailorResumeRequest, TailorResumeResponse
from app.services.resume_tailor import generate_tailored_resume


router = APIRouter(
    prefix="/tailor-resume",
    tags=["Resume Tailoring"]
)


@router.post("/", response_model=TailorResumeResponse)
def tailor_resume(request: TailorResumeRequest):
    return generate_tailored_resume(
        projects_text=request.projects_text,
        experience_text=request.experience_text,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills
    )
