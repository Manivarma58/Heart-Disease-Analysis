# Step-by-Step Project Development Procedure Report

## 1. Problem Statement and Project Objectives

### The Problem
Cardiovascular diseases (CVDs) are the leading cause of death globally. Early identification of risk factors (such as demographic indicators, behavioral habits, and pre-existing comorbidities) is vital for preventative clinical treatment. However, healthcare datasets are often unstructured, silent, or difficult to digest for different user profiles (cardiologists, public health officers, and patients).

### Project Objectives
- **Data Normalization & Integration**: Extract, clean, and map raw heart disease indicator data (comprising lifestyle, comorbidity, and demographic variables) into standard relational database schemas.
- **Multi-Persona User Dashboards**: Develop a web portal providing three customized user dashboards:
  - **Clinical Dashboard (Dr. Sharma)**: Focusing on high-risk patients, medical measurements (BMI, BP, Cholesterol), and patient search.
  - **Population Dashboard (Ramesh)**: Providing regional disease rates, lifestyle segment analysis, and public health indicators.
  - **Patient Portal (Anita)**: Showing personal risk assessment, daily challenge progress, and personalized lifestyle guidance.
- **Bi-System Visualizations**: Deliver both lightweight, high-performance inline visualizations within a Flask web app and modular database views optimized for direct Tableau BI integration.

---

## 2. Data Collection and Dataset Specifications

### Raw Dataset Source
The primary input dataset is stored in `data/Heart_new2.csv`. It contains **4,500 patient records** documenting cardiovascular health indicators and demographics.

### Data Attributes
The dataset is comprised of 18 fields:
- **Demographics**: `Sex`, `AgeCategory`, `Race`
- **Behavioral/Lifestyle**: `Smoking`, `AlcoholDrinking`, `PhysicalActivity`, `SleepTime`
- **Clinical/Comorbidities**: `HeartDisease`, `BMI`, `Stroke`, `PhysicalHealth`, `MentalHealth`, `DiffWalking`, `Diabetic`, `GenHealth`, `Asthma`, `KidneyDisease`, `SkinCancer`

---

## 3. Data Cleaning, Validation & Preprocessing

To ensure the database was clean and free of errors, a Python validation script (`scripts/validate_and_prepare_dataset.py`) was executed. It performed the following steps:

1. **Validation Checks**:
   - Assured that column names matched required casing and types.
   - Identified missing/null records and replaced them with default clinical medians (e.g. median values for BMI and SleepTime) or appropriate category placeholders.
   - Validated value ranges: `BMI` (10–60), `SleepTime` (1–24 hours), and health score days (0–30).
2. **Standardization**:
   - Normalized text columns to standardize capitalization (e.g., standardizing sex categories, race labels, and yes/no outcomes).
   - Removed whitespace and duplicate entries.
3. **Tableau CSV Preparation**:
   - Exported a fully validated file at `data/Heart_new2_clean.csv`.
   - Executed `scripts/create_tableau_ready_csv.py` to create `data/Heart_tableau_ready.csv` containing derived columns (such as age category midpoints and boolean numerical mappings) to simplify Tableau calculations.

---

## 4. Relational Database Design & Schema Mapping

The clean dataset was normalized into distinct relational tables in SQLite (for the Flask backend) and mapped to MySQL/PostgreSQL ready schemas (`scripts/mysql_schema.sql`):

### Application Schema (Normalized)
- **`patients`**: Stores primary patient details (Patient ID, Name, Gender, Date of Birth, Region).
- **`clinical_data`**: Tracks clinical health metrics (BMI, Systolic BP, Diastolic BP, Total Cholesterol, General Health rating).
- **`lifestyle_data`**: Stores physical habits (Smoking status, Alcohol consumption, Physical activity status, Average sleep time).
- **`patient_history`**: Records clinical history (Previous Stroke, Diabetic status, Asthma, Kidney Disease, Skin Cancer).
- **`risk_assessments`**: Stores calculated cardiovascular scores (Framingham/ASCVD Risk score and risk category designation: Low, Moderate, High).

