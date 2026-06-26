def generate_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            f"Consider learning {skill}"
        )

        suggestions.append(
            f"Add a project using {skill}"
        )

    return suggestions