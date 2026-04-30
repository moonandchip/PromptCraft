# PromptCraft

PromptCraft is a prompt-engineering practice game. Players are shown a reference image and must craft a text prompt that generates an AI image as close as possible to the original. Attempts will be scored via image similarity (planned: CLIP-based scoring), with feedback to help users iterate.

## Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI (Python)
- Scoring: CLIP / embedding similarity
- Image generation: API-based (for example Leonardo)

## Repo Structure
- `frontend/` React UI
- `backend/` FastAPI API
- `auth/` Next.js + Auth.js authentication service

## Auth Architecture
- `auth.promptcraft.com`: Next.js + Auth.js service handles login, registration, and sessions.
- `api.promptcraft.com`: FastAPI service accepts authenticated requests and proxies auth operations to `auth.promptcraft.com`.
- Use separate Postgres databases:
  - Backend: `promptcraft_app` via `DATABASE_URL`
  - Auth: `promptcraft_auth` via `AUTH_DATABASE_URL` (or `DATABASE_URL` in the auth service)

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

### 2) Environment Variables
Docker Compose loads environment from service-local files:

- `backend/.env` (copy from `backend/.env.example`)
- `auth/.env` (copy from `auth/.env.example`)
- `frontend/.env` (copy from `frontend/.env.example`)

Note: backend/auth DB URLs should use `db` as host inside Docker (not `localhost`):

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/promptcraft?schema=public
AUTH_DATABASE_URL=postgresql://postgres:postgres@db:5432/promptcraft?schema=auth
```

### 3) Build and Run
From the project root:

```bash
docker compose up --build
```

### 4) Access Services
- Frontend: `http://localhost:5173`
- Backend health check: `http://127.0.0.1:8000/health`
- Auth service: `http://127.0.0.1:3000`
- Postgres: `localhost:5432` (user/password: `postgres` / `postgres`, db: `promptcraft`)

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

Auth service:
```bash
cd auth
npm ci
npx prisma generate
npx prisma db push
npm run build
```

## GitHub CI/CD
Workflow file: `.github/workflows/ci-cd.yml`

- CI:
  - Runs backend tests on Python 3.12
  - Runs frontend tests on Node 22
  - Builds auth service on Node 22
  - Triggers on `push` and `pull_request`
- CD:
  - On push to `main`, builds and publishes Docker images to GHCR:
    - `ghcr.io/<owner>/<repo>/backend:latest`
    - `ghcr.io/<owner>/<repo>/frontend:latest`
    - `ghcr.io/<owner>/<repo>/auth:latest`
