import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.advice import router as advice_router
from app.api.v1.routes.analyze import router as api_analyze_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.interview import router as interview_router
from app.api.v1.routes.tailor import router as tailor_router
from app.api.v1.routes.report import router as report_router

load_dotenv()

frontend_url = os.getenv('FRONTEND_URL')
allowed_origins = [frontend_url] if frontend_url else ['*']

app = FastAPI(
    title="Resume Screening AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(api_analyze_router, prefix="/api/v1")
app.include_router(advice_router, prefix="/api/v1")
app.include_router(interview_router, prefix="/api/v1")
app.include_router(tailor_router, prefix="/api/v1")
app.include_router(report_router,prefix="/api/v1")

@app.get("/")
def home():
    return {
        "status": "Running",
        "message": "Resume Screening AI Backend"
    }

