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

## Windows Setup (First Time)

### Requirements
- Node.js 18+ (recommended)
- Python 3.10+ (3.11 is fine)
- Git

### Clone
```powershell
git clone https://github.com/moonandchip/PromptCraft.git
cd PromptCraft