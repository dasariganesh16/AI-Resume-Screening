def analyze_skill_evidence(
    sections,
    resume_skills
):

    strong = []
    moderate = []
    limited = []

    projects_text = sections[
        "projects"
    ].lower()

    experience_text = sections[
        "experience"
    ].lower()

    skills_text = sections[
        "skills"
    ].lower()

    for skill in resume_skills:

        skill_lower = skill.lower()

        in_projects = (
            skill_lower in projects_text
        )

        in_experience = (
            skill_lower in experience_text
        )

        in_skills = (
            skill_lower in skills_text
        )

        if in_skills and (
            in_projects or in_experience
        ):

            strong.append(skill)

        elif (
            in_projects
            or
            in_experience
        ):

            moderate.append(skill)

        elif in_skills:

            limited.append(skill)

    return {
        "strong": strong,
        "moderate": moderate,
        "limited": limited
    }

