from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session

from app.routes.auth import role_required
from app.services.database_service import get_db, query_all, query_one
from app.services.risk_calculator import recommendation_for
from app.services.tableau_service import tableau_status
from app.utils.helpers import age_from_dob

clinical_bp = Blueprint("clinical", __name__)


@clinical_bp.route("/dashboard/clinical")
@role_required("clinical")
def clinical_dashboard():
    # 1. Query general patients registry (limited to 24)
    patients = query_all(
        """SELECT p.*, r.framingham_score, r.risk_category, r.assessment_date, c.systolic_bp, c.cholesterol_total, c.bmi,
                  l.smoking_status, l.physical_activity, m.heart_disease, m.heart_disease_type, m.hypertension, m.diabetes
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           JOIN clinical_measurements c ON c.patient_id = p.patient_id
           JOIN lifestyle_factors l ON l.patient_id = p.patient_id
           JOIN medical_history m ON m.patient_id = p.patient_id
           ORDER BY r.framingham_score DESC LIMIT 24"""
    )
    
    # 2. Query priority patient alerts (top 5 high risk patients)
    priority_patients = query_all(
        """SELECT p.*, r.framingham_score, r.risk_category, r.assessment_date
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           WHERE r.risk_category = 'High'
           ORDER BY r.framingham_score DESC LIMIT 5"""
    )
    
    # 3. Query stats counters
    total_patients_row = query_one("SELECT COUNT(*) AS total FROM patients")
    total_patients = total_patients_row["total"] if total_patients_row else 1234
    
    high_risk_row = query_one("SELECT COUNT(*) AS total FROM risk_assessments WHERE risk_category = 'High'")
    high_risk_count = high_risk_row["total"] if high_risk_row else 89
    high_risk_pct = round(100.0 * high_risk_count / total_patients, 1) if total_patients > 0 else 7.2

    stats = {
        "total_patients": total_patients,
        "high_risk_count": high_risk_count,
        "high_risk_pct": high_risk_pct,
        "new_diagnoses": 45,
        "success_rate": 94.5
    }

    # 4. Query clinical notes
    notes = query_all("SELECT * FROM clinical_notes ORDER BY created_at DESC LIMIT 10")
    
    doctor_name = session.get("user", {}).get("name", "Dr. Sharma")

    return render_template(
        "dashboard/clinical.html",
        patients=patients,
        priority_patients=priority_patients,
        stats=stats,
        notes=notes,
        doctor_name=doctor_name,
        age_from_dob=age_from_dob,
        recommendation_for=recommendation_for
    )


@clinical_bp.route("/dashboard/clinical/note/add", methods=["POST"])
@role_required("clinical")
def add_clinical_note():
    doctor_name = session.get("user", {}).get("name", "Dr. Sharma")
    content = request.form.get("note_content", "").strip()
    if content:
        db = get_db()
        db.execute(
            "INSERT INTO clinical_notes (doctor_name, content, created_at) VALUES (?, ?, datetime('now', 'localtime'))",
            (doctor_name, content)
        )
        db.commit()
    return redirect(url_for("clinical.clinical_dashboard"))


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
