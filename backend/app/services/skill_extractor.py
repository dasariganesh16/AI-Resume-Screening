import pandas as pd
import re
from functools import lru_cache
from pathlib import Path


SKILLS_FILE = Path(__file__).resolve().parents[1] / "data" / "skills.csv"


# -----------------------------
# Load skills from CSV
# -----------------------------

@lru_cache(maxsize=1)
def load_skills():
    df = pd.read_csv(SKILLS_FILE)
    return df["skill"].dropna().tolist()


# -----------------------------
# Normalization Dictionary
# -----------------------------

NORMALIZATION = {

    # AI
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",

    "natural language processing": "NLP",
    "nlp": "NLP",

    "large language model": "LLM",
    "large language models": "LLM",
    "llm": "LLM",
    "llms": "LLM",

    "retrieval augmented generation": "RAG",
    "retrieval-augmented generation": "RAG",
    "rag": "RAG",

    # APIs
    "rest api": "REST API",
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",

    # Frameworks
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",

    "reactjs": "React",
    "react.js": "React",

    "nodejs": "Node.js",
    "node.js": "Node.js",

    # Databases
    "pl/sql": "SQL",

    # Cloud
    "amazon web services": "AWS",

    # Git
    "github actions": "GitHub Actions",

    # AI Libraries
    "lang chain": "LangChain",

    # OOP
    "object oriented programming": "OOP",

    # DSA
    "data structures and algorithms": "Data Structures"
}


# -----------------------------
# Extract Skills
# -----------------------------

def extract_skills(text):

    text_lower = text.lower()

    skills_db = load_skills()

    found_skills = set()

    # Check normalization phrases
    for phrase, skill in NORMALIZATION.items():

        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.add(skill)

    # Check skills from CSV
    for skill in skills_db:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return sorted(found_skills)


# -----------------------------
# Testing
# -----------------------------

if __name__ == "__main__":

    sample_text = """
    Python
    SQL
    JavaScript
    Docker

    Built a Retrieval Augmented Generation chatbot.
    Used LangChain and FAISS.
    """

    skills = extract_skills(sample_text)

    print(skills)
