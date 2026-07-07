from flask import Blueprint, render_template

from app.routes.auth import role_required
from app.services.database_service import query_one
from app.services.risk_calculator import recommendation_for
from app.services.tableau_service import tableau_status
from app.utils.helpers import age_from_dob

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/dashboard/patient")
@role_required("patient")
def patient_dashboard():
    patient = query_one(
        """SELECT p.*, r.*, c.*, l.*, m.*
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           JOIN clinical_measurements c ON c.patient_id = p.patient_id
           JOIN lifestyle_factors l ON l.patient_id = p.patient_id
           JOIN medical_history m ON m.patient_id = p.patient_id
           ORDER BY r.framingham_score DESC LIMIT 1"""
    )
    return render_template(
        "dashboard/patient.html",
        patient=patient,
        age=age_from_dob(patient["date_of_birth"]) if patient else None,
        recommendation=recommendation_for(patient["risk_category"]) if patient else "",
        tableau=tableau_status("patient"),
    )
