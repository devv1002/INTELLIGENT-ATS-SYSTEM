import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(
    resume_embedding,
    jd_embedding
):

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100, 2)