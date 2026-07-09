from flask import Blueprint, jsonify, redirect, render_template, session, url_for

from app.routes.auth import login_required
from app.services.database_service import query_all, query_one
from app.services.tableau_service import tableau_status

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard.home"))
    return render_template(
        "index.html",
        dashboard_embed=tableau_status("dashboard"),
        story_embed=tableau_status("story"),
    )


@dashboard_bp.route("/web-integration/dashboard")
def public_dashboard_embed():
    return render_template(
        "published_embed.html",
        title="Published Heart Disease Dashboard",
        eyebrow="Dashboard embed",
        tableau=tableau_status("dashboard"),
        fallback_url=url_for("auth.login"),
        fallback_label="Open local dashboard demo",
    )


@dashboard_bp.route("/web-integration/story")
def public_story_embed():
    return render_template(
        "published_embed.html",
        title="Published Heart Disease Story",
        eyebrow="Story embed",
        tableau=tableau_status("story"),
        fallback_url=url_for("auth.login"),
        fallback_label="Open local story demo",
    )


from app.utils.helpers import age_from_dob
from app.services.risk_calculator import recommendation_for

@dashboard_bp.route("/dashboard")
@login_required
def home():
    persona = session["user"]["persona"]
    
    # 1. Active Patients and Population Dataset Counts
    patient_count = query_one("SELECT COUNT(*) AS count FROM patients")["count"]
    population_count = query_one("SELECT COUNT(*) AS count FROM raw_heart_dataset")["count"]
    
    # 2. Risk Distribution percentages
    risk_counts = query_all("SELECT risk_category, COUNT(*) AS count FROM risk_assessments GROUP BY risk_category")
    total_assessments = sum(row["count"] for row in risk_counts) or 1
    risk_dist = {row["risk_category"]: round(100.0 * row["count"] / total_assessments) for row in risk_counts}
    for cat in ["Low", "Moderate", "High"]:
        if cat not in risk_dist:
            risk_dist[cat] = 0
            
    # 3. Dynamic Most Common Risk Factor (Smoking)
    smoking_count = query_one("SELECT COUNT(*) AS count FROM raw_heart_dataset WHERE smoking='Yes'")["count"]
    common_risk_pct = round(100.0 * smoking_count / (population_count or 1))
    common_risk = "Smoking"
    
    # 4. Recent Activity Logs (audit logs + fallback mock logs)
    audit_rows = query_all("SELECT * FROM audit_logs ORDER BY event_time DESC LIMIT 3")
    recent_activity = [dict(row) for row in audit_rows]
    if not recent_activity:
        recent_activity = [
            {"action": "Patient BP update", "resource": "Patient #0883 BP threshold alert: 142/95 mmHg", "event_time": "2 minutes ago"},
            {"action": "Risk Analysis generated", "resource": "Predictive cardiac AI completed for Maria Santos", "event_time": "1 hour ago"},
            {"action": "Lab results integrated", "resource": "Cholesterol panel for 12 patients updated", "event_time": "3 hours ago"}
        ]
        
    # 5. Patient Profile Record Lookup
    patient = None
    age = None
    rec = ""
    if persona == "patient":
        name_parts = session["user"]["name"].split(" ")
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        patient = query_one(
            """SELECT p.*, r.*, c.*, l.*, m.*
               FROM patients p
               JOIN risk_assessments r ON r.patient_id = p.patient_id
               JOIN clinical_measurements c ON c.patient_id = p.patient_id
               JOIN lifestyle_factors l ON l.patient_id = p.patient_id
               JOIN medical_history m ON m.patient_id = p.patient_id
               WHERE p.first_name = ? AND p.last_name = ?""",
            (first_name, last_name)
        )
        if not patient:
            patient = query_one(
                """SELECT p.*, r.*, c.*, l.*, m.*
                   FROM patients p
                   JOIN risk_assessments r ON r.patient_id = p.patient_id
                   JOIN clinical_measurements c ON c.patient_id = p.patient_id
                   JOIN lifestyle_factors l ON l.patient_id = p.patient_id
                   JOIN medical_history m ON m.patient_id = p.patient_id
                   ORDER BY r.framingham_score DESC LIMIT 1"""
            )
        if patient:
            age = age_from_dob(patient["date_of_birth"])
            rec = recommendation_for(patient["risk_category"])

    return render_template(
        "dashboard/home.html",
        patient_count=patient_count,
        population_count=population_count,
        risk_dist=risk_dist,
        common_risk=common_risk,
        common_risk_pct=common_risk_pct,
        recent_activity=recent_activity,
        patient=patient,
        age=age,
        recommendation=rec,
        age_from_dob=age_from_dob,
        recommendation_for=recommendation_for
    )


