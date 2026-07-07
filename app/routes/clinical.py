from flask import Blueprint, jsonify, render_template, request

from app.routes.auth import role_required
from app.services.database_service import query_all, query_one
from app.services.risk_calculator import recommendation_for
from app.services.tableau_service import tableau_status
from app.utils.helpers import age_from_dob

clinical_bp = Blueprint("clinical", __name__)


@clinical_bp.route("/dashboard/clinical")
@role_required("clinical")
def clinical_dashboard():
    patients = query_all(
        """SELECT p.*, r.framingham_score, r.risk_category, c.systolic_bp, c.cholesterol_total, c.bmi,
                  l.smoking_status, l.physical_activity
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           JOIN clinical_measurements c ON c.patient_id = p.patient_id
           JOIN lifestyle_factors l ON l.patient_id = p.patient_id
           ORDER BY r.framingham_score DESC LIMIT 24"""
    )
    risk_mix = query_all("SELECT risk_category, COUNT(*) AS count FROM risk_assessments GROUP BY risk_category")
    return render_template(
        "dashboard/clinical.html",
        patients=patients,
        risk_mix=risk_mix,
        age_from_dob=age_from_dob,
        recommendation_for=recommendation_for,
        tableau=tableau_status("clinical"),
    )


@clinical_bp.route("/api/patients")
@role_required("clinical")
def patients_api():
    term = f"%{request.args.get('q', '').strip()}%"
    rows = query_all(
        """SELECT p.patient_id, p.first_name, p.last_name, p.gender, p.region,
                  r.framingham_score, r.risk_category
           FROM patients p JOIN risk_assessments r ON r.patient_id = p.patient_id
           WHERE p.first_name LIKE ? OR p.last_name LIKE ? OR p.region LIKE ?
           ORDER BY r.framingham_score DESC LIMIT 20""",
        (term, term, term),
    )
    return jsonify([dict(row) for row in rows])


@clinical_bp.route("/api/patients/<int:patient_id>")
@role_required("clinical")
def patient_detail_api(patient_id):
    row = query_one(
        """SELECT p.*, r.*, c.*, l.*, m.*
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           JOIN clinical_measurements c ON c.patient_id = p.patient_id
           JOIN lifestyle_factors l ON l.patient_id = p.patient_id
           JOIN medical_history m ON m.patient_id = p.patient_id
           WHERE p.patient_id = ?""",
        (patient_id,),
    )
    return jsonify(dict(row) if row else {})
