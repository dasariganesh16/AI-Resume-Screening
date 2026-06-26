from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Resume Screening AI API",
        "version": "1.0.0"
    }
