# DocOps

AI assistant for business documents — Q&A over invoices and contracts with citations, plus an agent that creates entries with human confirmation.

**Status:** Week 1 — FastAPI skeleton, document CRUD, tests.

## Run
cp .env.example .env   # then edit credentials
docker compose up -d
docker compose exec db createdb -U docops docops_test
uv sync
uv run fastapi dev src/docops/main.py

## Test
uv run pytest

