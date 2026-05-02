-- Runs once, on the first Postgres boot when the data directory is empty.
-- 'public' always exists; 'auth' is created here so next-auth's prisma client
-- has somewhere to write to on first deploy.
CREATE SCHEMA IF NOT EXISTS auth;
