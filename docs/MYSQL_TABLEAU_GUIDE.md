# MySQL and Tableau Guide

## Files Used

- Dataset: `data/Heart_new2.csv`
- Final cleaned dataset: `data/Heart_new2_clean.csv`
- Tableau-ready dataset: `data/Heart_tableau_ready.csv`
- Validation report: `docs/DATASET_VALIDATION_REPORT.json`
- MySQL schema: `scripts/mysql_schema.sql`
- MySQL import command template: `scripts/mysql_load_data.sql`
- Tableau connection videos:
  - `C:\Users\MANI VARMA\Downloads\Connecting Tableu with Mysql.mp4`
  - `C:\Users\MANI VARMA\Downloads\Mysql Dataset Uplaod.mp4`

## MySQL Setup

1. Open MySQL Workbench.
2. Run `scripts/mysql_schema.sql`.
3. Import `data/Heart_new2.csv` into the `heart_raw` table.
4. Import `data/Heart_new2_clean.csv` into the `heart_clean` table.
5. If using SQL import, enable `local_infile` and adjust the CSV path in `scripts/mysql_load_data.sql`.

## Tableau Setup

1. Open Tableau Desktop.
2. Choose `MySQL` as the connector.
3. Connect to the `datavibe_heart` database.
4. Use these views as Tableau sources:
   - `tableau_visualization_ready`
   - `tableau_population_overview_clean`
   - `tableau_lifestyle_risk_clean`
   - `tableau_patient_monitoring`
5. Build three dashboards:
   - Clinical: age, BMI, diabetes, smoking, stroke, heart disease filters.
   - Policy: disease rate by race, age category, general health, and activity.
   - Patient: BMI, sleep, activity, smoking, and risk status cards.
6. Publish each dashboard to Tableau Public, Tableau Server, or Tableau Cloud.
7. Copy each dashboard embed URL into `.env`:
   - `TABLEAU_CLINICAL_URL`
   - `TABLEAU_PUBLIC_HEALTH_URL`
   - `TABLEAU_PATIENT_URL`

## Flask Dataset Import

Run this to load the CSV into the Flask demo database:

```powershell
.\.venv\Scripts\python scripts\import_heart_csv.py
```

Then run:

```powershell
.\.venv\Scripts\python run.py
```
