def match_skills(resume_skills, jd_skills):

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched_skills = sorted(
        list(resume_set.intersection(jd_set))
    )

    missing_skills = sorted(
        list(jd_set - resume_set)
    )

    bonus_skills = sorted(
        list(resume_set - jd_set)
    )

    if len(jd_set) == 0:
        skill_match_score = 0
    else:
        skill_match_score = (
            len(matched_skills)
            / len(jd_set)
        ) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "bonus_skills": bonus_skills,
        "skill_match_score": round(skill_match_score, 2)
    }
    
    
    
if __name__ == "__main__":

    resume_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Docker",
        "Transformers",
        "RAG"
    ]

    jd_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Docker",
        "FastAPI"
    ]

    result = match_skills(
        resume_skills,
        jd_skills
    )

    print(result)