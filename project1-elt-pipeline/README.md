# Project 1: Currency Exchange Rate ELT Pipeline

A simple ELT (Extract, Load, Transform) pipeline that pulls live currency exchange rates from a public API, transforms the data with pandas, and loads it into a PostgreSQL database — with idempotent reruns.

## Architecture
Public API (open.er-api.com)
↓ extract (requests)
Raw JSON response
↓ transform (pandas)
Clean DataFrame
↓ load (psycopg2)
PostgreSQL (Docker container)


## Tools Used
- **Python 3.12** — extraction, transformation, orchestration
- **pandas** — data transformation
- **requests** — API calls
- **psycopg2** — PostgreSQL connectivity
- **PostgreSQL 16** (via Docker) — data storage
- **python-dotenv** — secure credential management

## Key Design Decisions
- **Credentials are never hardcoded** — all DB connection details are loaded from a `.env` file (excluded from version control via `.gitignore`).
- **Idempotent by design** — the pipeline truncates the target table before each load, so re-running it (manually, on a schedule, or after a retry) never produces duplicate data.
- **Modular structure** — extract, transform, and load are separate functions, making each stage independently testable and reusable.

## How to Run

1. Start PostgreSQL locally via Docker:
```bash
   docker run --name pg-dev -e POSTGRES_PASSWORD=devpassword -e POSTGRES_DB=elt_project -p 5432:5432 -d postgres:16
```

2. Create a `.env` file in this folder:

3. Set up the virtual environment and install dependencies:
```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

4. Run the pipeline:
```bash
   python3 scripts/extract_transform_load.py
```

## Sample Output
Extracted data for base currency: USD
Transformed 166 currency rates
Loaded 166 rows into PostgreSQL
ELT pipeline completed successfully

## Next Steps (Planned Improvements)
- Orchestrate with Apache Airflow for scheduled daily runs
- Add data quality checks (null checks, row count validation)
- Add logging instead of print statements
- Add unit tests for transform logic