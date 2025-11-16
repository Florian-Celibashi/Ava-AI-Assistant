# Ava AI Assistant – Recruiter-Facing Copilot

## 🧭 Overview
Ava is a recruiter-facing AI assistant that helps talent teams get instant answers about roles, candidates, and hiring processes. It blends conversational intelligence, resume summarization, and structured data retrieval so that every recruiter can act with a personal research partner.

## ✨ Key Features
- **Job intelligence chat** – natural-language Q&A about openings, requirements, and processes.
- **Resume summarization** – condensed candidate overviews generated directly from uploaded résumés.
- **Structured data queries** – ask for pipeline stats or candidate lists using conversational filters.
- **Conversation memory** – Supabase persists prior chats so follow-up questions retain context.
- **Secure recruiter workspace** – per-user authentication, audit-friendly logging, and configurable guardrails.

## 🧰 Tech Stack
- **Environment & Tooling**
  - Node.js 18+, Python 3.11, pnpm/npm, uvicorn, Docker-ready services
- **Frontend Frameworks**
  - Next.js (App Router), React 18, TypeScript, Tailwind CSS, Vite-powered Storybook playgrounds
- **Backend Services**
  - FastAPI for REST + streaming endpoints, Pydantic models, LangChain-style orchestration modules
- **AI & Data Services**
  - OpenAI GPT models for chat + embeddings, Supabase Postgres + Vector Store for conversations & resume chunks, Redis cache for session tokens

## 🧩 Architecture Overview
- **Client Experience Layer**
  - Next.js UI exposes recruiter dashboards, chat widget, resume uploader, and structured query builder.
  - React Query keeps UI state in sync with backend APIs and Supabase real-time updates.
- **Application API Layer**
  - FastAPI service handles chat orchestration, resume parsing pipelines, and secure Supabase interactions.
  - Background workers schedule embedding generation and structured data lookups.
- **Intelligence Layer**
  - OpenAI chat + embedding models ground responses in curated context (role briefs, resume chunks).
  - Vector search ranks stored knowledge before each completion call.
- **Data Persistence Layer**
  - Supabase stores users, conversations, resumes, and analytics events; object storage keeps documents; SQL functions expose structured query results.

## ⚙️ Setup & Installation
1. **Clone & install**
   ```bash
   git clone https://github.com/your-org/ava-ai-assistant.git
   cd ava-ai-assistant
   ```
2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. **Backend**
   ```bash
   cd ../backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
4. **Supabase** – provision a project, enable Auth & Postgres, create `conversations`, `resumes`, and `job_insights` tables.

## 🔧 Configuration
Create `.env` files in both `frontend/` and `backend/` with the following keys:

```bash
# frontend/.env.local
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_MODEL=gpt-4o-mini

# backend/.env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
FRONTEND_URL=http://localhost:3000
RESUME_BUCKET=ava-resumes
```

## 🚀 Usage Examples
- **Ask a job question via API**
  ```bash
  curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question":"Summarize the must-have skills for the Senior Backend Engineer role"}'
  ```
- **Summarize a resume**
  ```bash
  curl -X POST http://localhost:8000/resume/summarize \
    -H "Authorization: Bearer <token>" \
    -F "file=@candidates/jordan-doe.pdf"
  ```
- **Run structured query from UI**
  1. Open `http://localhost:3000`.
  2. Choose *Structured Query* → “Show candidates with >5 years Go experience who passed recruiter screen.”
  3. Ava renders a sortable list along with suggested next steps.

## 🗂️ Folder Structure
```bash
ava-ai-assistant/
├── backend/            # FastAPI app, embeddings, vector search
│   ├── main.py
│   ├── openai_helpers.py
│   └── vector_search.py
├── frontend/           # Next.js app, UI components, hooks
│   ├── app/
│   ├── components/
│   └── lib/
├── myenv/              # Local Python environment assets
└── README.md
```

## 🔭 Future Improvements
- Voice input & calendaring integration for live recruiter screens.
- Fine-tuning workflows to align with company-specific tone & policies.
- Analytics dashboards highlighting funnel bottlenecks and FAQ deflection rates.
- Automated compliance checks for job descriptions and outreach copy.

## 📄 License
Released under the MIT License. Update `LICENSE` with your organization’s preferred terms if needed.
