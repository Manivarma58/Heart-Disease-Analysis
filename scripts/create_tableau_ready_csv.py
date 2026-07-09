import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "Heart_new2_clean.csv"
OUTPUT = ROOT / "data" / "Heart_tableau_ready.csv"


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def age_sort(age_category):
    if "older" in age_category:
        return 80
    return int(age_category.split("-")[0])


def health_score(value):
    return {"Poor": 1, "Fair": 2, "Good": 3, "Very good": 4, "Excellent": 5}[value]


def yes_no_flag(value):
    return 1 if value == "Yes" else 0


def sleep_quality(sleep_time):
    if sleep_time < 6:
        return "Poor (< 6 hrs)"
    if sleep_time <= 9:
        return "Optimal (6-9 hrs)"
    return "Excessive (> 9 hrs)"


def risk_segment(row):
    points = 0
    points += yes_no_flag(row["HeartDisease"]) * 5
    points += yes_no_flag(row["Smoking"]) * 2
    points += yes_no_flag(row["Stroke"]) * 3
    points += 2 if row["Diabetic"] != "No" else 0
    points += yes_no_flag(row["KidneyDisease"]) * 2
    points += 2 if float(row["BMI"]) >= 30 else 0
    points += 1 if row["PhysicalActivity"] == "No" else 0
    points += 1 if health_score(row["GenHealth"]) <= 2 else 0
    if points >= 8:
        return "High"
    if points >= 4:
        return "Moderate"
    return "Low"


def main():
    with open(SOURCE, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    fieldnames = [
        "Record ID",
        "Heart Disease",
        "Heart Disease Flag",
        "BMI",
        "BMI Category",
        "Obesity Flag",
        "Smoking Status",
        "Alcohol Drinking",
        "Stroke History",
        "Physical Health Days",
        "Mental Health Days",
        "Total Unhealthy Days",
        "Difficulty Walking",
        "Sex",
        "Age Category",
        "Age Sort",
        "Race",
        "Diabetic Status",
        "Physical Activity",
        "General Health",
        "General Health Score",
        "Sleep Time",
        "Sleep Quality",
        "Asthma",
        "Kidney Disease",
        "Skin Cancer",
        "Risk Segment",
        "High Risk Flag",
    ]

    with open(OUTPUT, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            bmi = float(row["BMI"])
            sleep_time = float(row["SleepTime"])
            segment = risk_segment(row)
            writer.writerow(
                {
                    "Record ID": index,
                    "Heart Disease": row["HeartDisease"],
                    "Heart Disease Flag": yes_no_flag(row["HeartDisease"]),
                    "BMI": row["BMI"],
                    "BMI Category": bmi_category(bmi),
                    "Obesity Flag": 1 if bmi >= 30 else 0,
                    "Smoking Status": row["Smoking"],
                    "Alcohol Drinking": row["AlcoholDrinking"],
                    "Stroke History": row["Stroke"],
                    "Physical Health Days": row["PhysicalHealth"],
                    "Mental Health Days": row["MentalHealth"],
                    "Total Unhealthy Days": int(row["PhysicalHealth"]) + int(row["MentalHealth"]),
                    "Difficulty Walking": row["DiffWalking"],
                    "Sex": row["Sex"],
                    "Age Category": row["AgeCategory"],
                    "Age Sort": age_sort(row["AgeCategory"]),
                    "Race": row["Race"],
                    "Diabetic Status": row["Diabetic"],
                    "Physical Activity": row["PhysicalActivity"],
                    "General Health": row["GenHealth"],
                    "General Health Score": health_score(row["GenHealth"]),
                    "Sleep Time": row["SleepTime"],
                    "Sleep Quality": sleep_quality(sleep_time),
                    "Asthma": row["Asthma"],
                    "Kidney Disease": row["KidneyDisease"],
                    "Skin Cancer": row["SkinCancer"],
                    "Risk Segment": segment,
                    "High Risk Flag": 1 if segment == "High" else 0,
                }
            )
    print(f"Tableau-ready CSV written to {OUTPUT}")


if __name__ == "__main__":
    main()
