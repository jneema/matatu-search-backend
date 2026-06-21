# Matatu Search API

Backend for a Nairobi matatu route search engine, focused on the Thika Road corridor. Given an origin and destination stage, it returns direct routes and one-transfer journeys with fares, frequencies, and payment methods.

Live API: **https://matatu-search-backend.onrender.com**  
Interactive docs: **https://matatu-search-backend.onrender.com/docs**

---

## Stack

- **FastAPI** + **asyncpg** — async Python web framework with direct PostgreSQL access
- **PostgreSQL** (Neon) — hosted database
- **Alembic** — schema migrations
- **Structlog** — structured logging

---

## Local setup

**Requirements:** Python 3.12+, PostgreSQL

```bash
git clone https://github.com/jneema/matatu-search-backend
cd matatu-search-backend

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:pass@localhost/matatu_db
ALEMBIC_DB_URL=postgresql+asyncpg://user:pass@localhost/matatu_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_IN_MINUTES=60
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

Run migrations and seed the database:

```bash
alembic upgrade head
python -m seed --direction both
```

Start the server:

```bash
uvicorn app.main:app --reload
```

---

## API endpoints

### Search

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/search` | Find matatu routes between two stages |

Query params: `origin`, `destination` (stage name, area, or alias — fuzzy matched), `session_id` (optional).

Returns direct routes and up to 5 one-transfer journeys, each with fare (peak/off-peak), frequency, duration, and payment methods.

**Example:**
```
GET /search?origin=pangani&destination=githurai+45
```

---

### Stages

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/stages` | List stages (filter by type, direction, area) |
| `GET` | `/stages/{id}` | Get a single stage |
| `POST` | `/stages` | Create a stage |
| `PATCH` | `/stages/{id}` | Update a stage |
| `DELETE` | `/stages/{id}` | Deactivate a stage |
| `GET` | `/stages/{id}/hours` | Get operating hours |
| `POST` | `/stages/{id}/hours` | Add operating hours |

Stage types: `formal` (official stops), `informal` (panya/bypass routes).

---

### Routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/routes` | List routes (filter by corridor, sacco, express, status) |
| `POST` | `/routes` | Create a route |

---

### SACCOs

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/saccos` | List SACCOs |
| `POST` | `/saccos` | Create a SACCO |

---

## Seed data

The seed script populates the Thika Road corridor with 11 SACCOs, 27 stages, 22 routes, fares, and occupancy data.

```bash
# Preview without writing
python -m seed --direction both --dry-run

# Seed all directions
python -m seed --direction both

# Seed with a specific database URL
python -m seed --url "postgresql://..." --direction both
```

---

## Deployment

Hosted on **Render** with **Neon** PostgreSQL.

**Environment variables to set in Render:**

| Variable | Notes |
|----------|-------|
| `DATABASE_URL` | `postgresql://...` (Neon connection string) |
| `ALEMBIC_DB_URL` | `postgresql+asyncpg://...?ssl=require` |
| `REDIS_URL` | Upstash or other Redis URL |
| `SECRET_KEY` | Random secret |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_IN_MINUTES` | e.g. `60` |
| `ENVIRONMENT` | `production` |
| `LOG_LEVEL` | `INFO` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |

**Start command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Pre-deploy command** (runs migrations automatically on each deploy):
```
alembic upgrade head
```
