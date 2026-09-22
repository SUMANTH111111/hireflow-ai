from sentence_transformers import SentenceTransformer, util

# Load once when Flask starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(resume_text, job_text):
    """
    Returns semantic similarity between 0 and 1
    """

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_text,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    ).item()

    return similarity