from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding