from flask import Blueprint, jsonify, redirect, render_template, session, url_for

from app.routes.auth import login_required
from app.services.database_service import query_all, query_one

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard.home"))
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def home():
    persona = session["user"]["persona"]
    if persona == "clinical":
        return redirect(url_for("clinical.clinical_dashboard"))
    if persona == "public_health":
        return redirect(url_for("public_health.public_health_dashboard"))
    if persona == "patient":
        return redirect(url_for("patient.patient_dashboard"))
    return redirect(url_for("admin.admin_home"))


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
