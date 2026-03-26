# Engineering Coding Standards — Context Document
---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Folder Structure](#2-folder-structure)
3. [Naming Conventions](#3-naming-conventions)
4. [Constants](#4-constants)
5. [Error Handling](#5-error-handling)
6. [Logging Standards](#6-logging-standards)
7. [API Response Conventions](#7-api-response-conventions)
8. [AI Adapter Pattern](#8-ai-adapter-pattern)
9. [Testing Standards](#9-testing-standards)
10. [Git & CI/CD Conventions](#10-git--cicd-conventions)

---

## 1. Purpose & Scope

This document defines the engineering coding standards for the PromptCraft project — an AI-powered prompt practice game where users write text prompts to generate images, which are scored against reference images using CLIP similarity. It serves as the single source of truth for both human engineers and AI coding assistants (e.g. GitHub Copilot, Claude, Cursor) when generating, reviewing, or modifying code.

All contributors — regardless of experience level — are expected to follow these standards. Consistency in naming, structure, error handling, and logging is non-negotiable. Code that violates these standards will be flagged in code review and must be corrected before merge.

> **Architectural Foundation**
>
> | Layer | Stack |
> |---|---|
> | Frontend | React + TypeScript — Type-based folder structure |
> | Backend | Python + FastAPI — Transport → Service → Data layers |
> | Database | PostgreSQL — SQLAlchemy ORM |
> | AI | Leonardo AI (image generation) + CLIP (image similarity scoring) — Adapter pattern (services never call external AI SDKs directly) |
> | Auth | External auth microservice (proxied via HTTP) |
> | Testing | Pytest — Unit + Integration |

---

## 2. Folder Structure

### 2.1 Backend

The backend follows a strict three-layer architecture organized vertically by domain. Each domain (round, auth, stats) owns all three layers. No layer may import from a layer above it. Each domain also owns its own constants, exceptions, types, and logging contracts.

```
backend/
├── app/
│   ├── main.py                       # FastAPI app entry point & global exception handlers
│   ├── config.py                     # Settings via pydantic-settings
│   ├── db.py                         # SQLAlchemy engine & session factory
│   ├── constants.py                  # App-wide logging channels
│   ├── exceptions.py                 # BaseErrorCodeEnum + AppException hierarchy
│   ├── response.py                   # ApiResponse[T] generic envelope
│   │
│   ├── auth/                         # Auth domain
│   │   ├── constants.py              # CHANNEL re-export + feature name constants
│   │   ├── exceptions.py             # AuthError enum + typed exception classes
│   │   ├── models.py                 # Pydantic request/response schemas
│   │   ├── types/
│   │   │   └── args.py               # LoginArgs, RegisterArgs dataclasses
│   │   ├── data/                     # Layer 3: External auth service HTTP calls
│   │   │   ├── get_internal_me.py
│   │   │   ├── post_internal_login.py
│   │   │   ├── post_register.py
│   │   │   └── request_auth_service.py
│   │   ├── service/                  # Layer 2: Business logic
│   │   │   ├── login.py
│   │   │   ├── register_user.py
│   │   │   ├── resolve_user_from_token.py
│   │   │   ├── errors.py
│   │   │   └── types.py
│   │   └── transport/                # Layer 1: HTTP endpoints
│   │       ├── router.py
│   │       ├── login.py
│   │       ├── register.py
│   │       ├── me.py
│   │       ├── get_auth_service.py
│   │       └── get_current_user.py
│   │
│   ├── round/                        # Round domain
│   │   ├── constants.py              # CHANNEL re-export + feature name constants
│   │   ├── exceptions.py             # RoundError enum + typed exception classes
│   │   ├── models.py                 # Pydantic request/response schemas
│   │   ├── types/
│   │   │   ├── args.py               # SubmitRoundArgs, StartRoundArgs dataclasses
│   │   │   └── log_attributes.py     # AttemptLogAttributes, RoundUserLogAttributes TypedDicts
│   │   ├── data/                     # Layer 3: DB access
│   │   │   ├── entities.py           # SQLAlchemy ORM models
│   │   │   ├── get_attempts_by_round_id.py
│   │   │   ├── get_next_attempt_number.py
│   │   │   ├── get_or_create_image.py
│   │   │   ├── get_or_create_user.py
│   │   │   ├── save_attempt.py
│   │   │   ├── save_prompt.py
│   │   │   ├── save_round_start.py
│   │   │   └── save_submission.py
│   │   ├── service/                  # Layer 2: Business logic
│   │   │   ├── submit_round.py
│   │   │   ├── start_round.py
│   │   │   ├── get_round_by_id.py
│   │   │   ├── get_rounds.py
│   │   │   ├── get_round_attempts.py
│   │   │   ├── get_round_history.py
│   │   │   ├── clip_scoring.py
│   │   │   └── generate_image.py
│   │   └── transport/                # Layer 1: HTTP endpoints
│   │       ├── router.py
│   │       ├── submit_endpoint.py
│   │       ├── start_endpoint.py
│   │       ├── get_rounds_endpoint.py
│   │       ├── get_round_attempts_endpoint.py
│   │       ├── get_round_history_endpoint.py
│   │       └── get_db_session.py
│   │
│   ├── stats/                        # Stats domain
│   │   ├── constants.py              # CHANNEL re-export + feature name constants
│   │   ├── exceptions.py             # StatsError enum + typed exception classes
│   │   ├── models.py
│   │   ├── data/
│   │   │   ├── entities.py
│   │   │   ├── get_rounds_aggregates_by_user_id.py
│   │   │   └── get_user_stats_from_attempts.py
│   │   ├── service/
│   │   │   └── get_user_stats.py
│   │   └── transport/
│   │       ├── router.py
│   │       ├── me.py
│   │       └── get_db_session.py
│   │
│   └── adapters/                     # External service adapters
│       ├── base_ai_adapter.py        # Abstract base for AI adapters
│       ├── leonardo_adapter.py       # Leonardo AI image generation
│       └── clip_adapter.py           # CLIP similarity scoring
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── service/
│   │   │   └── transport/
│   │   ├── round/
│   │   │   ├── data/
│   │   │   ├── service/
│   │   │   └── transport/
│   │   ├── stats/
│   │   │   ├── data/
│   │   │   ├── service/
│   │   │   └── transport/
│   │   └── adapters/
│   └── integration/
│       └── transport/
│
├── pyproject.toml
├── poetry.lock
└── Dockerfile
```

### 2.2 Frontend

The frontend uses a type-based folder structure. Components are never domain-specific at the `/components` level — domain logic lives inside `/pages`. All API service functions, shared types, and hooks are at the root of their respective folders.

```
frontend/
├── src/
│   ├── components/                   # Reusable, domain-agnostic UI components
│   │   ├── ui/                       # Primitive components (Button, Input, Modal)
│   │   └── layout/                   # Layout components (Navbar, Sidebar)
│   │
│   ├── pages/                        # Full page views — one file per route
│   │   ├── Dashboard.tsx
│   │   ├── RoundPlay.tsx
│   │   ├── RoundHistory.tsx
│   │   └── Profile.tsx
│   │
│   ├── hooks/                        # Custom React hooks
│   │   ├── useRounds.ts
│   │   ├── useStats.ts
│   │   └── useAuth.ts
│   │
│   ├── services/                     # API client functions (axios wrappers)
│   │   ├── roundService.ts
│   │   ├── statsService.ts
│   │   └── authService.ts
│   │
│   ├── types/                        # Shared TypeScript interfaces and types
│   │   ├── round.types.ts
│   │   ├── stats.types.ts
│   │   └── api.types.ts              # ApiResponse<T> envelope type lives here
│   │
│   ├── utils/                        # Pure utility functions
│   ├── store/                        # Global state (Zustand or React Context)
│   └── App.tsx
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/                          # Playwright specs
│
├── .eslintrc.json
├── .prettierrc
└── tsconfig.json
```

---

## 3. Naming Conventions

### 3.1 Backend — Python

Python naming strictly follows PEP 8.

| Construct | Convention | Example |
|---|---|---|
| Files / Modules | `snake_case` | `submit_round.py` |
| Classes | `PascalCase` | `RoundUser` |
| Functions / Methods | `snake_case` + verb prefix | `get_round_by_id()` |
| Variables | `snake_case` | `similarity_score` |
| Constants | `SCREAMING_SNAKE_CASE` | `POLL_MAX_ATTEMPTS` |
| Pydantic Schemas | `PascalCase` + suffix | `RoundSubmitRequest` |
| SQLAlchemy Models | `PascalCase` | `RoundUser`, `Attempt` |
| Services | `snake_case` functions | `submit_round()` |
| Args dataclasses | `PascalCase` + `Args` suffix | `SubmitRoundArgs` |
| Error enums | `PascalCase` + `Error` suffix | `RoundError` |
| Exception classes | `PascalCase` + `Exception` | `SubmitRoundException` |
| LogAttributes TypedDict | `PascalCase` + `LogAttributes` | `AttemptLogAttributes` |
| Adapters | `PascalCase` + `Adapter` | `LeonardoAdapter` |
| Test files | `test_` prefix | `test_submit_round.py` |

#### Schema Naming Pattern

All Pydantic schemas must use a consistent suffix that makes intent unambiguous:

```python
RoundSubmitRequest     # Body of POST /round/submit
RoundSubmitResponse    # Returned from POST /round/submit
RoundStartResponse     # Returned from POST /round/start
RoundListResponse      # Returned when listing rounds
RoundAttemptResponse   # Returned for attempt history
StatsResponse          # Returned from GET /stats/me
```

#### Service Function Naming

Service functions are always named with an imperative verb prefix. This makes the call-site self-documenting:

```python
submit_round(args: SubmitRoundArgs) -> RoundSubmitResponse
start_round(args: StartRoundArgs) -> RoundStartResponse
get_round_by_id(round_id: str) -> dict
get_rounds() -> list[RoundInfo]
get_round_attempts(session: Session, user_id: str, round_id: str) -> list[AttemptInfo]
get_user_stats(session: Session, user_id: str) -> StatsResponse
```

### 3.2 Frontend — TypeScript

| Construct | Convention | Example |
|---|---|---|
| React Components | `PascalCase` | `RoundCard.tsx` |
| Custom Hooks | `camelCase` + `use` prefix | `useRounds.ts` |
| Service files | `camelCase` + `Service` suffix | `roundService.ts` |
| Type / Interface files | `camelCase` + `.types` suffix | `round.types.ts` |
| Interface names | `PascalCase` + `I` prefix | `IRound`, `IAttempt` |
| Type aliases | `PascalCase` | `ApiResponse<T>` |
| Enum names | `PascalCase` | `RoundDifficulty` |
| Enum values | `SCREAMING_SNAKE_CASE` | `RoundDifficulty.HARD` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_PROMPT_LENGTH` |
| Event handlers | `camelCase` + `handle` prefix | `handleSubmitPrompt()` |
| Boolean variables | `camelCase` + `is`/`has` prefix | `isLoading`, `hasError` |
| Test files | `.test` or `.spec` suffix | `RoundCard.test.tsx` |

---

## 4. Constants

Constants are not magic strings. Every domain owns its constants in a dedicated file — never inline string literals in service or transport code. This makes log searching, feature flagging, and grep-based debugging reliable.

### 4.1 App-Wide Constants

`app/constants.py` holds logging channels shared across the application. A channel identifies the subsystem in log aggregation tools (e.g. Datadog, CloudWatch).

```python
# app/constants.py

# Logging channels — used as the 'channel' key in every structured log
ROUND_CHANNEL   = 'promptcraft.round'
AUTH_CHANNEL    = 'promptcraft.auth'
STATS_CHANNEL   = 'promptcraft.stats'
AI_CHANNEL      = 'promptcraft.ai'
```

### 4.2 Domain-Level Constants

Each domain folder contains a `constants.py` that defines the feature name strings used in structured logs for that domain. Feature names follow the pattern `VERB_ENTITY_FEATURE_NAME` and are always imported — never typed inline.

```python
# app/round/constants.py
from app.constants import ROUND_CHANNEL

CHANNEL = ROUND_CHANNEL

# Feature names — one constant per service operation
SUBMIT_ROUND_FEATURE          = 'submit_round'
START_ROUND_FEATURE           = 'start_round'
GET_ROUND_FEATURE             = 'get_round'
GET_ROUNDS_FEATURE            = 'get_rounds'
GET_ROUND_ATTEMPTS_FEATURE    = 'get_round_attempts'
GET_ROUND_HISTORY_FEATURE     = 'get_round_history'
```

> **Why This Matters**
>
> Channels and feature names are the primary keys for filtering logs in production. If they are inline strings, typos produce silent blind spots in observability. If they are imported constants, a typo is a `NameError` caught at import time. Always import — never hardcode channel or feature strings at the call site.

---

## 5. Error Handling

### 5.1 Error Architecture Overview

Errors flow in one direction: services raise typed domain exceptions, the transport layer catches them and converts them to HTTP responses. Nothing leaks raw exceptions to the client. The architecture has three components: a base exception hierarchy, per-domain error enums, and a global FastAPI exception handler.

```
Service raises SubmitRoundException(RoundError.NOT_FOUND)
         ↓
Transport catches SubmitRoundException  →  returns 404 envelope
         ↓ (if unexpected)
Transport catches Exception              →  logs + returns 500 with UNKNOWN_ERROR
```

### 5.2 Base Exception Hierarchy

All application exceptions inherit from `AppException`. `BaseErrorCodeEnum` is the parent of every domain error enum and ensures every error has a string `code` attribute.

```python
# app/exceptions.py
from enum import Enum

class BaseErrorCodeEnum(str, Enum):
    """Parent of all domain error enums. Inheriting from str
    makes values JSON-serialisable without extra conversion."""
    pass

class AppException(Exception):
    """Base for all typed application exceptions."""
    def __init__(self, error: BaseErrorCodeEnum, status_code: int = 500, message: str | None = None) -> None:
        self.error       = error
        self.status_code = status_code
        self.message     = message or str(error.value)
        super().__init__(self.message)
```

### 5.3 Domain Error Enums & Exception Classes

Every domain defines its own error enum and a set of exception classes — one per operation. This gives each failure a stable, searchable code and a clear origin.

```python
# app/round/exceptions.py
from app.exceptions import BaseErrorCodeEnum, AppException

class RoundError(BaseErrorCodeEnum):
    UNKNOWN_ERROR       = 'UNKNOWN_ERROR'
    NOT_FOUND           = 'ROUND_NOT_FOUND'
    GENERATION_FAILED   = 'ROUND_GENERATION_FAILED'
    GENERATION_TIMEOUT  = 'ROUND_GENERATION_TIMEOUT'
    NO_API_KEY          = 'ROUND_NO_API_KEY'
    SAVE_FAILED         = 'ROUND_SAVE_FAILED'

# One exception class per service operation
class SubmitRoundException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            RoundError.NOT_FOUND: 404,
            RoundError.GENERATION_FAILED: 502,
            RoundError.GENERATION_TIMEOUT: 504,
            RoundError.NO_API_KEY: 500,
            RoundError.SAVE_FAILED: 500,
        }
        super().__init__(error, status_map.get(error, 500), message)

class StartRoundException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            RoundError.NOT_FOUND: 404,
            RoundError.SAVE_FAILED: 500,
        }
        super().__init__(error, status_map.get(error, 500), message)

class GetRoundAttemptsException(AppException):
    def __init__(self, error: RoundError = RoundError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status = 404 if error == RoundError.NOT_FOUND else 500
        super().__init__(error, status, message)
```

```python
# app/auth/exceptions.py
from app.exceptions import BaseErrorCodeEnum, AppException

class AuthError(BaseErrorCodeEnum):
    UNKNOWN_ERROR       = 'UNKNOWN_ERROR'
    INVALID_CREDENTIALS = 'AUTH_INVALID_CREDENTIALS'
    SERVICE_UNAVAILABLE = 'AUTH_SERVICE_UNAVAILABLE'
    INVALID_TOKEN       = 'AUTH_INVALID_TOKEN'

class LoginException(AppException):
    def __init__(self, error: AuthError = AuthError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            AuthError.INVALID_CREDENTIALS: 401,
            AuthError.SERVICE_UNAVAILABLE: 503,
        }
        super().__init__(error, status_map.get(error, 500), message)

class RegisterException(AppException):
    def __init__(self, error: AuthError = AuthError.UNKNOWN_ERROR, message: str | None = None) -> None:
        status_map = {
            AuthError.INVALID_CREDENTIALS: 409,
            AuthError.SERVICE_UNAVAILABLE: 503,
        }
        super().__init__(error, status_map.get(error, 500), message)
```

### 5.4 Global Exception Handler

A single handler in `main.py` converts all `AppException` subclasses into the standard API envelope. Transport routes never build error responses manually — they only raise.

```python
# app/main.py
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data":    None,
            "error":   exc.error.value,   # stable machine-readable code
            "message": str(exc),           # human-readable detail
        }
    )
```

### 5.5 Transport Error Flow

Every route handler follows the same three-block pattern: happy path, domain exception, unknown exception. Unknown exceptions are always logged before re-raising.

```python
# app/round/transport/submit_endpoint.py
from ..constants import CHANNEL, SUBMIT_ROUND_FEATURE
from ..types.args import SubmitRoundArgs

def submit_endpoint(
    body:         RoundSubmitRequest,
    current_user: UserResponse = Depends(get_current_user),
    session:      Session      = Depends(get_db_session),
) -> ApiResponse[RoundSubmitResponse]:
    try:
        args = SubmitRoundArgs(
            user_email=current_user.email,
            round_id=body.round_id,
            user_prompt=body.user_prompt,
        )
        result = submit_round(session=session, args=args)
        return ApiResponse(data=result)

    except AppException:
        raise  # Already typed — global handler takes over

    except Exception as exc:
        logger.error(
            "Unexpected error in submit_round",
            extra={
                "channel": CHANNEL,
                "feature": SUBMIT_ROUND_FEATURE,
                "error":   str(exc),
            }
        )
        raise SubmitRoundException(RoundError.UNKNOWN_ERROR) from exc
```

### 5.6 Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Transport (endpoints) | Catches domain exceptions (re-raises) and unknown exceptions (logs then wraps). Never builds error JSON manually. |
| Service | Raises typed domain exception subclasses for all business rule violations. Never raises plain `Exception`. |
| Data | Raises domain exceptions when a record is absent or persistence fails. Never returns `None` for an expected record. |
| Adapter | Wraps SDK/network errors in `AppException`. Never leaks third-party exception types upward. |

### 5.7 Frontend — Error Handling

The frontend mirrors the backend's discipline. Service functions are the only place that touch HTTP error handling — components receive a typed result and render accordingly.

```typescript
// types/api.types.ts
export interface ApiResponse<T> {
  data:    T | null;
  error:   string | null;   // machine-readable error code from backend
  message: string | null;   // human-readable detail
}

// services/roundService.ts
export const submitRound = async (payload: ISubmitPayload): Promise<ApiResponse<IRoundResult>> => {
  try {
    const res = await axios.post<ApiResponse<IRoundResult>>('/api/round/submit', payload);
    return res.data;
  } catch (err: unknown) {
    const apiError = err instanceof AxiosError
      ? err.response?.data?.error ?? 'UNKNOWN_ERROR'
      : 'UNKNOWN_ERROR';
    return { data: null, error: apiError, message: 'Request failed' };
  }
};
```

> **Rules**
>
> - Never use a bare `except: pass` or an empty `catch` block.
> - Never raise a plain `Exception` from a service — use a typed domain exception.
> - Never build error JSON manually in a route — raise and let the global handler respond.
> - Frontend: never use `alert()` as the sole error signal. Render an error state in the UI.

---

## 6. Logging Standards

Structured logging is a first-class concern. Every log entry must be machine-parseable so it can be filtered, aggregated, and alerted on in production. Ad-hoc `print()` calls and unstructured log strings are not permitted.

### 6.1 Required Log Fields

| Field | Description |
|---|---|
| `channel` | The subsystem emitting the log. Always imported from the domain `constants.py`. Example: `promptcraft.round` |
| `feature` | The specific operation. Always imported from the domain `constants.py`. Example: `submit_round` |
| `user` | The user's `log_attributes` dict. Omit only in anonymous/unauthenticated contexts. |
| `error` | The string representation of the exception. Present only on error paths. |
| `entity` | The entity's `log_attributes` dict. Present when a model instance is in scope. |

### 6.2 Logging Call Pattern

Every service function logs two events: one on success and one on error. The unknown exception path in the transport layer also logs before re-raising.

```python
# app/round/service/submit_round.py
import logging
from ..constants import CHANNEL, SUBMIT_ROUND_FEATURE
from ..exceptions import SubmitRoundException, RoundError

logger = logging.getLogger(__name__)

def submit_round(session: Session, args: SubmitRoundArgs) -> RoundSubmitResponse:
    try:
        # ... business logic ...

        logger.info(
            "Round submitted successfully",
            extra={
                "channel": CHANNEL,
                "feature": SUBMIT_ROUND_FEATURE,
                "user":    args.user_email,
                "attempt": attempt.log_attributes,
            }
        )
        return result

    except SubmitRoundException:
        raise

    except Exception as exc:
        logger.error(
            "Unexpected error submitting round",
            extra={
                "channel": CHANNEL,
                "feature": SUBMIT_ROUND_FEATURE,
                "user":    args.user_email,
                "error":   str(exc),
            }
        )
        raise SubmitRoundException(RoundError.UNKNOWN_ERROR) from exc
```

### 6.3 `log_attributes` on Models

Every SQLAlchemy model exposes a `log_attributes` property that returns a typed dict of the fields relevant for logging. This is the only way entity data enters a log entry — never build ad-hoc dicts inline at the log call site.

```python
# app/round/types/log_attributes.py
from typing import TypedDict

class AttemptLogAttributes(TypedDict):
    attempt_id:    str
    user_id:       str
    round_id:      str
    attempt_number: int
    similarity_score: float

class RoundUserLogAttributes(TypedDict):
    user_id: str
    email:   str
```

```python
# app/round/data/entities.py
from app.round.types.log_attributes import AttemptLogAttributes

class Attempt(Base):
    __tablename__ = 'attempts'
    # ... columns ...

    @property
    def log_attributes(self) -> AttemptLogAttributes:
        return AttemptLogAttributes(
            attempt_id=self.id,
            user_id=self.user_id,
            round_id=self.round_id,
            attempt_number=self.attempt_number,
            similarity_score=self.similarity_score,
        )
```

> **Rule: `log_attributes` Is the Only Log Source for Entity Data**
>
> - `extra={'attempt_id': attempt.id, 'score': attempt.similarity_score}` — never construct ad-hoc dicts.
> - `extra={'attempt': attempt.log_attributes}` — always use the model property.
>
> The TypedDict ensures consistency and makes log shape changes traceable.

### 6.4 Typed Args Dataclasses

Service and data functions accept `*Args` dataclasses rather than raw keyword arguments. This creates an explicit, typed contract at every layer boundary and makes it easy to trace what data flows into an operation.

```python
# app/round/types/args.py
from dataclasses import dataclass

@dataclass
class SubmitRoundArgs:
    user_email:  str
    round_id:    str
    user_prompt: str

@dataclass
class StartRoundArgs:
    user_id: str
```

```python
# In transport endpoint:
args = SubmitRoundArgs(
    user_email=current_user.email,
    round_id=body.round_id,
    user_prompt=body.user_prompt,
)
result = submit_round(session=session, args=args)

# In service:
def submit_round(session: Session, args: SubmitRoundArgs) -> RoundSubmitResponse: ...
```

> **Why Dataclasses Over Kwargs**
>
> - Kwargs are untyped at the boundary — a typo is a silent bug at runtime.
> - Dataclasses are validated by mypy and visible in IDE autocomplete.
> - Adding a field to `SubmitRoundArgs` surfaces all callers that need updating.

### 6.5 Log Levels

| Level | When to use |
|---|---|
| `logger.info(...)` | Successful completion of a service operation. |
| `logger.warning(...)` | Recoverable issue or unexpected input that did not cause failure. |
| `logger.error(...)` | Unexpected exception caught in transport. Always include `'error': str(e)`. |
| `logger.debug(...)` | Development-only detail. Must be gated — never left in production paths. |

> **`print()` Is Forbidden**
>
> Using `print()` for logging is a code review failure. Use Python's `logging` module in all backend code. Frontend: use `console.warn` or `console.error` in development mode only, never in production.

---

## 7. API Response Conventions

### 7.1 Standard Envelope

Every API response — success or failure — uses the same JSON envelope. This allows the frontend to handle all responses uniformly without inspecting HTTP status codes for message content.

```json
{
  "data":    "<T> | null",
  "error":   "string | null",
  "message": "string | null"
}
```

> **Invariants**
>
> - If `data` is non-null, `error` must be `null`.
> - If `error` is non-null, `data` must be `null`.
> - `error` values are always enum codes (e.g. `ROUND_NOT_FOUND`), never freeform strings.
> - `message` may be set independently on either success or error responses.

### 7.2 Success Examples

```json
// POST /round/submit — 200 OK
{
  "data":    { "generated_image_url": "https://...", "similarity_score": 72.5 },
  "error":   null,
  "message": null
}

// GET /stats/me — 200 OK
{
  "data":    { "rounds_played": 5, "average_score": 68.3, "best_score": 92.1 },
  "error":   null,
  "message": null
}

// GET /round/rounds — 200 OK
{
  "data":    [
    { "id": "ancient-temple", "title": "Ancient Temple", "difficulty": "medium", "reference_image": "ancient-temple.jpg" }
  ],
  "error":   null,
  "message": null
}
```

### 7.3 Error Examples

```json
// POST /round/submit with invalid round — 404 Not Found
{
  "data":    null,
  "error":   "ROUND_NOT_FOUND",
  "message": "Round with id 'nonexistent' not found."
}

// POST /round/submit when Leonardo API fails — 502 Bad Gateway
{
  "data":    null,
  "error":   "ROUND_GENERATION_FAILED",
  "message": "Image generation failed."
}

// POST /auth/login with bad credentials — 401 Unauthorized
{
  "data":    null,
  "error":   "AUTH_INVALID_CREDENTIALS",
  "message": "Invalid email or password."
}
```

### 7.4 HTTP Status Code Reference

| Status Code | Meaning | When to use |
|---|---|---|
| 200 OK | Success | GET, POST (round submit/start) success |
| 201 Created | Resource created | POST /auth/register success |
| 400 Bad Request | Malformed request | Invalid JSON or missing fields |
| 401 Unauthorized | Not authenticated | Missing or invalid token |
| 403 Forbidden | Not authorized | Authenticated but lacks permission |
| 404 Not Found | Resource absent | Round or record does not exist |
| 500 Internal | Unhandled exception | Unknown server error |
| 502 Bad Gateway | Upstream failure | Leonardo API or auth service failure |
| 503 Unavailable | Service down | Auth service unreachable |
| 504 Gateway Timeout | Upstream timeout | Leonardo generation polling expired |

---

## 8. AI Adapter Pattern

### 8.1 Architecture Principle

Services never import from external AI SDKs or make raw HTTP calls to AI services directly. All AI calls go through an adapter in `/adapters`. This enforces a single integration point, keeps business logic free of SDK/HTTP concerns, and makes the AI provider swappable without touching service code.

> **Dependency Rule**
>
> - `submit_round.py` → `LeonardoAdapter` → Leonardo HTTP API
> - `submit_round.py` → Leonardo HTTP API (direct call) **WRONG**
>
> If Leonardo is replaced with another image generation provider, only `leonardo_adapter.py` changes.

### 8.2 Base Adapter Interface

```python
# adapters/base_ai_adapter.py
from abc import ABC, abstractmethod

class BaseImageGenerationAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate an image from the given prompt. Return the image URL."""
        ...

class BaseScoringAdapter(ABC):
    @abstractmethod
    def compute_similarity(self, reference_image_path: str, generated_image_url: str) -> float:
        """Compute similarity between a reference image and a generated image.
        Returns a score from 0.0 to 100.0."""
        ...
```

### 8.3 Leonardo Adapter Implementation

```python
# adapters/leonardo_adapter.py
from app.adapters.base_ai_adapter import BaseImageGenerationAdapter
from app.exceptions import AppException
from app.round.exceptions import RoundError

class LeonardoAdapter(BaseImageGenerationAdapter):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def generate(self, prompt: str) -> str:
        try:
            # ... Leonardo HTTP calls, polling logic ...
            return image_url
        except Exception as e:
            raise AppException(RoundError.GENERATION_FAILED, 502) from e
```

### 8.4 Service Usage

```python
# app/round/service/submit_round.py
def submit_round(
    session: Session,
    args: SubmitRoundArgs,
    image_generator: BaseImageGenerationAdapter,
    scorer: BaseScoringAdapter,
) -> RoundSubmitResponse:
    image_url = image_generator.generate(args.user_prompt)
    score = scorer.compute_similarity(reference_path, image_url)
    # ... save and return ...
```

---

## 9. Testing Standards

### 9.1 Strategy Overview

| Layer | Tools | What it tests |
|---|---|---|
| Unit | Pytest + unittest.mock | Every function in transport, service, and data layers in isolation with mocked dependencies |
| Integration | Pytest + FastAPI TestClient | Full transport → service → data cycle with test DB |

All test layers run in GitHub Actions CI on every pull request. A PR cannot be merged if any test layer is failing.

### 9.2 Unit Test Structure & Rules

Unit tests are the primary safety net for each layer. The following rules apply universally:

- **One test class per source file.** `submit_round.py` → `TestSubmitRound`. `save_submission.py` → `TestSaveSubmission`.
- **One test function per method per flow.** Every public function must have at minimum one test for the happy path and one test for each distinct failure mode.
- **All dependencies are mocked.** No layer test may touch a real database, real HTTP connection, or real external service. Use `MagicMock` for sync dependencies.
- **Side effects model real failure.** Bad-path tests set `side_effect` on mocks to raise the exact typed exception the real dependency would raise — not a generic `Exception`.
- **Assertions are specific.** Every test asserts the return value shape, the exception type, the exception error code, and — where relevant — that a downstream mock was called with the correct arguments.

#### Test file locations mirror source structure

```
app/round/transport/submit_endpoint.py    →  tests/unit/round/transport/test_submit_endpoint.py
app/round/service/submit_round.py         →  tests/unit/round/service/test_submit_round.py
app/round/data/save_submission.py         →  tests/unit/round/data/test_save_submission.py
app/adapters/leonardo_adapter.py          →  tests/unit/adapters/test_leonardo_adapter.py
```

---

### 9.3 Transport Layer Unit Tests

Transport tests mock the entire service layer. They verify that: the endpoint calls the correct service function with correctly constructed args; it returns the expected HTTP status and envelope shape on success; it re-raises domain exceptions unchanged; and it wraps unknown exceptions into the correct typed domain exception before re-raising.

```python
# tests/unit/round/transport/test_submit_endpoint.py
import pytest
from unittest.mock import MagicMock, patch
from app.round.exceptions import SubmitRoundException, RoundError

class TestSubmitEndpoint:

    # ── POST /round/submit ────────────────────────────────────────────────

    def test_submit_returns_200_and_envelope_on_success(self):
        # mock service, call endpoint, assert envelope shape
        ...

    def test_submit_calls_service_with_correct_args(self):
        # verify SubmitRoundArgs constructed from request body + current_user
        ...

    def test_submit_returns_404_when_service_raises_not_found(self):
        # mock service to raise SubmitRoundException(RoundError.NOT_FOUND)
        ...

    def test_submit_returns_502_when_generation_fails(self):
        # mock service to raise SubmitRoundException(RoundError.GENERATION_FAILED)
        ...

    def test_submit_returns_500_and_wraps_unknown_exception(self):
        # mock service to raise RuntimeError, verify UNKNOWN_ERROR envelope
        ...

    def test_submit_returns_401_when_unauthenticated(self):
        # call without auth header, verify 401
        ...
```

---

### 9.4 Service Layer Unit Tests

Service tests mock the data layer and adapters. They verify business logic: argument construction, orchestration order, successful return values, and that the correct typed exception is raised for each business rule violation.

```python
# tests/unit/round/service/test_submit_round.py
import pytest
from unittest.mock import MagicMock, patch
from app.round.service.submit_round import submit_round
from app.round.exceptions import SubmitRoundException, RoundError
from app.round.types.args import SubmitRoundArgs

class TestSubmitRound:

    def test_submit_round_returns_response_on_success(self):
        # mock get_round_by_id, generate_image, compute_similarity, save_submission
        # assert SubmitResponse with correct url and score
        ...

    def test_submit_round_raises_not_found_for_invalid_round(self):
        # mock get_round_by_id to return None
        # assert SubmitRoundException with RoundError.NOT_FOUND
        ...

    def test_submit_round_raises_generation_failed_on_adapter_error(self):
        # mock image_generator.generate to raise
        # assert SubmitRoundException with RoundError.GENERATION_FAILED
        ...

    def test_submit_round_returns_zero_score_when_clip_fails(self):
        # mock scorer.compute_similarity to raise
        # assert result.similarity_score == 0.0
        ...

    def test_submit_round_raises_save_failed_on_db_error(self):
        # mock save_submission to raise
        # assert SubmitRoundException with RoundError.SAVE_FAILED
        ...
```

---

### 9.5 Data Layer Unit Tests

Data layer tests mock the SQLAlchemy session directly. They verify that the correct ORM calls are made with the correct arguments, that the function raises the appropriate domain exception when a record is absent, and that unexpected DB errors are wrapped and re-raised.

```python
# tests/unit/round/data/test_save_submission.py
import pytest
from unittest.mock import MagicMock
from app.round.data.save_submission import save_submission

class TestSaveSubmission:

    def test_save_submission_commits_all_records(self):
        # mock session, verify add/commit calls
        ...

    def test_save_submission_raises_on_db_error(self):
        # mock session.commit to raise, verify domain exception
        ...
```

---

### 9.6 Integration Tests

Integration tests exercise the full transport → service → data pipeline with a real SQLite test database. No mocks. They validate HTTP status codes, the complete response envelope, and persisted state.

```python
# tests/integration/transport/test_round_routes.py
def test_submit_round_returns_200_with_envelope():
    response = client.post('/round/submit', json=submit_payload(), headers=auth_header())
    assert response.status_code == 200
    body = response.json()
    assert body['data']['generated_image_url'] is not None
    assert body['error'] is None

def test_submit_round_returns_404_for_invalid_round():
    response = client.post('/round/submit', json={"round_id": "nonexistent", "user_prompt": "test"}, headers=auth_header())
    assert response.status_code == 404
    assert response.json()['error'] == 'ROUND_NOT_FOUND'

def test_get_stats_returns_aggregated_data():
    # play some rounds first
    response = client.get('/stats/me', headers=auth_header())
    assert response.status_code == 200
    assert response.json()['data']['rounds_played'] >= 0
```

---

### 9.7 Coverage Requirements

| Layer | Minimum |
|---|---|
| Service layer (backend) | 90% line coverage |
| Data layer (backend) | 80% line coverage |
| Adapter layer (backend) | 80% line coverage |
| Transport layer (backend) | 80% line coverage |

---

## 10. Git & CI/CD Conventions

### 10.1 Branch Naming

| Prefix | Example |
|---|---|
| `feature/` | `feature/stats-and-round-history-endpoint` |
| `fix/` | `fix/clip-scoring-zero-division` |
| `chore/` | `chore/update-dependencies` |
| `test/` | `test/add-integration-submit-round` |
| `docs/` | `docs/update-engineering-standards` |

### 10.2 Commit Message Format

Commits must follow [Conventional Commits](https://www.conventionalcommits.org). This enables automatic changelog generation and makes git history scannable.

```
<type>(<scope>): <short summary>

Types:  feat | fix | chore | test | docs | refactor | perf
Scope:  round | auth | stats | ai | db | ci

feat(round):    add round attempt history endpoint
fix(auth):      handle expired tokens from auth service
test(round):    add integration tests for POST /round/submit
chore(db):      add alembic migration for attempts table
```

### 10.3 CI Pipeline

| Stage | What runs |
|---|---|
| Stage 1 — Lint | flake8 (backend) \| ESLint, Prettier (frontend) |
| Stage 2 — Unit Tests | `pytest tests/unit/` (backend) |
| Stage 3 — Integration Tests | `pytest tests/integration/` against SQLite test DB |
| Stage 4 — Coverage Gate | Fails build if any layer falls below configured thresholds |

> **Branch Protection Rules**
>
> - Direct pushes to `main` are disabled. All changes go through PRs.
> - At least 1 peer review approval is required before merge.
> - All CI stages must be green before the Merge button is enabled.
> - Squash merge is preferred — keeps `main` history linear and readable.
