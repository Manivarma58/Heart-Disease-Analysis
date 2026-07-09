# CardioViz - Heart Disease Analytics Platform

CardioViz is a Flask-based healthcare analytics platform for cardiovascular risk analysis. It includes seeded patient data, role-based dashboards, Tableau embed hooks, risk scoring, and SQL assets for a PostgreSQL-ready implementation.

The project now includes the real dataset file at `data/Heart_new2.csv` and an importer that maps it into the application database schema.

---

## Technologies & Frameworks Used

CardioViz is built using a modern, lightweight, and secure technology stack:

### 1. Backend & Frameworks
* **Python 3**: Core backend programming language.
* **Flask**: Micro-framework handling routing, controller logic, modular Blueprints, and session management.
* **SQLite 3**: Database engine used locally for storage. Implements normalized schemas, database triggers, indexes, and custom SQL reporting views.
* **Werkzeug Security**: Cryptographic password hashing (`pbkdf2:sha256`) for secure credential storage.

### 2. Frontend & Styling
* **HTML5 & Jinja2 Templates**: Server-side templating engine for modular HTML structures.
* **Vanilla CSS3**: Tailored styling using custom HSL/RGB colors, responsive flex and grid layouts, glassmorphism, and interactive micro-animations.
* **Lucide Icons**: Premium, lightweight vector icons loaded dynamically.
* **Google Fonts**: Google's Outfit, Inter, and Poppins typography.

### 3. Data Science & Image Processing
* **Pandas**: Used in data preparation scripts to import, clean, validate, and convert `data/Heart_new2.csv` into database records and clean export datasets.
* **Pillow (PIL)**: Used to process the brand's 3D logo transparency and remove solid backing blocks for the browser favicon tab logo.

### 4. Integrations & Security Verification
* **Google OAuth / GIS Chooser Simulator**: Simulates browser-stored Google accounts using browser `localStorage`. Successfully maps real email accounts used in the browser to internal doctor, patient, public health, and admin system profiles.
* **Real Email Dispatch Verification System**:
  * Utilizes background threading (`threading.Thread`) to send real verification emails without blocking web requests.
  * Connects to **ntfy.sh** POST gateway to send instant email alerts directly to the user's inbox on signup.
  * Protects both signup (Step 3 onboarding verification) and login (2FA authentication screen) with dynamic, time-sensitive 6-digit codes.

---

## Demo Accounts

All accounts use `datavibe123`.

* `doctor@datavibe.local` - Dr. Sharma clinical dashboard (Mani Varma)
* `ramesh@datavibe.local` - public health dashboard (mani varma kalapu)
* `anita@datavibe.local` - patient portal (Mani Varma Patient)
* `admin@datavibe.local` - admin tools (suresh Naik)

---

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

---

## Load the Provided Dataset

```powershell
.\.venv\Scripts\python scripts\validate_and_prepare_dataset.py
.\.venv\Scripts\python scripts\create_tableau_ready_csv.py
.\.venv\Scripts\python scripts\import_heart_csv.py
```

This validates `data/Heart_new2.csv`, creates `data/Heart_new2_clean.csv`, imports the dataset into normalized dashboard tables, and keeps a raw copy in `raw_heart_dataset`.

---

## Tableau Integration

Set these environment variables to embed live Tableau dashboards:

* `TABLEAU_CLINICAL_URL`
* `TABLEAU_PUBLIC_HEALTH_URL`
* `TABLEAU_PATIENT_URL`
* `TABLEAU_DASHBOARD_URL`
* `TABLEAU_STORY_URL`

When the variables are empty, each dashboard shows a native demo visualization instead.

For MySQL and Tableau setup, see `docs/MYSQL_TABLEAU_GUIDE.md`.

---

## Included Architecture

* Flask app factory and blueprints
* Role-based session authentication
* SQLite demo schema mirroring the heart disease dataset
* Seeded patient, clinical, lifestyle, history, and risk assessment data
* Risk calculator service
* REST endpoints for overview and patient search
* Dockerfile and Docker Compose
* SQL views and indexes for analytical reporting

---

## Project Documents

* `docs/FINAL_PROJECT_REPORT.md`
* `docs/MYSQL_TABLEAU_GUIDE.md`
* `docs/DATASET_DB_TABLEAU_READINESS.md`
* `docs/DATA_PREPARATION_FOR_TABLEAU.md`
* `docs/DASHBOARD_DESIGN.md`
* `docs/DATA_STORY.md`
* `docs/CALCULATED_FIELDS_AND_VISUALIZATIONS.md`
* `docs/PUBLISHING_AND_WEB_INTEGRATION.md`
* `docs/DEMO_SCRIPT.md`
* `docs/SUBMISSION_CHECKLIST.md`
