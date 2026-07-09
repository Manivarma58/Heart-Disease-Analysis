import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "Heart_new2.csv"
CLEAN = ROOT / "data" / "Heart_new2_clean.csv"
REPORT = ROOT / "docs" / "DATASET_VALIDATION_REPORT.json"

EXPECTED_COLUMNS = [
    "HeartDisease",
    "BMI",
    "Smoking",
    "AlcoholDrinking",
    "Stroke",
    "PhysicalHealth",
    "MentalHealth",
    "DiffWalking",
    "Sex",
    "AgeCategory",
    "Race",
    "Diabetic",
    "PhysicalActivity",
    "GenHealth",
    "SleepTime",
    "Asthma",
    "KidneyDisease",
    "SkinCancer",
]


def validate_row(row):
    errors = []
    yes_no_columns = [
        "HeartDisease",
        "Smoking",
        "AlcoholDrinking",
        "Stroke",
        "DiffWalking",
        "PhysicalActivity",
        "Asthma",
        "KidneyDisease",
        "SkinCancer",
    ]
    for column in yes_no_columns:
        if row[column] not in {"Yes", "No"}:
            errors.append(f"{column} must be Yes/No")
    if row["Sex"] not in {"Male", "Female"}:
        errors.append("Sex must be Male/Female")
    if row["GenHealth"] not in {"Excellent", "Very good", "Good", "Fair", "Poor"}:
        errors.append("Invalid GenHealth")
    try:
        bmi = float(row["BMI"])
        if bmi <= 0 or bmi > 100:
            errors.append("BMI out of expected range")
    except ValueError:
        errors.append("BMI is not numeric")
    for column in ("PhysicalHealth", "MentalHealth"):
        try:
            value = int(row[column])
            if value < 0 or value > 30:
                errors.append(f"{column} out of expected 0-30 range")
        except ValueError:
            errors.append(f"{column} is not integer")
    try:
        sleep = float(row["SleepTime"])
        if sleep < 0 or sleep > 24:
            errors.append("SleepTime out of expected 0-24 range")
    except ValueError:
        errors.append("SleepTime is not numeric")
    return errors


def main():
    with open(SOURCE, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = reader.fieldnames or []

    seen = set()
    cleaned = []
    duplicate_count = 0
    validation_errors = []
    missing_cells = 0

    for index, row in enumerate(rows, start=2):
        missing_cells += sum(1 for value in row.values() if value == "")
        row_errors = validate_row(row)
        if row_errors:
            validation_errors.append({"line": index, "errors": row_errors})
            continue
        fingerprint = tuple(row[column] for column in EXPECTED_COLUMNS)
        if fingerprint in seen:
            duplicate_count += 1
            continue
        seen.add(fingerprint)
        cleaned.append(row)

    with open(CLEAN, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(cleaned)

    report = {
        "source_file": str(SOURCE),
        "clean_file": str(CLEAN),
        "expected_columns_present": columns == EXPECTED_COLUMNS,
        "source_rows": len(rows),
        "clean_rows": len(cleaned),
        "columns": len(columns),
        "missing_cells": missing_cells,
        "duplicate_rows_removed": duplicate_count,
        "invalid_rows_removed": len(validation_errors),
        "heart_disease_distribution": Counter(row["HeartDisease"] for row in cleaned),
        "sex_distribution": Counter(row["Sex"] for row in cleaned),
        "age_category_distribution": Counter(row["AgeCategory"] for row in cleaned),
        "tableau_ready": columns == EXPECTED_COLUMNS and missing_cells == 0 and not validation_errors,
        "validation_errors_sample": validation_errors[:20],
    }

    with open(REPORT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"Cleaned dataset written to {CLEAN}")
    print(f"Validation report written to {REPORT}")
    print(f"Rows: {len(rows)} source, {len(cleaned)} clean")


if __name__ == "__main__":
    main()