@dashboard_bp.route("/dashboard/tableau-style")
@login_required
def tableau_style_dashboard():
    totals = query_one(
        """SELECT COUNT(*) AS records,
                  SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) AS heart_cases,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate,
                  ROUND(AVG(bmi), 1) AS avg_bmi
           FROM raw_heart_dataset"""
    )
    gender = query_all(
        """SELECT sex, heart_disease, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY sex, heart_disease
           ORDER BY sex, heart_disease"""
    )
    race = query_all(
        """SELECT race, COUNT(*) AS count,
                  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM raw_heart_dataset), 2) AS pct
           FROM raw_heart_dataset
           GROUP BY race
           ORDER BY count DESC"""
    )
    diabetic_stroke = query_all(
        """SELECT diabetic, stroke, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY diabetic, stroke
           ORDER BY diabetic, stroke"""
    )
    smoking_alcohol = query_all(
        """SELECT smoking, alcohol_drinking, heart_disease, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY smoking, alcohol_drinking, heart_disease
           ORDER BY smoking, alcohol_drinking, heart_disease"""
    )
    age_rate = query_all(
        """SELECT age_category,
                  COUNT(*) AS records,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset
           GROUP BY age_category
           ORDER BY CASE WHEN age_category='80 or older' THEN 80 ELSE CAST(SUBSTR(age_category, 1, 2) AS INTEGER) END"""
    )
    activity = query_all(
        """SELECT physical_activity, COUNT(*) AS records,
                  SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) AS heart_cases,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset
           GROUP BY physical_activity
           ORDER BY physical_activity"""
    )
    gen_health = query_all(
        """SELECT gen_health, COUNT(*) AS records,
                  SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) AS heart_cases,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset
           GROUP BY gen_health
           ORDER BY CASE gen_health
                    WHEN 'Poor' THEN 1 WHEN 'Fair' THEN 2 WHEN 'Good' THEN 3
                    WHEN 'Very good' THEN 4 ELSE 5 END"""
    )
    other_diseases = query_all(
        """SELECT 'Asthma' AS condition_name, asthma AS status, COUNT(*) AS records,
                  SUM(CASE WHEN stroke='Yes' THEN 1 ELSE 0 END) AS stroke_cases
           FROM raw_heart_dataset GROUP BY asthma
           UNION ALL
           SELECT 'Kidney Disease' AS condition_name, kidney_disease AS status, COUNT(*) AS records,
                  SUM(CASE WHEN stroke='Yes' THEN 1 ELSE 0 END) AS stroke_cases
           FROM raw_heart_dataset GROUP BY kidney_disease
           UNION ALL
           SELECT 'Skin Cancer' AS condition_name, skin_cancer AS status, COUNT(*) AS records,
                  SUM(CASE WHEN stroke='Yes' THEN 1 ELSE 0 END) AS stroke_cases
           FROM raw_heart_dataset GROUP BY skin_cancer"""
    )
    age_bmi = query_all(
        """SELECT age_category,
                  ROUND(AVG(bmi), 1) AS avg_bmi,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset
           GROUP BY age_category
           ORDER BY CASE WHEN age_category='80 or older' THEN 80 ELSE CAST(SUBSTR(age_category, 1, 2) AS INTEGER) END"""
    )
    stroke_overlap = query_all(
        """SELECT CASE
                    WHEN heart_disease='Yes' AND diabetic <> 'No' THEN 'Heart Disease + Diabetes'
                    WHEN heart_disease='Yes' AND diabetic = 'No' THEN 'Heart Disease Only'
                    WHEN heart_disease='No' AND diabetic <> 'No' THEN 'Diabetes Only'
                    ELSE 'Neither'
                  END AS cohort,
                  COUNT(*) AS records,
                  SUM(CASE WHEN stroke='Yes' THEN 1 ELSE 0 END) AS stroke_cases,
                  ROUND(100.0 * SUM(CASE WHEN stroke='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS stroke_rate
           FROM raw_heart_dataset
           GROUP BY cohort
           ORDER BY stroke_rate DESC"""
    )
    return render_template(
        "dashboard/tableau_style.html",
        totals=totals,
        gender=gender,
        race=race,
        diabetic_stroke=diabetic_stroke,
        smoking_alcohol=smoking_alcohol,
        age_rate=age_rate,
        activity=activity,
        gen_health=gen_health,
        other_diseases=other_diseases,
        age_bmi=age_bmi,
        stroke_overlap=stroke_overlap,
    )


