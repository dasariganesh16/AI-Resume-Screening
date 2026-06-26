from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

def calculate_embedding_similarity(
    resume_text,
    jd_text
):
    model = get_embedding_model()

    resume_embedding = model.encode(
        resume_text
    )

    jd_embedding = model.encode(
        jd_text
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return float(round(float(similarity) * 100, 2))



if __name__ == "__main__":

    resume = """
    Experienced Machine Learning Engineer
    with Python, SQL, Deep Learning
    and NLP experience.
    """

    jd = """
    Looking for a Machine Learning Engineer
    with Python, SQL, Deep Learning
    and NLP skills.
    """

    score = calculate_embedding_similarity(
        resume,
        jd
    )

    print(score)
