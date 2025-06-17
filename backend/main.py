# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import json

with open("context.json") as f:
    context = json.load(f)

system_msg = {
    "role": "system",
    "content": f"You are Ava, an AI assistant who represents {context['name']} to recruiters."
    # Florian is a {context['title']} skilled in {', '.join(context['skills'])}. He's currently working on projects like {', '.join(context['projects'])}. His career goals: {context['goals']}.
}

# Load environment variables
load_dotenv()

# Initialize OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Message(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Ava AI Assistant backend is live."}

from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY from your env

@app.post("/ask")
async def ask_ava(msg: Message):
    try:
        messages = [
            system_msg,
            {"role": "user", "content": msg.question}
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        print("OpenAI API Error:", e)
        return {"error": str(e)}