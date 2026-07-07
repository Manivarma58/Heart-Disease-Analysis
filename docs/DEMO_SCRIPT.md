# DataVibe Demo Script

## 1. Project Introduction

DataVibe is a heart disease analytics platform that combines a Flask web app, a structured database, Tableau-ready MySQL views, and role-specific healthcare dashboards.

## 2. Dataset

Show `data/Heart_new2.csv`. Mention that it contains 4,500 patient-style records with heart disease status, BMI, smoking, alcohol, stroke, age category, race, diabetic status, physical activity, general health, sleep time, kidney disease, and related health indicators.

## 3. Run the Application

```powershell
.\.venv\Scripts\python scripts\import_heart_csv.py
.\.venv\Scripts\python run.py
```

Open `http://127.0.0.1:5000`.

## 4. Demo Accounts

Use password `datavibe123` for all accounts.

- `doctor@datavibe.local`
- `ramesh@datavibe.local`
- `anita@datavibe.local`
- `admin@datavibe.local`

## 5. Dr. Sharma Demo

Log in as `doctor@datavibe.local`.

Show:

- Clinical dashboard
- Risk mix cards
- High-risk patient cards
- Patient search
- Tableau clinical embed placeholder

## 6. Ramesh Demo

Log in as `ramesh@datavibe.local`.

Show:

- Population health dashboard
- Regional indicators
- Lifestyle risk table
- Policy-style Tableau section

## 7. Anita Demo

Log in as `anita@datavibe.local`.

Show:

- Personal health score
- Blood pressure, BMI, activity, and recommendation
- Lifestyle challenge cards

## 8. Admin Demo

Log in as `admin@datavibe.local`.

Show:

- User list
- Dataset upload screen
- Mention CSV validation/import pipeline

## 9. Tableau and MySQL

Open `docs/MYSQL_TABLEAU_GUIDE.md`.

Explain:

- MySQL schema is in `scripts/mysql_schema.sql`
- CSV import template is in `scripts/mysql_load_data.sql`
- Tableau connects to MySQL views
- Flask embeds published Tableau dashboard URLs through `.env`

## 10. Closing

Summarize that the project includes the web app, dataset, database import, analytics dashboards, Tableau integration path, Docker deployment files, documentation, and demo script.
