from app.services.embedding_similarity import calculate_embedding_similarity
from app.services.pdf_reader import extract_text_from_pdf
from app.services.score_engine import calculate_final_score
from app.services.section_extractor import extract_sections
from app.services.skill_evidence_analyzer import analyze_skill_evidence
from app.services.skill_extractor import extract_skills
from app.services.skill_matcher import match_skills
from app.services.suggestion_engine import generate_suggestions


def analyze_resume_against_job(resume_file, job_description: str, filename: str):
    resume_text = extract_text_from_pdf(resume_file)

    if not resume_text.strip():
        raise ValueError("Could not extract text from the uploaded resume PDF.")

    if not job_description.strip():
        raise ValueError("Job description is required.")

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    skill_match = match_skills(
        resume_skills=resume_skills,
        jd_skills=jd_skills
    )

    similarity_score = calculate_embedding_similarity(
        resume_text=resume_text,
        jd_text=job_description
    )

    ats_score = calculate_final_score(
        similarity_score=similarity_score,
        skill_match_score=skill_match["skill_match_score"],
        bonus_skill_count=len(skill_match["bonus_skills"])
    )

    sections = extract_sections(resume_text)
    skill_evidence = analyze_skill_evidence(
        sections=sections,
        resume_skills=resume_skills
    )

    suggestions = generate_suggestions(
        skill_match["missing_skills"]
    )

    return {
    "filename": filename,
    "ats_score": ats_score,
    "similarity_score": similarity_score,
    "skill_match_score": skill_match["skill_match_score"],

    "resume_skills": resume_skills,
    "job_description_skills": jd_skills,

    "matched_skills": skill_match["matched_skills"],
    "missing_skills": skill_match["missing_skills"],
    "bonus_skills": skill_match["bonus_skills"],

    "skill_evidence": skill_evidence,
    "suggestions": suggestions,

    # NEW
    "projects_text": sections["projects"],
    "experience_text": sections["experience"],
    "job_description": job_description
    }
