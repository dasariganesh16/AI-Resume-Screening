from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def calculate_embedding_similarity(resume_text, jd_text):
    """Compute similarity between resume and job description using TF-IDF + cosine."""

    resume_text = (resume_text or "").strip()
    jd_text = (jd_text or "").strip()

    try:
        vectorizer = TfidfVectorizer()

        tfidf = vectorizer.fit_transform([
            resume_text,
            jd_text
        ])

        resume_vector = tfidf[0].toarray()[0]
        jd_vector = tfidf[1].toarray()[0]

    except Exception:
        return 0.0

    dot = np.dot(resume_vector, jd_vector)

    norm_resume = np.linalg.norm(resume_vector)
    norm_jd = np.linalg.norm(jd_vector)

    if norm_resume == 0 or norm_jd == 0:
        return 0.0

    similarity = dot / (norm_resume * norm_jd)

    return round(float(similarity * 100), 2)
