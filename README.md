# CardioViz - Heart Disease Analysis

CardioViz is a Flask-based Heart Disease Analysis project for cardiovascular risk exploration. It includes the real heart disease dataset, database import scripts, SQL/MySQL assets, Tableau-ready exports, role-based dashboards, and a public project overview website.

The project supports the full workflow shown in the assignment: data collection, dataset validation, database storage, SQL operations, Tableau connection, data preparation, unique visualizations, and a responsive dashboard.

## Project Structure

```text
Heart_Disease_Analysis/
├── api/                        # Vercel serverless functions entrypoint
│   └── index.py
├── app/                        # Flask application source
│   ├── models/                 # Database models and schemas
│   ├── routes/                 # Blueprint controllers (auth, dashboard, SQL console, etc.)
│   ├── services/               # Heart disease risk calculation engine
│   ├── static/                 # CSS/JS assets and images
│   ├── templates/              # HTML template files
│   ├── utils/                  # Utility functions
│   ├── config.py               # Flask environment configuration
│   └── __init__.py             # Flask App factory
├── Data_Cleaning/              # Cleaned dataset & preprocessing steps for analysis
│   ├── cleaned_heart.csv
│   └── preprocessing_steps.docx
├── data/                       # Local data store containing datasets
│   ├── Heart_new2.csv
│   ├── Heart_new2_clean.csv
│   └── Heart_tableau_ready.csv
├── Dataset/                    # Raw internship dataset and metadata
│   ├── heart.csv
│   └── data_dictionary.xlsx
├── docs/                       # Project documentation pages
│   ├── CALCULATED_FIELDS_AND_VISUALIZATIONS.md
│   ├── DASHBOARD_DESIGN.md
│   └── ...
├── Report/                     # Submission assets (PDF reports, PowerPoint presentations)
│   ├── Project_Report.pdf
│   └── Presentation.pptx
├── scripts/                    # CLI tools for dataset validation, prep, and db import
│   ├── create_tableau_ready_csv.py
│   ├── validate_and_prepare_dataset.py
│   └── import_heart_csv.py
├── SQL/                        # SQL schemas, imports, and analytical queries
│   ├── create_database.sql
│   ├── create_table.sql
│   ├── import_data.sql
│   └── analysis_queries.sql
├── Tableau/                    # Tableau workbooks and dashboard screenshots
│   ├── Heart_Disease_Dashboard.twb
│   ├── Heart_Disease_Dashboard.twbx
│   └── Dashboard_Screenshots/
├── tests/                      # Automated unit and integration tests
├── Dockerfile                  # Containerization files
├── docker-compose.yml
├── requirements.txt            # Python dependencies
├── run.py                      # Flask development server entry point
├── vercel.json                 # Vercel serverless deployment config
└── README.md                   # This README file
```

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
