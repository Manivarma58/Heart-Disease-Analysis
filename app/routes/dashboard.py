from flask import Blueprint, jsonify, redirect, render_template, session, url_for

from app.routes.auth import login_required
from app.services.database_service import get_db, query_all, query_one
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


@dashboard_bp.route("/dashboard")
@login_required
def home():
    user = session["user"]
    persona = user.get("persona")
    name = user.get("name", "User")
    role = user.get("role", "User")
    email = user.get("email", "")

    # 1. Initialize stats context
    stats = {}
    patient_details = {}

    # 2. Query Doctor Specific Stats
    if persona == "clinical" or persona == "admin":
        total_patients_row = query_one("SELECT COUNT(*) AS total FROM patients")
        stats["total_patients"] = total_patients_row["total"] if total_patients_row else 0
        
        high_risk_row = query_one("SELECT COUNT(*) AS total FROM risk_assessments WHERE risk_category = 'High'")
        stats["high_risk_patients"] = high_risk_row["total"] if high_risk_row else 0
        
        # Pending reviews and new cases fallbacks
        stats["pending_reviews"] = 12
        stats["new_cases_24h"] = 45

    # 3. Query Patient Specific Stats
    elif persona == "patient":
        names = name.split()
        first_name = names[0] if len(names) > 0 else ""
        last_name = names[1] if len(names) > 1 else ""
        
        patient_row = query_one(
            """SELECT p.*, r.*, c.*, l.*, m.*
               FROM patients p
               LEFT JOIN risk_assessments r ON r.patient_id = p.patient_id
               LEFT JOIN clinical_measurements c ON c.patient_id = p.patient_id
               LEFT JOIN lifestyle_factors l ON l.patient_id = p.patient_id
               LEFT JOIN medical_history m ON m.patient_id = p.patient_id
               WHERE p.first_name = ? AND p.last_name = ?
               ORDER BY r.assessment_date DESC LIMIT 1""",
            (first_name, last_name)
        )
        
        if not patient_row:
            patient_row = query_one(
                """SELECT p.*, r.*, c.*, l.*, m.*
                   FROM patients p
                   LEFT JOIN risk_assessments r ON r.patient_id = p.patient_id
                   LEFT JOIN clinical_measurements c ON c.patient_id = p.patient_id
                   LEFT JOIN lifestyle_factors l ON l.patient_id = p.patient_id
                   LEFT JOIN medical_history m ON m.patient_id = p.patient_id
                   ORDER BY r.framingham_score DESC LIMIT 1"""
            )
            
        if patient_row:
            patient_details = dict(patient_row)
            framingham = patient_details.get("framingham_score") or 18.0
            stats["health_score"] = int(100 - framingham)
            stats["risk_level"] = patient_details.get("risk_category") or "Moderate"
        else:
            stats["health_score"] = 82
            stats["risk_level"] = "Moderate"
            
        stats["last_checkup"] = "2 weeks ago"
        stats["next_appointment"] = "July 15"

    # 4. Query recent activity logs from audit_logs
    audit_rows = query_all("SELECT action, resource, event_time FROM audit_logs ORDER BY event_time DESC LIMIT 5")
    recent_activity = []
    if audit_rows:
        for row in audit_rows:
            action = row["action"]
            resource = row["resource"]
            time_str = row["event_time"]
            recent_activity.append({
                "title": f"{action} {resource}",
                "time": time_str
            })
    else:
        recent_activity = [
            {"title": "Patient #1024 Reviewed", "time": "10 mins ago • Clinical"},
            {"title": "High-Risk Alert Triggered", "time": "45 mins ago • Vital Pulse"},
            {"title": "Public Health Data Export", "time": "2 hours ago • Policy"},
            {"title": "New Report Generated", "time": "4 hours ago • Reports"},
            {"title": "Schedule Update", "time": "6 hours ago • Follow-up"}
        ]

    # Save an audit log of viewing the dashboard
    db = get_db()
    db.execute(
        "INSERT INTO audit_logs (event_time, user_email, action, resource) VALUES (datetime('now', 'localtime'), ?, ?, ?)",
        (email, "Viewed", "Dashboard Hub")
    )
    db.commit()

    return render_template(
        "dashboard/hub.html",
        name=name,
        role=role,
        persona=persona,
        stats=stats,
        patient=patient_details,
        recent_activity=recent_activity
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
    # Get doctor name for personalized report builder branding
    doctor_name = session.get("user", {}).get("name", "Dr. John Smith")
    
    return render_template(
        "dashboard/heart_story.html",
        totals=totals,
        gender=gender,
        activity=activity,
        diabetic_stroke=diabetic_stroke,
        smoking_alcohol=smoking_alcohol,
        age_rate=age_rate,
        doctor_name=doctor_name,
    )


@dashboard_bp.route("/dashboard/settings")
@login_required
def settings_page():
    user = session.get("user", {})
    doctor_name = user.get("name", "Dr. Julian Vance")
    email = user.get("email", "julian.vance@stjude.org")
    persona = user.get("persona", "clinical")
    
    totals = query_one(
        """SELECT COUNT(*) AS records,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate
           FROM raw_heart_dataset"""
    )
    
    return render_template(
        "dashboard/settings.html",
        doctor_name=doctor_name,
        email=email,
        persona=persona,
        totals=totals,
    )


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


@dashboard_bp.route("/dashboard/api-docs")
@login_required
def api_docs_page():
    return render_template("dashboard/api_docs.html")


@dashboard_bp.route("/dashboard/design-system/navigation")
@login_required
def navigation_components_page():
    return render_template("dashboard/navigation_components.html")


@dashboard_bp.route("/dashboard/design-system/notifications")
@login_required
def notifications_components_page():
    return render_template("dashboard/notifications_components.html")


@dashboard_bp.route("/dashboard/design-system/forms")
@login_required
def forms_page():
    return render_template("dashboard/forms.html")


@dashboard_bp.route("/dashboard/powerbi-style")
@login_required
def powerbi_style_dashboard():
    return render_template("dashboard/powerbi_style.html")


@dashboard_bp.route("/dashboard/sql-console")
@login_required
def sql_console():
    return render_template("dashboard/sql_console.html")


@dashboard_bp.route("/dashboard/design-system/visualizations")
@login_required
def visualizations_library_page():
    return render_template("dashboard/visualizations_library.html")


@dashboard_bp.route("/dashboard/design-system/integration")
@login_required
def integration_page():
    return render_template("dashboard/integration.html")


@dashboard_bp.route("/dashboard/clinical-analytics")
@login_required
def clinical_analytics_page():
    patients = query_all("SELECT patient_id, first_name, last_name, gender, date_of_birth, region FROM patients ORDER BY last_name ASC")
    totals = query_one(
        """SELECT COUNT(*) AS records,
                  SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) AS heart_cases,
                  ROUND(100.0 * SUM(CASE WHEN heart_disease='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disease_rate,
                  ROUND(AVG(bmi), 1) AS avg_bmi
           FROM raw_heart_dataset"""
    )
    return render_template(
        "dashboard/clinical_analytics.html",
        patients=patients,
        totals=totals,
        doctor_name=session.get("user", {}).get("name", "Dr. Sharma")
    )


@dashboard_bp.route("/knowledge-center")
def knowledge_center_page():
    return render_template("dashboard/knowledge_center.html")


@dashboard_bp.route("/about-us")
def about_us_page():
    return render_template("dashboard/about_us.html")


@dashboard_bp.route("/support")
def support_hub_page():
    return render_template("dashboard/support_hub.html")


@dashboard_bp.route("/privacy")
def privacy_policy_page():
    return render_template("dashboard/privacy_policy.html")


@dashboard_bp.route("/compliance/hipaa")
def hipaa_compliance_page():
    return render_template("dashboard/hipaa_compliance.html")


@dashboard_bp.route("/terms")
def terms_of_service_page():
    return render_template("dashboard/terms_of_service.html")


@dashboard_bp.route("/compliance/accessibility")
def accessibility_governance_page():
    return render_template("dashboard/accessibility_governance.html")


@dashboard_bp.route("/dashboard/reports")
@login_required
def reports_dashboard_page():
    return render_template("dashboard/reports_dashboard.html")


@dashboard_bp.route("/dashboard/reports/builder")
@login_required
def reports_builder_page():
    return render_template("dashboard/reports_builder.html")


