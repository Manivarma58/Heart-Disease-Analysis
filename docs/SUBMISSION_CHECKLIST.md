# Submission Checklist

- Flask application completed.
- Dataset copied into `data/Heart_new2.csv`.
- Dataset imported into SQLite dashboard tables.
- 4,500 raw records loaded into `raw_heart_dataset`.
- 4,500 normalized patient records loaded.
- Clinical dashboard completed.
- Public health dashboard completed.
- Patient dashboard completed.
- Admin screens completed.
- Tableau embed hooks completed.
- MySQL schema and import scripts completed.
- Data preparation document completed.
- Tableau-ready CSV completed.
- Final project report completed.
- Demo script completed.
- README completed with run instructions.
- Dockerfile and Docker Compose included.

## Verification Command

```powershell
.\.venv\Scripts\python scripts\import_heart_csv.py
.\.venv\Scripts\python run.py
```

Then open `http://127.0.0.1:5000`.

## Tableau Preparation Files

- `data/Heart_tableau_ready.csv`
- `docs/DATA_PREPARATION_FOR_TABLEAU.md`
- `scripts/create_tableau_ready_csv.py`
- `scripts/mysql_schema.sql`
