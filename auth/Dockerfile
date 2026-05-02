FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./
# NODE_ENV=production with `npm ci` would skip devDependencies, but we need
# `prisma`, `typescript`, and `next`'s build tooling at image-build time.
RUN npm ci --include=dev

COPY . .

RUN npx prisma generate && npm run build

EXPOSE 3000

# Default to production. Local dev overrides `command:` in docker-compose.yml
# to run `next dev` against the bind-mounted source.
CMD ["sh", "-c", "npx prisma db push && exec npm run start -- --hostname 0.0.0.0 --port 3000"]
