# CardioViz Final Project Report

## Objective

CardioViz analyzes heart disease indicators and presents role-specific insights for a cardiologist, public health officer, and patient.

## Dataset

The project uses `Heart_new2_clean.csv`, containing 4,494 cleaned heart-health records with lifestyle, demographic, and health-condition fields such as BMI, smoking, stroke, age category, diabetic status, physical activity, sleep time, and heart disease outcome.

The CSV is stored inside the project at `data/Heart_new2.csv`. It is imported into both the raw table `raw_heart_dataset` and the normalized application tables.

## Implementation

- Backend: Flask
- Local database: SQLite
- BI database target: MySQL
- Visualization: Tableau-ready views and embedded dashboard URLs
- UI: Responsive CardioViz healthcare dashboard

## Dashboards

### Dr. Sharma

Clinical dashboard for patient risk review, high-risk identification, and lifestyle factor comparison.

### Ramesh

Population dashboard for disease prevalence, public health trends, and resource planning.

### Anita

Patient dashboard for personal score, health indicators, goals, and lifestyle recommendations.

## Risk Model

The app uses a transparent demo cardiovascular risk score based on age, sex, BMI, smoking, diabetes, estimated blood pressure, estimated cholesterol, stroke history, and general health.

## Tableau Integration

The project includes MySQL views designed for Tableau dashboards. Flask can embed published Tableau views through environment variables.

## Future Enhancements

- Add full PostgreSQL or MySQL runtime backend.
- Add real Tableau workbook files after dashboard creation.
- Add secure user registration, 2FA, and complete audit logging.
- Add validated Framingham or ASCVD production calculators.

## Submission Contents

- Web application source code.
- Imported SQLite database with the cleaned real dataset.
- MySQL schema and CSV loading scripts.
- Tableau connection guide.
- Final report.
- Demo script.
- Docker deployment files.
