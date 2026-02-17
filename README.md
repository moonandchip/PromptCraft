# PromptCraft

PromptCraft is a prompt-engineering practice game. Players are shown a reference image and must craft a text prompt that generates an AI image as close as possible to the original. Attempts will be scored via image similarity (planned: CLIP-based scoring), with feedback to help users iterate.

## Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI (Python)
- Scoring (planned): CLIP / embedding similarity
- Image generation (planned): API-based (for example Leonardo)

## Repo Structure
- `frontend/` React UI
- `backend/` FastAPI API

## Local Development (Docker)

### Requirements
- Docker Desktop (or Docker Engine + Compose)
- Git
- Poetry (only needed for running backend tests locally outside Docker)

### 1) Clone the Repository
```bash
git clone https://github.com/moonandchip/PromptCraft.git
cd PromptCraft
```

### 2) Optional Environment Variables
Create a root `.env` file if you want to override defaults used by `docker compose`.

You can start from:
```bash
cp .env.example .env
```

```env
VITE_API_URL=http://localhost:8000
LEONARDO_API_KEY=your_key_here
```

### 3) Build and Run
From the project root:

```bash
docker compose up --build
```

### 4) Access Services
- Frontend: `http://localhost:5173`
- Backend health check: `http://127.0.0.1:8000/health`

Expected health response:
```json
{"status":"ok"}
```

### Useful Commands
Stop containers:
```bash
docker compose down
```

Rebuild after dependency changes:
```bash
docker compose up --build
```

## Run Tests Locally
Frontend:
```bash
cd frontend
npm ci
npm run test
```

Backend:
```bash
cd backend
poetry install --with dev
poetry run pytest tests -q
```

## GitHub CI/CD
Workflow file: `.github/workflows/ci-cd.yml`

- CI:
  - Runs backend tests on Python 3.12
  - Runs frontend tests on Node 22
  - Triggers on `push` and `pull_request`
- CD:
  - On push to `main`, builds and publishes Docker images to GHCR:
    - `ghcr.io/<owner>/<repo>/backend:latest`
    - `ghcr.io/<owner>/<repo>/frontend:latest`
