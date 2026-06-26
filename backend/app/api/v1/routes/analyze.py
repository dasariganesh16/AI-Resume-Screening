import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import analyze_resume_against_job
from app.schemas.analysis import AnalysisResponse


router = APIRouter(
    prefix="/analyze",
    tags=["Resume Analysis"]
)


@router.post("/", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resume uploads are supported."
        )

    try:
        return analyze_resume_against_job(
            resume_file=resume.file,
            job_description=job_description,
            filename=resume.filename
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        logging.exception("Resume analysis failed")
        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed."
        ) from exc
