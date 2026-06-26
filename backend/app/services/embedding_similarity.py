from functools import lru_cache
import math
import os

from dotenv import load_dotenv
from google import genai


@lru_cache(maxsize=1)
def get_embedding_client():
    load_dotenv()

    api_key = (
        os.getenv("GEMINI_API_KEY_EMBEDDING")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY_ADVISOR")
        or os.getenv("GEMINI_API_KEY_INTERVIEW")
        or os.getenv("GEMINI_API_KEY_TAILOR")
    )

    if not api_key:
        raise ValueError("No Gemini API key configured for embeddings.")

    return genai.Client(api_key=api_key)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def calculate_embedding_similarity(
    resume_text,
    jd_text
):
    client = get_embedding_client()

    response = client.embeddings.create(
        model="textembedding-gecko-001",
        input=[resume_text, jd_text]
    )

    resume_embedding = response.data[0].embedding
    jd_embedding = response.data[1].embedding

    similarity = cosine_similarity(resume_embedding, jd_embedding)

    return float(round(similarity * 100, 2))
