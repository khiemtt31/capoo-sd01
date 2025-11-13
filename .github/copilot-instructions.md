## Purpose
Short, actionable guidance for AI coding assistants to be productive in this repository.

Keep this focused on discoverable, repo-specific patterns (commands, layout, integration points).

## High-level architecture (quick)
- Monorepo managed by pnpm (see `pnpm-workspace.yaml`). Top-level packages are under `apps/*` and `packages/*`.
- Frontend: Next.js app at `apps/frontend` (uses app-router). Check `apps/frontend/package.json` for deps (React, Next, TanStack Query, axios, zod).
- Backend: Python FastAPI service at `apps/backend` (entry: `apps/backend/app/main.py`). Uses SQLAlchemy/SQLModel for models and alembic for migrations (see `apps/backend/requirements.txt`).
- Shared JS/TS utilities live in `packages/shared` and are built with `tsup` (see `packages/shared/package.json`).
- Database: Postgres docker-compose under `database/` — used for local development. The backend uses `.env` (pydantic Settings) to load `DATABASE_URL` (see `apps/backend/app/core/config.py`).

## Quick developer workflows (explicit commands)
- Install JS deps (root): pnpm install
- Build all JS packages: pnpm -r build
- Lint JS packages: pnpm -r lint
- Run frontend locally (from repo root): cd apps/frontend && pnpm dev
  - Note: top-level scripts `dev:web` / `dev:api` use package filters `web`/`api` which don't match the actual package names; prefer running the package script directly.
- Run backend locally (from `apps/backend`):
  - Create venv: `python -m venv .venv`
  - Activate (Git Bash / bash.exe on Windows): `source .venv/Scripts/activate` (or use `.venv\\Scripts\\activate` in PowerShell/cmd)
  - Install: `pip install -r requirements.txt`
  - Start DB (from project root): `cd database && docker-compose up -d`
  - Run server: `uvicorn app.main:app --reload` (FastAPI app will expose docs at `/api/docs` per `app.main` configuration)

## Key repo-specific patterns and gotchas
- API prefix: The backend sets an `API_PREFIX` in `apps/backend/app/core/config.py` (default `/api`) and mounts routers with that prefix. Expect OpenAPI and docs under `/api/*`.
- Model registration: Domain model modules are explicitly imported in `app/main.py` (e.g. `app.domain.user_model`) to ensure models register with `Base.metadata`. When adding models, import them into `app/main.py` or another import-time registration point.
- Postgres DROP behavior: `register_drop_cascade_for_postgres()` in `app/main.py` attaches a DDL listener to append `CASCADE` to `DROP TABLE` for PostgreSQL. Be mindful when running `Base.metadata.drop_all()` in dev.
- Settings: `pydantic-settings` loads `.env` (see `Settings.model_config` in `apps/backend/app/core/config.py`). Use that `.env` for local secrets like `DATABASE_URL`, `SECRET_KEY`, etc.
- Migrations: `alembic` is present in `requirements.txt`. If you need to change schemas, prefer alembic migrations over `Base.metadata.create_all()` for non-trivial changes.

## Files you should look at when coding
- Backend entry & wiring: `apps/backend/app/main.py`
- Backend config: `apps/backend/app/core/config.py`
- API controllers: `apps/backend/app/api/*` (routers/controllers)
- Domain models: `apps/backend/app/domain/*` (models are imported in `main.py`)
- Frontend entry & routes: `apps/frontend/app/*`, `apps/frontend/package.json`
- Workspace layout & scripts: `pnpm-workspace.yaml`, top-level `package.json`
- Local DB orchestration: `database/docker-compose.yml` and SQL schemas `database/*.sql`
- Shared utilities: `packages/shared/src` and `packages/shared/package.json`

## Example small tasks and how to approach them
- Add a backend model: create model under `apps/backend/app/domain/`, add import in `apps/backend/app/main.py` so it's registered, add alembic revision, run migrations against the dockerized DB.
- Change frontend API call: update an axios call in `apps/frontend` to point to `http://localhost:8000/api/...` (note the API prefix).

## Notes for the AI assistant
- Prefer concrete edits to the files referenced above; when changing DB schema prefer generating an alembic migration file and document the migration steps.
- If you run or suggest commands that start services, reference the exact file that defines the service (e.g. `database/docker-compose.yml`).
- Do not assume top-level pnpm scripts are authoritative—double-check the package name under `apps/*` before using `pnpm --filter`.

---
If any of the sections above are unclear or you'd like me to include extra examples (for example, a short sample alembic migration or an example API router change), tell me which area to expand and I will iterate.
