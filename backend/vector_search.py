from openai_helpers import generate_embedding
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def find_most_relevant_chunk(user_input, stored_chunks):
    input_vector = generate_embedding(user_input)
    best_score = -1
    best_chunk = None
    for chunk in stored_chunks:
        sim = cosine_similarity(input_vector, chunk["embedding"])
        if sim > best_score:
            best_score = sim
            best_chunk = chunk["text"]
    return best_chunk