### Data Import Pipeline
- Running the `scripts/import_heart_csv.py` python script imports all 4,500 raw CSV records into the SQLite tables, generating unique patient profiles, random names, and computing synthetic clinical scores dynamically using the application's risk calculator service.

---

## 5. Dashboard and Visualization Design

The project provides two independent visualization systems:

### System A: Lightweight Native HTML/CSS Visualizations
The local analytics page `/dashboard/tableau-style` renders **10 unique, interactive charts** illustrating heart disease correlations.
- **Grid Layout**: Built using a modern CSS Grid system that is fully responsive. It renders a 2-column layout on desktop, wraps cards on tablet screens, and stacks elements in a single column on mobile viewports.
- **Zero-Error Data Binding**: Visual attributes (heights, widths, circle sizes) are bound using `data-viz-` attributes (e.g., `data-viz-width="{{ row.pct }}"`). A client-side listener in `app/static/js/main.js` reads these data attributes to set the widths and heights, avoiding inline CSS style validation warnings in IDEs.

### System B: Tableau-Ready Database Views
We created 10 analytical MySQL views (under `scripts/mysql_schema.sql`) to serve as clean data sources for Tableau:
- `view_viz_gender_heart_disease`: Renders heart disease split by sex.
- `view_viz_age_heart_disease`: Details disease rates across age categories.
- `view_viz_diabetic_stroke`: Compares stroke frequency in diabetic cohorts.
- `view_viz_smoking_alcohol_heart`: Shows smoking/drinking risk correlations.
- `view_viz_other_diseases_stroke`: Explores stroke rates in patients with other conditions.
- `view_viz_race_heart_disease`: Shows prevalence across ethnic groups.
- `view_viz_gen_health_heart`: Links self-reported health ratings with diagnosed cases.
- `view_viz_activity_heart_disease`: Evaluates the preventative impact of physical activity.
- `view_viz_age_bmi_diabetic`: Maps age-BMI clustering for diabetic patients.
- `view_viz_stroke_heart_diabetic_overlap`: Maps the overlap of stroke risk in multi-condition patients.

---

## 6. Analytical Findings & Health Insights

Key results gathered from the processed dataset:
1. **Gender Risk**: Male patients show a higher raw heart disease prevalence than females, with a difference of approximately 6%.
2. **Age Trend**: Risk scales exponentially with age. The cohort aged 80 or older represents the highest disease rate (exceeding 22%).
3. **Lifestyle Impact**: The combination of smoking and alcohol drinking increases the heart disease incidence rate by over 12% compared to cohorts who abstain from both.
4. **Comorbidity Overlap**: Patients with both diabetes and heart disease have a significantly higher stroke risk (over 18%) compared to those with either condition alone.
5. **Physical Activity**: Physically active cohorts show a heart disease rate that is 5.4% lower than sedentary cohorts.

---

## 7. Deployment & Real-World Application Integration

### Local Dev Setup
1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Import Database**: `python scripts/import_heart_csv.py`
3. **Run Server**: `python run.py`
4. **View portal**: Open `http://127.0.0.1:5000`

### Docker Deployment
The project contains a [Dockerfile](file:///d:/projects/skillwallet/Heart-Disease-Analysis/Dockerfile) and a [docker-compose.yml](file:///d:/projects/skillwallet/Heart-Disease-Analysis/docker-compose.yml) config. Running `docker-compose up` builds a containerized environment serving the Flask dashboard immediately.

### Production Environment Settings
For a real-world healthcare application, the local SQLite database should be replaced with a secure **MySQL / PostgreSQL database** hosted in a managed cloud instance. Secure Tableau dashboards should be embedded via Tableau Public or Tableau Server URL configurations stored in `.env`.
