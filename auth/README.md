# PromptCraft Auth Service

This service runs the authentication domain (`auth.promptcraft.com`) using:

- Next.js (App Router)
- Auth.js (Credentials provider)
- Prisma + PostgreSQL

## Environment Variables

Use `auth/.env.example` as a template.

- `AUTH_DATABASE_URL`: shared Postgres DB URL, recommended to use a dedicated schema:
  - `postgresql://.../promptcraft?schema=auth`
- `AUTH_SECRET`: random long secret used to sign Auth.js tokens
- `AUTH_URL`: public auth service URL
- `AUTH_TRUST_HOST`: set to `true` behind reverse proxies

## Local Commands

```bash
npm ci
npx prisma generate
npx prisma db push
npm run dev
```

## Endpoints

- `POST /api/register` create credentials user
- `POST /api/internal/login` backend-facing credentials login
- `GET /api/internal/me` backend-facing bearer token validation
- `GET|POST /api/auth/*` Auth.js routes
- `GET /api/session` current authenticated session
