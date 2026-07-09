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
    from flask import redirect, url_for
    return redirect(url_for("dashboard.home") + "#health-hub")
