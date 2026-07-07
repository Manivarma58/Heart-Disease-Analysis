from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.routes.auth import role_required
from app.services.database_service import get_db, query_all, query_one

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@role_required("admin")
def admin_home():
    users = query_all("SELECT user_id, name, email, role, persona FROM users ORDER BY role")
    stats = query_one("SELECT COUNT(*) AS patients FROM patients")
    return render_template("admin/user_management.html", users=users, stats=stats)


@admin_bp.route("/admin/data-upload", methods=["GET", "POST"])
@role_required("admin")
def data_upload():
    if request.method == "POST":
        flash("CSV validation pipeline placeholder accepted the file for demo review.", "success")
        return redirect(url_for("admin.data_upload"))
    return render_template("admin/data_upload.html")


@admin_bp.route("/admin/audit")
@role_required("admin")
def audit():
    logs = query_all("SELECT * FROM audit_logs ORDER BY event_time DESC LIMIT 100")
    return {"logs": [dict(row) for row in logs]}
