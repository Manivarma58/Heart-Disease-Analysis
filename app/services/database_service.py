import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from flask import current_app, g
from werkzeug.security import generate_password_hash

from app.services.risk_calculator import calculate_demo_risk, risk_category


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL,
  persona TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
  patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  date_of_birth TEXT NOT NULL,
  gender TEXT NOT NULL,
  region TEXT NOT NULL,
  urban_rural TEXT NOT NULL,
  occupation TEXT,
  education_level TEXT,
  income_range TEXT
);

CREATE TABLE IF NOT EXISTS clinical_measurements (
  measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL,
  measurement_date TEXT NOT NULL,
  systolic_bp INTEGER NOT NULL,
  diastolic_bp INTEGER NOT NULL,
  cholesterol_total INTEGER NOT NULL,
  cholesterol_hdl INTEGER NOT NULL,
  cholesterol_ldl INTEGER NOT NULL,
  triglycerides INTEGER NOT NULL,
  fasting_blood_sugar INTEGER NOT NULL,
  bmi REAL NOT NULL,
  heart_rate INTEGER NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS lifestyle_factors (
  lifestyle_id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL,
  smoking_status TEXT NOT NULL,
  smoking_duration INTEGER NOT NULL,
  alcohol_consumption TEXT NOT NULL,
  physical_activity TEXT NOT NULL,
  diet_quality TEXT NOT NULL,
  sleep_hours REAL NOT NULL,
  stress_level TEXT NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS medical_history (
  history_id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL,
  diagnosis_date TEXT,
  heart_disease TEXT NOT NULL,
  heart_disease_type TEXT,
  hypertension TEXT NOT NULL,
  diabetes TEXT NOT NULL,
  family_history TEXT NOT NULL,
  previous_cardiac_event TEXT NOT NULL,
  current_medications TEXT,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS risk_assessments (
  assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL,
  assessment_date TEXT NOT NULL,
  framingham_score REAL NOT NULL,
  ascvd_score REAL NOT NULL,
  risk_category TEXT NOT NULL,
  lifestyle_risk_score REAL NOT NULL,
  genetic_risk_score REAL NOT NULL,
  FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_time TEXT NOT NULL,
  user_email TEXT,
  action TEXT NOT NULL,
  resource TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clinical_notes (
  note_id INTEGER PRIMARY KEY AUTOINCREMENT,
  doctor_name TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_heart_dataset (
  raw_id INTEGER PRIMARY KEY AUTOINCREMENT,
  heart_disease TEXT,
  bmi REAL,
  smoking TEXT,
  alcohol_drinking TEXT,
  stroke TEXT,
  physical_health INTEGER,
  mental_health INTEGER,
  diff_walking TEXT,
  sex TEXT,
  age_category TEXT,
  race TEXT,
  diabetic TEXT,
  physical_activity TEXT,
  gen_health TEXT,
  sleep_time REAL,
  asthma TEXT,
  kidney_disease TEXT,
  skin_cancer TEXT
);

CREATE INDEX IF NOT EXISTS idx_patients_region ON patients(region);
CREATE INDEX IF NOT EXISTS idx_risk_category ON risk_assessments(risk_category);
CREATE INDEX IF NOT EXISTS idx_measurements_patient_date ON clinical_measurements(patient_id, measurement_date);
"""


def get_db():
    if "db" not in g:
        db_path = current_app.config["DATABASE_PATH"]
        db_exists = Path(db_path).exists()
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        if not db_exists:
            g.db.executescript(SCHEMA)
            user_count = g.db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if user_count == 0:
                seed_demo_users(g.db)
            patient_count = g.db.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
            if patient_count == 0:
                csv_path = real_dataset_path()
                if csv_path.exists():
                    import_heart_csv(g.db, csv_path)
            g.db.commit()
    return g.db


def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_database():
    pass


def real_dataset_path():
    root = Path(current_app.root_path).parent
    clean = root / "data" / "Heart_new2_clean.csv"
    if clean.exists():
        return clean
    return root / "data" / "Heart_new2.csv"


def seed_demo_users(db):
    users = [
        ("Dr. Sharma", "doctor@datavibe.local", "Cardiologist", "clinical"),
        ("Ramesh Iyer", "ramesh@datavibe.local", "Health Official", "public_health"),
        ("Anita Rao", "anita@datavibe.local", "Patient", "patient"),
        ("Admin User", "admin@datavibe.local", "Admin", "admin"),
    ]
    for name, email, role, persona in users:
        db.execute(
            "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
            (name, email, generate_password_hash("datavibe123"), role, persona),
        )


def seed_demo_data(db, rows=240):
    seed_demo_users(db)
    return

    first_names = ["Aarav", "Anita", "Diya", "Ishaan", "Kavya", "Mohan", "Neha", "Priya", "Rahul", "Sanjay", "Tara", "Vikram"]
    last_names = ["Bose", "Iyer", "Kapoor", "Khan", "Mehta", "Nair", "Patel", "Rao", "Reddy", "Sharma", "Singh", "Verma"]
    regions = ["North", "South", "East", "West", "Central"]
    educations = ["Primary", "Secondary", "Graduate", "Postgraduate"]
    incomes = ["Low", "Lower Middle", "Middle", "Upper Middle", "High"]
    jobs = ["Teacher", "Engineer", "Farmer", "Shop Owner", "Nurse", "Driver", "Homemaker", "Clerk"]

    random.seed(42)
    today = date.today()
    for _ in range(rows):
        age = random.randint(25, 82)
        gender = random.choice(["M", "F", "Other"])
        dob = today.replace(year=today.year - age).isoformat()
        region = random.choice(regions)
        urban_rural = random.choice(["Urban", "Rural"])
        cursor = db.execute(
            """INSERT INTO patients
            (first_name, last_name, date_of_birth, gender, region, urban_rural, occupation, education_level, income_range)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                random.choice(first_names),
                random.choice(last_names),
                dob,
                gender,
                region,
                urban_rural,
                random.choice(jobs),
                random.choice(educations),
                random.choice(incomes),
            ),
        )
        patient_id = cursor.lastrowid
        smoker = random.choices(["Never", "Former", "Current"], [0.55, 0.25, 0.20])[0]
        activity = random.choices(["Sedentary", "Light", "Moderate", "Heavy"], [0.25, 0.35, 0.30, 0.10])[0]
        diet = random.choices(["Poor", "Average", "Good", "Excellent"], [0.20, 0.42, 0.30, 0.08])[0]
        diabetes = random.random() < (0.08 + age / 650)
        systolic = random.randint(105, 178) + (8 if activity == "Sedentary" else 0)
        diastolic = random.randint(68, 104)
        total_chol = random.randint(155, 285) + (14 if diet == "Poor" else 0)
        hdl = random.randint(32, 68)
        bmi = round(random.uniform(19.5, 36.5) + (1.8 if activity == "Sedentary" else 0), 1)
        score = calculate_demo_risk(age, gender, systolic, total_chol, hdl, smoker == "Current", diabetes, bmi)
        category = risk_category(score)

        db.execute(
            """INSERT INTO clinical_measurements
            (patient_id, measurement_date, systolic_bp, diastolic_bp, cholesterol_total, cholesterol_hdl,
             cholesterol_ldl, triglycerides, fasting_blood_sugar, bmi, heart_rate)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                patient_id,
                (today - timedelta(days=random.randint(0, 365))).isoformat(),
                systolic,
                diastolic,
                total_chol,
                hdl,
                max(75, total_chol - hdl - random.randint(25, 55)),
                random.randint(90, 240),
                random.randint(82, 156) + (18 if diabetes else 0),
                bmi,
                random.randint(58, 104),
            ),
        )
        db.execute(
            """INSERT INTO lifestyle_factors
            (patient_id, smoking_status, smoking_duration, alcohol_consumption, physical_activity,
             diet_quality, sleep_hours, stress_level)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                patient_id,
                smoker,
                random.randint(0, 30) if smoker != "Never" else 0,
                random.choice(["None", "Light", "Moderate", "Heavy"]),
                activity,
                diet,
                round(random.uniform(5.1, 8.4), 1),
                random.choice(["Low", "Moderate", "High"]),
            ),
        )
        has_hd = category == "High" or (category == "Moderate" and random.random() < 0.28)
        db.execute(
            """INSERT INTO medical_history
            (patient_id, diagnosis_date, heart_disease, heart_disease_type, hypertension, diabetes,
             family_history, previous_cardiac_event, current_medications)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                patient_id,
                (today - timedelta(days=random.randint(60, 2000))).isoformat() if has_hd else None,
                "Yes" if has_hd else "No",
                random.choice(["Coronary Artery Disease", "Arrhythmia", "Heart Failure"]) if has_hd else None,
                "Yes" if systolic >= 140 else "No",
                "Yes" if diabetes else "No",
                "Yes" if random.random() < 0.31 else "No",
                "Yes" if has_hd and random.random() < 0.25 else "No",
                random.choice(["Statin", "Beta blocker", "ACE inhibitor", "Lifestyle plan", "None"]),
            ),
        )
        db.execute(
            """INSERT INTO risk_assessments
            (patient_id, assessment_date, framingham_score, ascvd_score, risk_category, lifestyle_risk_score, genetic_risk_score)
             VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                patient_id,
                today.isoformat(),
                score,
                round(min(35, score * random.uniform(0.85, 1.15)), 1),
                category,
                round((6 if smoker == "Current" else 1) + (5 if activity == "Sedentary" else 1) + (4 if diet == "Poor" else 1), 1),
                round(random.uniform(1, 10), 1),
            ),
        )


def reset_health_tables(db):
    for table in (
        "raw_heart_dataset",
        "risk_assessments",
        "medical_history",
        "lifestyle_factors",
        "clinical_measurements",
        "patients",
    ):
        db.execute(f"DELETE FROM {table}")


def import_heart_csv(db, csv_path, limit=None):
    reset_health_tables(db)
    with open(csv_path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            if limit and index > limit:
                break
            patient_id = insert_csv_patient(db, index, row)
            insert_csv_raw(db, row)
            insert_csv_clinical(db, patient_id, row)
            insert_csv_lifestyle(db, patient_id, row)
            insert_csv_history(db, patient_id, row)
            insert_csv_risk(db, patient_id, row)
    db.commit()


def insert_csv_raw(db, row):
    db.execute(
        """INSERT INTO raw_heart_dataset
        (heart_disease, bmi, smoking, alcohol_drinking, stroke, physical_health, mental_health,
         diff_walking, sex, age_category, race, diabetic, physical_activity, gen_health,
         sleep_time, asthma, kidney_disease, skin_cancer)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            row["HeartDisease"],
            float(row["BMI"]),
            row["Smoking"],
            row["AlcoholDrinking"],
            row["Stroke"],
            int(row["PhysicalHealth"]),
            int(row["MentalHealth"]),
            row["DiffWalking"],
            row["Sex"],
            row["AgeCategory"],
            row["Race"],
            row["Diabetic"],
            row["PhysicalActivity"],
            row["GenHealth"],
            float(row["SleepTime"]),
            row["Asthma"],
            row["KidneyDisease"],
            row["SkinCancer"],
        ),
    )


def insert_csv_patient(db, index, row):
    age = age_midpoint(row["AgeCategory"])
    gender = "M" if row["Sex"] == "Male" else "F"
    region = region_from_race(row["Race"])
    dob = date(date.today().year - age, 7, 1).isoformat()
    cursor = db.execute(
        """INSERT INTO patients
        (first_name, last_name, date_of_birth, gender, region, urban_rural, occupation, education_level, income_range)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            f"Patient{index:04d}",
            row["Race"].replace(" ", ""),
            dob,
            gender,
            region,
            "Urban" if index % 3 else "Rural",
            "Dataset participant",
            "Not recorded",
            "Not recorded",
        ),
    )
    return cursor.lastrowid


def insert_csv_clinical(db, patient_id, row):
    age = age_midpoint(row["AgeCategory"])
    bmi = float(row["BMI"])
    smoker = row["Smoking"] == "Yes"
    diabetic = row["Diabetic"] != "No"
    poor_health = health_weight(row["GenHealth"])
    systolic = int(108 + age * 0.45 + max(0, bmi - 24) * 1.6 + poor_health * 4 + (8 if smoker else 0))
    diastolic = int(68 + age * 0.12 + max(0, bmi - 24) * 0.65 + poor_health * 2)
    cholesterol_total = int(165 + age * 0.55 + max(0, bmi - 25) * 2.2 + (16 if smoker else 0) + (12 if diabetic else 0))
    hdl = max(32, int(62 - max(0, bmi - 22) * 0.8 - (5 if smoker else 0)))
    db.execute(
        """INSERT INTO clinical_measurements
        (patient_id, measurement_date, systolic_bp, diastolic_bp, cholesterol_total, cholesterol_hdl,
         cholesterol_ldl, triglycerides, fasting_blood_sugar, bmi, heart_rate)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            patient_id,
            date.today().isoformat(),
            systolic,
            diastolic,
            cholesterol_total,
            hdl,
            max(70, cholesterol_total - hdl - 35),
            int(95 + max(0, bmi - 22) * 4 + poor_health * 10),
            92 + (30 if diabetic else 0) + poor_health * 5,
            bmi,
            64 + poor_health * 4 + (5 if smoker else 0),
        ),
    )


def insert_csv_lifestyle(db, patient_id, row):
    db.execute(
        """INSERT INTO lifestyle_factors
        (patient_id, smoking_status, smoking_duration, alcohol_consumption, physical_activity,
         diet_quality, sleep_hours, stress_level)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            patient_id,
            "Current" if row["Smoking"] == "Yes" else "Never",
            10 if row["Smoking"] == "Yes" else 0,
            "Moderate" if row["AlcoholDrinking"] == "Yes" else "None",
            "Moderate" if row["PhysicalActivity"] == "Yes" else "Sedentary",
            diet_from_health(row["GenHealth"]),
            float(row["SleepTime"]),
            stress_from_mental_health(int(row["MentalHealth"])),
        ),
    )


