# Ava AI Assistant — Professional Conversational Agent
### https://ava-ai-assistant.vercel.app
## 🧭 Overview
- AI copilot that represents Florian professionally to recruiters and collaborators.
- Combines curated resume context, retrieval-augmented prompts, and a modern chat UI.
- Ships with FastAPI backend + Vite/React frontend deployable to Render/Vercel.

## ✨ Key Features
- **Context-aware replies** – Local BM25-style chunk retrieval keeps answers grounded in Florian's experience without extra embedding latency.
- **Modern chat interface** – Responsive React UI with auto-scroll, typing indicators, and avatar branding.
- **Startup readiness notice** – Pings the backend to surface cold-start messaging for free-tier hosting.
- **Conversation continuity** – Frontend sends bounded chat history so answers remain consistent across turns.
- **Configurable OpenAI access** – Environment variables control model, API keys, CORS origins, and cache behavior.
- **Production-friendly** – Dockerfile, Procfile, and requirements lock in reproducible deployments.

## 🧰 Tech Stack
- **Environment**
  - Node.js 20+, Python 3.11+, npm, uvicorn
- **Frameworks**
  - Frontend: React + Vite, Tailwind-esque utility styling
  - Backend: FastAPI, Pydantic, Starlette
- **Libraries**
  - Frontend: Fetch API, custom startup notice component
  - Backend: OpenAI Python SDK, python-dotenv for secrets
- **Services**
  - OpenAI Chat Completions API (model default `gpt-4o-mini`, env override supported)
  - Optional hosting: Render (backend), Vercel/Netlify (frontend)

## 🧩 Architecture Overview
- **Retrieval Layer** – `context_index.py` builds a local context index from `context.json` and ranks relevant chunks in-memory.
- **Prompt Orchestration** – `main.py` assembles system persona, retrieved context snippets, bounded history, and user question.
- **API Layer** – FastAPI exposes `/`, `/healthz`, `/readyz`, and `/ask` with strict request validation and response caching.
- **Frontend Client** – `frontend/src/App.jsx` manages local chat state, optimistic UI updates, and asynchronous responses.
- **Startup Notice** – `frontend/src/components/StartupNotice.jsx` continuously pings the backend and surfaces cold-start messaging until ready.

## ⚙️ Setup & Installation
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

## 🔐 Configuration
Create `.env` files at both roots:

**backend/.env**
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini     # optional override
FRONTEND_URL=http://localhost:5173
FRONTEND_URLS=https://your-frontend.example.com
MAX_CONTEXT_CHUNKS=4
MAX_HISTORY_MESSAGES=8
RESPONSE_CACHE_TTL_SECONDS=600
RESPONSE_CACHE_MAX_ITEMS=256
OPENAI_TIMEOUT_SECONDS=45
```

**frontend/.env**
```bash
VITE_API_URL=http://localhost:8000
VITE_BACKEND_URL=http://localhost:8000
```

## 📁 Folder Structure
```
Ava-AI-Assistant/
├── backend/           # FastAPI service + local retrieval index
│   ├── main.py        # API + OpenAI orchestration + caching
│   ├── context_index.py
│   ├── settings.py
│   ├── context.json   # Resume/project knowledge base
│   └── requirements.txt
├── frontend/          # React/Vite chat client
│   ├── src/App.jsx
│   ├── src/components/StartupNotice.jsx
│   └── vite.config.js
└── README.md
```

## 🔮 Future Improvements
- Add persistent conversation history with database storage.
- Introduce authentication for recruiter-only insights.
- Implement analytics dashboard for session metrics.
- Expand retrieval store to a managed vector DB (Pinecone/Weaviate).
