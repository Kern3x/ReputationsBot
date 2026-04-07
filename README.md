# ReputationsBot

An asynchronous Telegram bot for group reputation management, built with `pyTelegramBotAPI`, `SQLAlchemy 2.x`, and `PostgreSQL`.

## Features

- Increase reputation: `+rep`, `+r`, `+реп`, `+р`
- Decrease reputation: `-rep <reason>`, `-r <reason>`, `-реп <reason>`, `-р <reason>`
- View reputation: `!rep`, `!r`, `!реп`, `!р`, `!info`
- View decrease history: `/history` or `/h` (in reply)
- Decrease threshold: the actor must have reputation `>= 15.0`

## Architecture

- `app/bot.py` - bot initialization and handler registration
- `app/handlers/` - Telegram handlers
- `app/services/` - business logic (commands/rules)
- `app/repos/` - database access layer (race-safe upsert/update)
- `app/models/` - SQLAlchemy models
- `app/db/` - engine/session/healthcheck DB access
- `app/core/` - settings, logging, exception handler
- `alembic/` - schema migrations

## Environment Variables

Copy the template and fill in the token:

```bash
cp .env.example .env
```

Key parameters:

- `TELEGRAM_BOT_TOKEN` - bot token
- `BOT_ID` - Telegram bot ID
- `LOG_LEVEL` - log level (`INFO`, `DEBUG`, ...)
- `POSTGRES_*` - primary database connection settings
- `TEST_DATABASE_URL` - database URL for integration tests

## Run with Docker Compose (Recommended)

```bash
docker compose up --build -d
```

What happens on startup:

- the bot container runs `alembic upgrade head`
- then polling starts

Logs:

```bash
docker compose logs -f bot
```

Stop:

```bash
docker compose down
```

## Local Run (Without Docker)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python start_bot.py
```

## Alembic Migrations

Create a new revision:

```bash
alembic revision -m "describe change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one step:

```bash
alembic downgrade -1
```

## Tests

Unit/async tests:

```bash
pytest -m "not integration" -q
```

Integration tests (PostgreSQL in Docker):

```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from tests
```

## CI

GitHub Actions workflow:

- `.github/workflows/ci.yml`
- job `unit` runs unit tests
- job `integration` starts docker-compose and runs integration tests
