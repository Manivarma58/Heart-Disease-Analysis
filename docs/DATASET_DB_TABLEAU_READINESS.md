# Dataset, Database, and Tableau Readiness

## 1. Acquire Finalized Dataset

### Final Dataset

- Source dataset: `data/Heart_new2.csv`
- Final cleaned dataset: `data/Heart_new2_clean.csv`
- Validation report: `docs/DATASET_VALIDATION_REPORT.json`

### Validation Summary

- Source rows: 4,500
- Final clean rows: 4,494
- Columns: 18
- Missing cells: 0
- Duplicate rows removed: 6
- Invalid rows removed: 0
- Outcome field: `HeartDisease`
- Dataset status: ready for analysis and Tableau visualization

### Relevance to Problem

The dataset is aligned with the heart disease analytics problem because it includes:

- Target outcome: `HeartDisease`
- Demographic fields: `Sex`, `AgeCategory`, `Race`
- Clinical and health indicators: `BMI`, `Stroke`, `Diabetic`, `GenHealth`, `KidneyDisease`, `Asthma`
- Lifestyle indicators: `Smoking`, `AlcoholDrinking`, `PhysicalActivity`, `SleepTime`
- Wellbeing indicators: `PhysicalHealth`, `MentalHealth`, `DiffWalking`

### Reproduce Validation

```powershell
.\.venv\Scripts\python scripts\validate_and_prepare_dataset.py
```

## 2. Storing Data in DB and Performing SQL Operations

### Database Target

The project supports:

- SQLite for local Flask demo
- MySQL for Tableau integration

### SQLite Import

```powershell
.\.venv\Scripts\python scripts\import_heart_csv.py
```

This loads the dataset into:

- `raw_heart_dataset`
- `patients`
- `clinical_measurements`
- `lifestyle_factors`
- `medical_history`
- `risk_assessments`

### MySQL Storage

Use:

- `scripts/mysql_schema.sql`
- `scripts/mysql_load_data.sql`

Main MySQL tables:

- `heart_raw`: original imported data
- `heart_clean`: clean Tableau-ready data with constraints

### SQL Operations Included

The SQL scripts perform:

- Constraint validation
- Index creation
- BMI category transformation
- Heart disease binary flag creation
- General health score transformation
- Population aggregation
- Lifestyle risk aggregation
- Tableau-ready view creation

Important MySQL views:

- `heart_analysis_ready`
- `tableau_population_overview_clean`
- `tableau_lifestyle_risk_clean`
- `tableau_patient_monitoring`

## 3. Connect DB with Tableau

### Connection Steps

1. Open Tableau Desktop.
2. Select `MySQL` connector.
3. Enter host, port, username, and password.
4. Select database `datavibe_heart`.
5. Use these views:
   - `tableau_population_overview_clean`
   - `tableau_lifestyle_risk_clean`
   - `tableau_patient_monitoring`
6. Build dashboards for:
   - Clinical analysis
   - Public health policy analysis
   - Patient monitoring
7. Publish dashboards to Tableau Server, Tableau Cloud, or Tableau Public.
8. Add published URLs to `.env`:
   - `TABLEAU_CLINICAL_URL`
   - `TABLEAU_PUBLIC_HEALTH_URL`
   - `TABLEAU_PATIENT_URL`

### Refresh Mode

For live analysis, use a Tableau live MySQL connection. For faster demos or scheduled reporting, use Tableau extracts and schedule refreshes.

### Security Notes

- Use a read-only MySQL user for Tableau.
- Do not expose admin database credentials in Tableau.
- Restrict Tableau access by dashboard role.
- Use environment variables for Flask embed URLs.
