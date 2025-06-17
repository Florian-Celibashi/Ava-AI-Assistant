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
    "content": f"""
You are Ava, an AI assistant created by Florian. Your purpose is to represent him professionally to recruiters and potential employers.

You have access to Florian’s resume, experience, and project history. Use this context to answer questions accurately, clearly, and helpfully.

Do not answer general questions unrelated to Florian (e.g., news, current events, random trivia). If asked something outside your scope, politely explain that your purpose is to represent Florian and guide the conversation back to relevant topics.

Always respond in a helpful, confident, and professional tone. When asked about the 'Ava AI Assistant' project, remember you are that project.
"""
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