# CardioViz Demo Script

## 1. Project Introduction

CardioViz is a heart disease analytics platform that combines a Flask web app, a structured database, Tableau-ready MySQL views, and role-specific healthcare dashboards.

## 2. Dataset

Show `data/Heart_new2_clean.csv`. Mention that it contains 4,494 cleaned real dataset records with heart disease status, BMI, smoking, alcohol, stroke, age category, race, diabetic status, physical activity, general health, sleep time, kidney disease, and related health indicators.

## 3. Run the Application

```powershell
.\.venv\Scripts\python scripts\import_heart_csv.py
.\.venv\Scripts\python run.py
```

Open `http://127.0.0.1:5000`.

## 4. Demo Accounts

Use password `cardioviz123` for all accounts.

- `doctor@cardioviz.local`
- `ramesh@cardioviz.local`
- `anita@cardioviz.local`
- `admin@cardioviz.local`

## 5. Dr. Sharma Demo

Log in as `doctor@cardioviz.local`.

Show:

- Clinical dashboard
- Risk mix cards
- High-risk patient cards
- Patient search
- Tableau clinical embed placeholder

## 6. Ramesh Demo

Log in as `ramesh@cardioviz.local`.

Show:

- Population health dashboard
- Regional indicators
- Lifestyle risk table
- Policy-style Tableau section

## 7. Anita Demo

Log in as `anita@cardioviz.local`.

Show:

- Personal health score
- Blood pressure, BMI, activity, and recommendation
- Lifestyle challenge cards

## 8. Admin Demo

Log in as `admin@cardioviz.local`.

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

## 10. Heart Disease Story

Open `/story/heart-disease`.

Show:

- Scene 1: dataset context
- Scene 2: gender comparison
- Scene 3: physical activity
- Scene 4: diabetes and stroke
- Scene 5: smoking and alcohol
- Scene 6: conclusion and age trend

## 11. Publishing and Web Integration

Open `/`.

Show:

- Public web application landing page
- About section
- Dashboard embed section
- Story embed section
- Contact/publishing section

Then open:

- `/web-integration/dashboard`
- `/web-integration/story`

Explain that Tableau Public URLs can be configured through `.env`.

## 12. Closing

Summarize that the project includes the web app, dataset, database import, analytics dashboards, Tableau integration path, Docker deployment files, documentation, and demo script.
