# Ava AI Assistant — Professional Conversational Agent

## 🧭 Overview
- AI copilot that represents Florian professionally to recruiters and collaborators.
- Combines curated resume context, retrieval-augmented prompts, and a modern chat UI.
- Ships with FastAPI backend + Vite/React frontend deployable to Render/Vercel.

## ✨ Key Features
- **Context-aware replies** – Embedding-powered chunk retrieval keeps answers grounded in Florian's experience.
- **Modern chat interface** – Responsive React UI with auto-scroll, typing indicators, and avatar branding.
- **Startup readiness notice** – Pings the backend to surface cold-start messaging for free-tier hosting.
- **Configurable OpenAI access** – Environment variables control model, API keys, and CORS origins.
- **Production-friendly** – Dockerfile, Procfile, and requirements lock in reproducible deployments.

## 🧰 Tech Stack
- **Environment**
  - Node.js 20+, Python 3.11+, npm, uvicorn
- **Frameworks**
  - Frontend: React 18 + Vite, Tailwind-esque utility styling
  - Backend: FastAPI, Pydantic, Starlette
- **Libraries**
  - Frontend: Axios for API calls, custom startup notice component
  - Backend: OpenAI Python SDK, NumPy, python-dotenv for secrets
- **Services**
  - OpenAI Chat Completions API (model default `gpt-5` env override)
  - Optional hosting: Render (backend), Vercel/Netlify (frontend)

## 🧩 Architecture Overview
- **Retrieval Layer** – `vector_search.py` embeds stored memory chunks and ranks them against user prompts.
- **Prompt Orchestration** – `main.py` assembles system persona, context fact injection, and user message before calling OpenAI.
- **API Layer** – FastAPI exposes `/` health check and `/ask` endpoint, handling CORS and structured request validation.
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
OPENAI_MODEL=gpt-5           # optional override
FRONTEND_URL=http://localhost:5173
```

**frontend/.env**
```bash
VITE_API_URL=http://localhost:8000
VITE_BACKEND_URL=http://localhost:8000
```

## 🚀 Usage Examples
```bash
# Run backend API
cd backend
uvicorn main:app --reload --port 8000

# Run frontend dev server
cd frontend
npm run dev
```
Visit `http://localhost:5173`, introduce yourself, and Ava will respond with context-grounded answers from Florian's profile.

## 📁 Folder Structure
```
Ava-AI-Assistant/
├── backend/           # FastAPI service, embeddings, memory chunks
│   ├── main.py        # API + OpenAI orchestration
│   ├── vector_search.py
│   ├── context.json   # Resume/project knowledge base
│   ├── memory_chunks.json
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

## 📜 License
MIT License. Use, modify, and deploy with attribution to the original author.
