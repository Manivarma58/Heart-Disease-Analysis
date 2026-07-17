from flask import Blueprint, render_template, session

from app.routes.auth import role_required
from app.services.database_service import query_one
from app.services.risk_calculator import recommendation_for
from app.services.tableau_service import tableau_status
from app.utils.helpers import age_from_dob

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/dashboard/patient")
@role_required("patient")
def patient_dashboard():
    user = session.get("user", {})
    email = user.get("email")
    patient = None
    
    if email:
        patient = query_one(
            """SELECT p.*, r.*, c.*, l.*, m.*
               FROM patients p
               JOIN risk_assessments r ON r.patient_id = p.patient_id
               JOIN clinical_measurements c ON c.patient_id = p.patient_id
               JOIN lifestyle_factors l ON l.patient_id = p.patient_id
               JOIN medical_history m ON m.patient_id = p.patient_id
               WHERE LOWER(p.first_name || ' ' || p.last_name) = (SELECT LOWER(name) FROM users WHERE LOWER(email) = ?)""",
            (email.strip().lower(),)
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
        
    patient_dict = dict(patient) if patient else {}

    return render_template(
        "dashboard/patient.html",
        patient=patient_dict,
        age=age_from_dob(patient_dict["date_of_birth"]) if patient_dict else None,
        recommendation=recommendation_for(patient_dict["risk_category"]) if patient_dict else "",
        tableau=tableau_status("patient"),
    )
