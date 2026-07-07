# DataVibe - Heart Disease Analytics Platform

DataVibe is a Flask-based healthcare analytics demo for cardiovascular risk analysis. It includes seeded patient data, role-based dashboards, Tableau embed hooks, risk scoring, and SQL assets for a PostgreSQL-ready implementation.

The project now includes the real dataset file at `data/Heart_new2.csv` and an importer that maps it into the application schema.

## Demo Accounts

All accounts use `datavibe123`.

- `doctor@datavibe.local` - Dr. Sharma clinical dashboard
- `ramesh@datavibe.local` - public health dashboard
- `anita@datavibe.local` - patient portal
- `admin@datavibe.local` - admin tools

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

## Load the Provided Dataset

```powershell
.\.venv\Scripts\python scripts\validate_and_prepare_dataset.py
.\.venv\Scripts\python scripts\create_tableau_ready_csv.py
.\.venv\Scripts\python scripts\import_heart_csv.py
```

This validates `data/Heart_new2.csv`, creates `data/Heart_new2_clean.csv`, imports the dataset into normalized dashboard tables, and keeps a raw copy in `raw_heart_dataset`.

## Tableau Integration

Set these environment variables to embed live Tableau dashboards:

- `TABLEAU_CLINICAL_URL`
- `TABLEAU_PUBLIC_HEALTH_URL`
- `TABLEAU_PATIENT_URL`

When the variables are empty, each dashboard shows a native demo visualization instead.

For MySQL and Tableau setup, see `docs/MYSQL_TABLEAU_GUIDE.md`.

## Included Architecture

- Flask app factory and blueprints
- Role-based session authentication
- SQLite demo schema mirroring the requested heart disease dataset
- Seeded patient, clinical, lifestyle, history, and risk assessment data
- Risk calculator service
- REST endpoints for overview and patient search
- Dockerfile and Docker Compose
- SQL views and indexes for analytical reporting

## Project Documents

- `docs/FINAL_PROJECT_REPORT.md`
- `docs/MYSQL_TABLEAU_GUIDE.md`
- `docs/DATASET_DB_TABLEAU_READINESS.md`
- `docs/DATA_PREPARATION_FOR_TABLEAU.md`
- `docs/DEMO_SCRIPT.md`
- `docs/SUBMISSION_CHECKLIST.md`
