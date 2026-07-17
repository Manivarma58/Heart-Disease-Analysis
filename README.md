# CardioViz - Heart Disease Analysis

CardioViz is a Flask-based Heart Disease Analysis project for cardiovascular risk exploration. It includes the real heart disease dataset, database import scripts, SQL/MySQL assets, Tableau-ready exports, role-based dashboards, and a public project overview website.

The project supports the full workflow shown in the assignment: data collection, dataset validation, database storage, SQL operations, Tableau connection, data preparation, unique visualizations, and a responsive dashboard.

## Demo Accounts

All accounts use `cardioviz123`.

- `doctor@cardioviz.local` - Dr. Sharma clinical dashboard
- `ramesh@cardioviz.local` - public health dashboard
- `anita@cardioviz.local` - patient portal
- `admin@cardioviz.local` - admin tools

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

## Load or Refresh the Dataset

```powershell
.\.venv\Scripts\python scripts\validate_and_prepare_dataset.py
.\.venv\Scripts\python scripts\create_tableau_ready_csv.py
.\.venv\Scripts\python scripts\import_heart_csv.py
```

This validates `data/Heart_new2.csv`, creates `data/Heart_new2_clean.csv`, imports the data into normalized dashboard tables, and keeps a raw copy in `raw_heart_dataset`.

## Key Pages

- `/` - CardioViz project overview website
- `/dashboard` - role-based dashboard hub after login
- `/dashboard/tableau-style` - native Tableau-style analytics dashboard
- `/story/heart-disease` - heart disease data story
- `/web-integration/dashboard` - published Tableau dashboard embed area
- `/web-integration/story` - published Tableau story embed area
- `/data/heart-dataset.csv` - dataset download

## Tableau Integration

Set these environment variables to embed live Tableau dashboards:

- `TABLEAU_CLINICAL_URL`
- `TABLEAU_PUBLIC_HEALTH_URL`
- `TABLEAU_PATIENT_URL`
- `TABLEAU_DASHBOARD_URL`
- `TABLEAU_STORY_URL`

When the variables are empty, each dashboard shows a native demo visualization. For MySQL and Tableau setup, see `docs/MYSQL_TABLEAU_GUIDE.md`.

## Included Architecture

- Flask app factory and blueprints
- Role-based session authentication
- SQLite demo schema with MySQL migration scripts
- Real imported clinical, lifestyle, history, and risk assessment data
- Risk calculator service
- REST endpoints for overview and visualization data
- Dockerfile and Docker Compose
- SQL views and indexes for analytical reporting

## Project Documents

- `docs/FINAL_PROJECT_REPORT.md`
- `docs/MYSQL_TABLEAU_GUIDE.md`
- `docs/DATASET_DB_TABLEAU_READINESS.md`
- `docs/DATA_PREPARATION_FOR_TABLEAU.md`
- `docs/DASHBOARD_DESIGN.md`
- `docs/DATA_STORY.md`
- `docs/CALCULATED_FIELDS_AND_VISUALIZATIONS.md`
- `docs/PUBLISHING_AND_WEB_INTEGRATION.md`
- `docs/DEMO_SCRIPT.md`
- `docs/SUBMISSION_CHECKLIST.md`