def insert_csv_history(db, patient_id, row):
    heart_disease = row["HeartDisease"]
    db.execute(
        """INSERT INTO medical_history
        (patient_id, diagnosis_date, heart_disease, heart_disease_type, hypertension, diabetes,
         family_history, previous_cardiac_event, current_medications)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            patient_id,
            date.today().isoformat() if heart_disease == "Yes" else None,
            heart_disease,
            "Heart Disease" if heart_disease == "Yes" else None,
            "Yes" if row["Stroke"] == "Yes" or row["DiffWalking"] == "Yes" else "No",
            "Yes" if row["Diabetic"] != "No" else "No",
            "No",
            row["Stroke"],
            medication_from_row(row),
        ),
    )


def insert_csv_risk(db, patient_id, row):
    age = age_midpoint(row["AgeCategory"])
    bmi = float(row["BMI"])
    diabetic = row["Diabetic"] != "No"
    smoker = row["Smoking"] == "Yes"
    clinical_boost = health_weight(row["GenHealth"]) * 2
    score = calculate_demo_risk(
        age,
        "M" if row["Sex"] == "Male" else "F",
        int(112 + age * 0.45 + max(0, bmi - 24) * 1.6),
        int(170 + age * 0.55 + max(0, bmi - 25) * 2.2),
        max(32, int(62 - max(0, bmi - 22) * 0.8)),
        smoker,
        diabetic,
        bmi,
    )
    if row["HeartDisease"] == "Yes":
        score = max(score, 22)
    score = round(min(35, score + clinical_boost), 1)
    category = risk_category(score)
    db.execute(
        """INSERT INTO risk_assessments
        (patient_id, assessment_date, framingham_score, ascvd_score, risk_category, lifestyle_risk_score, genetic_risk_score)
         VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            patient_id,
            date.today().isoformat(),
            score,
            round(min(35, score * 0.96 + (2 if row["Stroke"] == "Yes" else 0)), 1),
            category,
            lifestyle_score(row),
            4.0 + (2.5 if row["KidneyDisease"] == "Yes" else 0) + (2 if row["Stroke"] == "Yes" else 0),
        ),
    )


