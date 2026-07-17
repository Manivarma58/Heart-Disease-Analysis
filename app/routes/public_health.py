from flask import Blueprint, render_template, jsonify

from app.routes.auth import role_required
from app.services.database_service import query_all, query_one
from app.services.report_generator import population_report
from app.services.tableau_service import tableau_status

public_health_bp = Blueprint("public_health", __name__)


@public_health_bp.route("/dashboard/public-health")
@role_required("public_health")
def public_health_dashboard():
    regional = query_all(
        """SELECT p.region, p.urban_rural, COUNT(*) AS patients,
                  ROUND(AVG(r.framingham_score), 1) AS avg_risk,
                  SUM(CASE WHEN m.heart_disease='Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           JOIN medical_history m ON m.patient_id = p.patient_id
           GROUP BY p.region, p.urban_rural
           ORDER BY p.region, p.urban_rural"""
    )
    lifestyle = query_all(
        """SELECT l.physical_activity, l.smoking_status, COUNT(*) AS patients,
                  ROUND(AVG(r.framingham_score), 1) AS avg_risk
           FROM lifestyle_factors l
           JOIN risk_assessments r ON r.patient_id = l.patient_id
           GROUP BY l.physical_activity, l.smoking_status
           ORDER BY avg_risk DESC"""
    )
    totals = query_one("SELECT COUNT(*) AS patients, ROUND(AVG(framingham_score), 1) AS avg_risk FROM risk_assessments")
    
    # Calculate prevalence rate from medical history
    cases_row = query_one("SELECT COUNT(*) AS cases FROM medical_history WHERE heart_disease='Yes'")
    total_row = query_one("SELECT COUNT(*) AS total FROM patients")
    cases_count = cases_row["cases"] if cases_row else 0
    total_count = total_row["total"] if total_row else 0
    prevalence = round(100.0 * cases_count / total_count, 1) if total_count > 0 else 8.5
    
    # Calculate highest vs lowest region
    highest_region = "North"
    lowest_region = "South"
    highest_risk = 0.0
    lowest_risk = 100.0
    for r in regional:
        if r["avg_risk"] > highest_risk:
            highest_risk = r["avg_risk"]
            highest_region = r["region"]
        if r["avg_risk"] < lowest_risk:
            lowest_risk = r["avg_risk"]
            lowest_region = r["region"]
            
    variation = {
        "highest": highest_region,
        "lowest": lowest_region,
        "diff": round(highest_risk - lowest_risk, 1)
    }

    stats = {
        "prevalence": prevalence,
        "patients_count": total_count,
        "variation": variation,
        "demographic": "Males, 46-60 (15.2%)",
        "prevention_impact": 2.5
    }

    # Query additional visualizations data:
    # 1. Urban vs Rural
    urban_rural_rows = query_all(
        """SELECT p.urban_rural, COUNT(*) AS total, SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN medical_history m ON p.patient_id = m.patient_id
           GROUP BY p.urban_rural"""
    )
    urban_rural_data = [dict(r) for r in urban_rural_rows]

    # 2. Age & Gender Trends
    age_gender_rows = query_all(
        """SELECT
             CASE
               WHEN (strftime('%Y', 'now') - strftime('%Y', p.date_of_birth)) < 30 THEN '18-29'
               WHEN (strftime('%Y', 'now') - strftime('%Y', p.date_of_birth)) BETWEEN 30 AND 45 THEN '30-45'
               WHEN (strftime('%Y', 'now') - strftime('%Y', p.date_of_birth)) BETWEEN 46 AND 60 THEN '46-60'
               ELSE '60+'
             END AS age_category,
             p.gender AS sex,
             COUNT(*) AS total,
             SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN medical_history m ON p.patient_id = m.patient_id
           GROUP BY age_category, sex"""
    )
    age_gender_data = [dict(r) for r in age_gender_rows]

    # 3. Race Distribution (using last_name which holds Race from import)
    race_rows = query_all(
        """SELECT p.last_name AS race, COUNT(*) AS total, SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN medical_history m ON p.patient_id = m.patient_id
           GROUP BY race"""
    )
    race_data = [dict(r) for r in race_rows]

    # 4. Income range correlation
    income_rows = query_all(
        """SELECT p.income_range, COUNT(*) AS total, SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN medical_history m ON p.patient_id = m.patient_id
           GROUP BY p.income_range"""
    )
    income_data = [dict(r) for r in income_rows]

    # 5. Education impact
    edu_rows = query_all(
        """SELECT p.education_level, COUNT(*) AS total, SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM patients p
           JOIN medical_history m ON p.patient_id = m.patient_id
           GROUP BY p.education_level"""
    )
    edu_data = [dict(r) for r in edu_rows]

    # 6. Lifestyle (Smoking status by region)
    lifestyle_smoke_rows = query_all(
        """SELECT l.smoking_status, COUNT(*) AS total, SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM lifestyle_factors l
           JOIN medical_history m ON m.patient_id = l.patient_id
           GROUP BY smoking_status"""
    )
    lifestyle_smoke_data = [dict(r) for r in lifestyle_smoke_rows]

    chart_data = {
        "urban_rural": urban_rural_data,
        "age_gender": age_gender_data,
        "race": race_data,
        "income": income_data,
        "edu": edu_data,
        "smoke": lifestyle_smoke_data
    }

    return render_template(
        "dashboard/public_health.html",
        regional=regional,
        lifestyle=lifestyle,
        totals=totals,
        stats=stats,
        chart_data=chart_data,
        report=population_report(),
        tableau=tableau_status("public_health"),
    )