@dashboard_bp.route("/story/heart-disease")
@login_required
def heart_disease_story():
    totals = query_one(
        """SELECT COUNT(*) AS records,
                  SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) AS heart_cases,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset"""
    )
    gender = query_all(
        """SELECT sex, heart_disease, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY sex, heart_disease
           ORDER BY sex, heart_disease"""
    )
    activity = query_all(
        """SELECT physical_activity, heart_disease, COUNT(*) AS count,
                  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM raw_heart_dataset), 1) AS pct
           FROM raw_heart_dataset
           GROUP BY physical_activity, heart_disease
           ORDER BY physical_activity, heart_disease"""
    )
    diabetic_stroke = query_all(
        """SELECT diabetic, stroke, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY diabetic, stroke
           ORDER BY count DESC"""
    )
    smoking_alcohol = query_all(
        """SELECT smoking, alcohol_drinking, heart_disease, COUNT(*) AS count
           FROM raw_heart_dataset
           GROUP BY smoking, alcohol_drinking, heart_disease
           ORDER BY smoking, alcohol_drinking, heart_disease"""
    )
    age_rate = query_all(
        """SELECT age_category,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset
           GROUP BY age_category
           ORDER BY CASE WHEN age_category='80 or older' THEN 80 ELSE CAST(SUBSTR(age_category, 1, 2) AS INTEGER) END"""
    )
    return render_template(
        "dashboard/heart_story.html",
        totals=totals,
        gender=gender,
        activity=activity,
        diabetic_stroke=diabetic_stroke,
        smoking_alcohol=smoking_alcohol,
        age_rate=age_rate,
    )


@dashboard_bp.route("/dashboard/settings")
@login_required
def settings_page():
    return render_template("dashboard/settings.html")


@dashboard_bp.route("/dashboard/api-docs")
@login_required
def api_docs_page():
    return render_template("dashboard/api_docs.html")


@dashboard_bp.route("/dashboard/navigation-components")
@login_required
def navigation_components_page():
    return render_template("dashboard/navigation_components.html")


@dashboard_bp.route("/dashboard/visualizer")
@login_required
def visualizer_page():
    return render_template("dashboard/visualizer.html")


@dashboard_bp.route("/dashboard/forms")
@login_required
def forms_page():
    return render_template("dashboard/forms.html")


@dashboard_bp.route("/dashboard/notifications-components")
@login_required
def notifications_components_page():
    return render_template("dashboard/notifications_components.html")


@dashboard_bp.route("/patients")
@login_required
def patients_alias():
    return redirect(url_for("clinical.clinical_dashboard"))


@dashboard_bp.route("/reports")
@login_required
def reports_alias():
    return redirect(url_for("dashboard.heart_disease_story"))


@dashboard_bp.route("/settings")
@login_required
def settings_alias():
    return redirect(url_for("dashboard.settings_page"))


@dashboard_bp.route("/api/overview")
@login_required
def overview_api():
    totals = query_one(
        """SELECT COUNT(*) AS patients,
                  ROUND(AVG(framingham_score), 1) AS avg_risk,
                  SUM(CASE WHEN risk_category='High' THEN 1 ELSE 0 END) AS high_risk
           FROM risk_assessments"""
    )
    regions = query_all(
        """SELECT p.region, COUNT(*) AS patients, ROUND(AVG(r.framingham_score), 1) AS avg_risk
           FROM patients p JOIN risk_assessments r ON p.patient_id = r.patient_id
           GROUP BY p.region ORDER BY p.region"""
    )
    return jsonify({"totals": dict(totals), "regions": [dict(row) for row in regions]})
