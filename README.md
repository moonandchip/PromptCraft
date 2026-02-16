# PromptCraft

PromptCraft is a prompt-engineering practice game. Players are shown a reference image and must craft a text prompt that generates an AI image as close as possible to the original. Attempts will be scored via image similarity (planned: CLIP-based scoring), with feedback to help users iterate.

## Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI (Python)
- Scoring (planned): CLIP / embedding similarity
- Image generation (planned): API-based (e.g., Leonardo)

## Repo Structure
- `frontend/` React UI
- `backend/` FastAPI API
- `docs/` architecture + decisions + runbook
- `scripts/` Windows PowerShell helpers
- `.github/` PR templates, issue templates, CI

---

## 🚀 Local Development Setup (Windows)

### Requirements

- Python 3.10+
- Node.js 22 LTS (or >= 20.19.0)
- Git

Check versions:

node -v
python --version

Node must be v22.x.x (or >= 20.19.0).

---

## 1) Clone the Repository

git clone https://github.com/moonandchip/PromptCraft.git
cd PromptCraft

---

## 2) Backend Setup (FastAPI)

cd backend
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..

Create backend/.env file with:

DATABASE_URL=your_database_url_here
LEONARDO_API_KEY=your_key_here

---

## 3) Frontend Setup (React + Vite)

cd frontend
npm install
cd ..

Create frontend/.env file with:

VITE_API_URL=http://localhost:8000

---

## 4) Run the Full Development Environment

From project root:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\dev.ps1

Frontend:
http://localhost:5173

Backend health check:
http://127.0.0.1:8000/health

Expected response:
{"status":"ok"}

---

Important:
- Do not commit .env files
- Always create feature branches
- Do not push directly to main