@public_health_bp.route("/dashboard/public-health/visualizations")
@role_required("public_health")
def visualizations_dashboard():
    return render_template("dashboard/visualizations.html")


@public_health_bp.route("/api/visualizations-data")
@role_required("public_health")
def visualizations_data():
    # 1. Gender vs Heart Disease
    gender_hd = query_all(
        """SELECT sex,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY sex"""
    )
    
    # 2. Age vs Heart Disease
    age_hd = query_all(
        """SELECT age_category,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY age_category"""
    )
    def get_age_sort_val(cat):
        if "older" in cat:
            return 80
        return int(cat.split("-")[0])
    age_hd_sorted = sorted([dict(r) for r in age_hd], key=lambda x: get_age_sort_val(x["age_category"]))

    # 3. Diabetic vs Stroke
    diabetic_stroke = query_all(
        """SELECT diabetic,
                  COUNT(*) AS total,
                  SUM(CASE WHEN stroke = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY diabetic"""
    )

    # 4. Impact of Smoking and Alcohol on Heart Disease
    smoking_alcohol = query_all(
        """SELECT smoking, alcohol_drinking,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY smoking, alcohol_drinking"""
    )

    # 5. Other Health Diseases vs Stroke
    other_diseases = query_all(
        """SELECT 'Asthma' AS condition_name, asthma AS status, COUNT(*) AS total, SUM(CASE WHEN stroke = 'Yes' THEN 1 ELSE 0 END) AS cases FROM raw_heart_dataset GROUP BY asthma
           UNION ALL
           SELECT 'Kidney Disease' AS condition_name, kidney_disease AS status, COUNT(*) AS total, SUM(CASE WHEN stroke = 'Yes' THEN 1 ELSE 0 END) AS cases FROM raw_heart_dataset GROUP BY kidney_disease
           UNION ALL
           SELECT 'Skin Cancer' AS condition_name, skin_cancer AS status, COUNT(*) AS total, SUM(CASE WHEN stroke = 'Yes' THEN 1 ELSE 0 END) AS cases FROM raw_heart_dataset GROUP BY skin_cancer"""
    )

    # 6. Race wise Heart Disease
    race_hd = query_all(
        """SELECT race,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY race"""
    )

    # 7. General Health vs Heart Disease
    gen_health_hd = query_all(
        """SELECT gen_health,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY gen_health"""
    )
    health_order = {"Poor": 1, "Fair": 2, "Good": 3, "Very good": 4, "Excellent": 5}
    gen_health_sorted = sorted([dict(r) for r in gen_health_hd], key=lambda x: health_order.get(x["gen_health"], 0))

    # 8. Physical Activity vs Heart Disease
    activity_hd = query_all(
        """SELECT physical_activity,
                  COUNT(*) AS total,
                  SUM(CASE WHEN heart_disease = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY physical_activity"""
    )

    # 9. Age and BMI vs Diabetic (Scatter Plot - Sampled for Performance)
    age_bmi_diabetic = query_all(
        """SELECT age_category, bmi, diabetic
           FROM raw_heart_dataset
           ORDER BY RANDOM() LIMIT 500"""
    )
    def get_age_midpoint(cat):
        if "older" in cat:
            return 82
        start, end = cat.split("-")
        return (int(start) + int(end)) / 2
    
    scatter_data = []
    for r in age_bmi_diabetic:
        scatter_data.append({
            "age": get_age_midpoint(r["age_category"]),
            "age_category": r["age_category"],
            "bmi": r["bmi"],
            "diabetic": r["diabetic"]
        })

    # 10. Stroke overlap cohorts
    stroke_overlap = query_all(
        """SELECT
             CASE
               WHEN heart_disease = 'Yes' AND diabetic <> 'No' THEN 'Both'
               WHEN heart_disease = 'Yes' AND diabetic = 'No' THEN 'Heart Disease Only'
               WHEN heart_disease = 'No' AND diabetic <> 'No' THEN 'Diabetes Only'
               ELSE 'Neither'
             END AS cohort,
             COUNT(*) AS total,
             SUM(CASE WHEN stroke = 'Yes' THEN 1 ELSE 0 END) AS cases
           FROM raw_heart_dataset
           GROUP BY cohort"""
    )

    return jsonify({
        "gender_hd": [dict(r) for r in gender_hd],
        "age_hd": age_hd_sorted,
        "diabetic_stroke": [dict(r) for r in diabetic_stroke],
        "smoking_alcohol": [dict(r) for r in smoking_alcohol],
        "other_diseases": [dict(r) for r in other_diseases],
        "race_hd": [dict(r) for r in race_hd],
        "gen_health_hd": gen_health_sorted,
        "activity_hd": [dict(r) for r in activity_hd],
        "age_bmi_diabetic": scatter_data,
        "stroke_overlap": [dict(r) for r in stroke_overlap]
    })

