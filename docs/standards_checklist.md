# Standards Compliance Checklist

This checklist identifies every gap between the current PromptCraft codebase and the engineering standards defined in `engineering_standards.md`. Work through each item to bring the codebase up to standard.

---

## 1. Exception Hierarchy

- [ ] Create `app/exceptions/__init__.py` and `app/exceptions/base.py` with `BaseErrorCodeEnum` and `AppException`
- [ ] Create `app/round/domain/exceptions.py` with `RoundError` enum (`UNKNOWN_ERROR`, `NOT_FOUND`, `GENERATION_FAILED`, `GENERATION_TIMEOUT`, `NO_API_KEY`, `SAVE_FAILED`)
- [ ] Create per-operation exception classes: `SubmitRoundException`, `StartRoundException`, `GetRoundAttemptsException`
- [ ] Create `app/auth/domain/exceptions.py` with `AuthError` enum (`UNKNOWN_ERROR`, `INVALID_CREDENTIALS`, `SERVICE_UNAVAILABLE`, `INVALID_TOKEN`)
- [ ] Create per-operation exception classes: `LoginException`, `RegisterException`, `ResolveTokenException`
- [ ] Create `app/stats/domain/exceptions.py` with `StatsError` enum and `GetStatsException`
- [ ] Migrate `RoundServiceError` usages in service layer to use new typed exceptions
- [ ] Migrate `AuthServiceError` usages in service layer to use new typed exceptions
- [ ] Migrate `GenerationError` in `generate_image.py` to use `RoundError` codes via adapter
- [ ] Remove old error classes (`RoundServiceError`, `AuthServiceError`, `GenerationError`) once migration is complete

## 2. Global Exception Handler

- [ ] Add `@app.exception_handler(AppException)` to `app/main.py` returning `{data, error, message}` envelope
- [ ] Remove manual `HTTPException` raises from `submit_endpoint.py`
- [ ] Remove manual `HTTPException` raises from `start_endpoint.py`
- [ ] Remove manual `HTTPException` raises from `get_round_attempts_endpoint.py`
- [ ] Remove manual `HTTPException` raises from `login.py` (transport)
- [ ] Remove manual `HTTPException` raises from `register.py` (transport)
- [ ] Remove manual `HTTPException` raises from `me.py` (auth transport)
- [ ] Verify all transport endpoints follow the three-block pattern: happy path, domain exception (re-raise), unknown exception (log + wrap)

## 3. API Response Envelope

- [ ] Create a generic `ApiResponse[T]` Pydantic model with `data`, `error`, `message` fields
- [ ] Wrap all success responses in `ApiResponse` envelope across every endpoint
- [ ] Ensure error responses from the global handler use the same `{data: null, error: "CODE", message: "..."}` shape
- [ ] Update `health` endpoint to return `ApiResponse(data={"status": "ok"}, error=None, message=None)`

## 4. Structured Logging

- [ ] Create `app/constants.py` with app-wide logging channels (`ROUND_CHANNEL`, `AUTH_CHANNEL`, `STATS_CHANNEL`, `AI_CHANNEL`)
- [ ] Create `app/round/domain/constants.py` with feature name constants (`SUBMIT_ROUND_FEATURE`, `START_ROUND_FEATURE`, etc.)
- [ ] Create `app/auth/domain/constants.py` with feature name constants (`LOGIN_FEATURE`, `REGISTER_FEATURE`, etc.)
- [ ] Create `app/stats/domain/constants.py` with feature name constants (`GET_STATS_FEATURE`)
- [ ] Add structured `extra={}` dicts to all `logger.info()` calls in service layer (channel, feature, user, entity)
- [ ] Add structured `extra={}` dicts to all `logger.error()` calls in transport/service layers
- [ ] Replace unstructured format-string logs in `generate_image.py` with structured `extra={}` logging
- [ ] Replace unstructured format-string logs in `clip_scoring.py` with structured `extra={}` logging
- [ ] Verify no `print()` statements exist anywhere in the codebase

## 5. `log_attributes` on ORM Models

- [ ] Create `app/round/domain/types/log_attributes.py` with `AttemptLogAttributes`, `RoundUserLogAttributes`, `PromptLogAttributes`
- [ ] Add `log_attributes` property to `Attempt` model in `entities.py`
- [ ] Add `log_attributes` property to `RoundUser` model in `entities.py`
- [ ] Add `log_attributes` property to `Prompt` model in `entities.py`
- [ ] Add `log_attributes` property to `RoundImage` model in `entities.py`
- [ ] Add `log_attributes` property to `Round` model in `stats/data/entities.py`
- [ ] Update all service log calls to use `entity.log_attributes` instead of ad-hoc dicts

## 6. Typed Args Dataclasses

