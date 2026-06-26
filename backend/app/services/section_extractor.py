def extract_sections(resume_text):

    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": "",
        "certifications": ""
    }

    headings = {
        "education": "education",
        "experience": "experience",
        "projects": "projects",
        "skills": "technical skills",
        "certifications": "certifications"
    }

    text_lower = resume_text.lower()

    for section_name, heading in headings.items():

        start = text_lower.find(heading)

        if start == -1:
            continue

        end = len(resume_text)

        for other_heading in headings.values():

            if other_heading == heading:
                continue

            pos = text_lower.find(
                other_heading,
                start + 1
            )

            if pos != -1 and pos < end:
                end = pos

        sections[section_name] = resume_text[start:end]

    return sections



if __name__ == "__main__":

    sample_text = """
    Education
    B.Tech CSE

    Experience
    Web Development Internship

    Projects
    Library Management System using Java

    Technical Skills
    Java SQL Git

    Certifications
    Java Certificate
    """

    sections = extract_sections(
        sample_text
    )

    print(sections)