def age_midpoint(age_category):
    if "older" in age_category:
        return 82
    start, end = age_category.split("-")
    return (int(start) + int(end)) // 2


def region_from_race(race):
    return {
        "White": "North",
        "Black": "South",
        "Asian": "East",
        "American Indian/Alaskan Native": "West",
        "Hispanic": "Central",
        "Other": "Central",
    }.get(race, "Central")


def health_weight(value):
    return {"Excellent": 0, "Very good": 1, "Good": 2, "Fair": 3, "Poor": 4}.get(value, 2)


def diet_from_health(value):
    return {"Excellent": "Excellent", "Very good": "Good", "Good": "Average", "Fair": "Average", "Poor": "Poor"}.get(value, "Average")


def stress_from_mental_health(days):
    if days >= 20:
        return "High"
    if days >= 7:
        return "Moderate"
    return "Low"


def lifestyle_score(row):
    return round(
        (5 if row["Smoking"] == "Yes" else 1)
        + (3 if row["AlcoholDrinking"] == "Yes" else 0)
        + (5 if row["PhysicalActivity"] == "No" else 1)
        + max(0, float(row["BMI"]) - 25) * 0.35,
        1,
    )


def medication_from_row(row):
    meds = []
    if row["HeartDisease"] == "Yes":
        meds.append("Cardiology follow-up")
    if row["Diabetic"] != "No":
        meds.append("Glucose management")
    if row["Stroke"] == "Yes":
        meds.append("Secondary prevention")
    return ", ".join(meds) if meds else "None"


def query_all(sql, params=()):
    return get_db().execute(sql, params).fetchall()


def query_one(sql, params=()):
    return get_db().execute(sql, params).fetchone()


def export_patients_csv(path):
    rows = query_all("SELECT * FROM patients")
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(rows[0].keys() if rows else [])
        writer.writerows([tuple(row) for row in rows])