- [ ] Create `app/round/domain/types/args.py` with `SubmitRoundArgs`, `StartRoundArgs`
- [ ] Create `app/auth/domain/types/args.py` with `LoginArgs`, `RegisterArgs`
- [ ] Refactor `submit_round()` to accept `SubmitRoundArgs` instead of individual kwargs
- [ ] Refactor `start_round()` to accept `StartRoundArgs`
- [ ] Refactor `save_submission()` to accept a dataclass instead of 8 individual kwargs
- [ ] Refactor auth service functions (`login()`, `register_user()`) to accept typed args
- [ ] Update all transport endpoints to construct args dataclasses from request body + current_user

## 7. Adapter Pattern for External AI Services

- [ ] Create `app/adapters/base_ai_adapter.py` with `BaseImageGenerationAdapter` and `BaseScoringAdapter` ABCs
- [ ] Create `app/adapters/leonardo_adapter.py` — extract Leonardo HTTP logic from `generate_image.py` into adapter class
- [ ] Create `app/adapters/clip_adapter.py` — extract CLIP scoring logic from `clip_scoring.py` into adapter class
- [ ] Update `submit_round()` to receive adapters via dependency injection instead of importing directly
- [ ] Create FastAPI dependency functions to provide adapter instances
- [ ] Remove direct HTTP/SDK calls from service layer files
- [ ] Write unit tests for `leonardo_adapter.py` in `tests/unit/adapters/`
- [ ] Write unit tests for `clip_adapter.py` in `tests/unit/adapters/`

## 8. Centralized Config (pydantic-settings)

- [ ] Add `pydantic-settings` to `pyproject.toml` dependencies
- [ ] Create `app/config.py` with a `Settings` class validating `DATABASE_URL`, `LEONARDO_API_KEY`, `AUTH_SERVICE_URL`
- [ ] Replace `os.environ.get()` calls in `generate_image.py` with injected config
- [ ] Replace `os.environ.get()` calls in `db.py` with injected config
- [ ] Replace `os.environ.get()` calls in auth service config builder with injected config
- [ ] Add a FastAPI dependency that provides the `Settings` singleton

## 9. Domain Folder Structure

- [ ] Create `app/round/domain/` directory with `__init__.py`
- [ ] Create `app/auth/domain/` directory with `__init__.py`
- [ ] Create `app/stats/domain/` directory with `__init__.py`
- [ ] Move/create domain-specific `constants.py`, `exceptions.py`, and `types/` into each domain folder
- [ ] Update all imports across the codebase to reference new domain paths

## 10. Pydantic Schema Naming

- [ ] Rename `SubmitRequest` → `RoundSubmitRequest`
- [ ] Rename `SubmitResponse` → `RoundSubmitResponse`
- [ ] Rename `StartRoundResponse` → `RoundStartResponse`
- [ ] Rename `RoundInfo` → `RoundListItem` or keep as `RoundInfo` (acceptable)
- [ ] Rename `AttemptInfo` → `RoundAttemptResponse`
- [ ] Update all imports and usages after renaming

## 11. Test Structure Alignment

- [ ] Reorganise `tests/` into `tests/unit/` and `tests/integration/` top-level split
- [ ] Move existing unit tests under `tests/unit/round/`, `tests/unit/auth/`, `tests/unit/stats/`
- [ ] Create `tests/integration/transport/` for full-stack integration tests
- [ ] Create integration tests for round submit flow (with test DB, mocked Leonardo/CLIP adapters)
- [ ] Create integration tests for auth flow
- [ ] Create integration tests for stats flow
- [ ] Ensure every test class follows `TestXxx` naming matching the source file
- [ ] Ensure every service/data function has tests for happy path + each failure mode
- [ ] Add tests for unknown exception wrapping in transport endpoints

## 12. Transport Endpoint Pattern

- [ ] Ensure every endpoint follows the three-block try/except pattern (happy path → domain exception → unknown exception)
- [ ] Add unknown-exception wrapping to `me_stats_endpoint` in stats (currently has no error handling)
- [ ] Add structured error logging in the unknown-exception catch block of every endpoint
- [ ] Verify endpoints construct `ApiResponse` envelopes on success

## 13. Database Migrations

- [ ] Add Alembic to `pyproject.toml` dev dependencies
- [ ] Initialise Alembic (`alembic init alembic`)
- [ ] Create initial migration from existing ORM models
- [ ] Document migration workflow in CLAUDE.md

## 14. CI Pipeline

- [ ] Create GitHub Actions workflow with lint, unit test, integration test, and coverage stages
- [ ] Configure flake8 to run as a CI stage
- [ ] Configure pytest coverage thresholds (90% service, 80% data, 80% adapter, 80% transport)
- [ ] Set up branch protection rules on `main` (require PR, require CI green, require 1 approval)

## 15. Commit Message Convention

- [ ] Adopt conventional commits format: `type(scope): summary`
- [ ] Valid types: `feat`, `fix`, `chore`, `test`, `docs`, `refactor`, `perf`
- [ ] Valid scopes: `round`, `auth`, `stats`, `ai`, `db`, `ci`
