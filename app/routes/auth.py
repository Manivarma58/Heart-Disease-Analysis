from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.services.database_service import query_one

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def role_required(*personas):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = session.get("user")
            if not user:
                return redirect(url_for("auth.login", next=request.path))
            if user["persona"] not in personas and user["persona"] != "admin":
                flash("Your account does not have access to that workspace.", "warning")
                return redirect(url_for("dashboard.home"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = {
                "id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "persona": user["persona"],
            }
            return redirect(request.args.get("next") or url_for("dashboard.home"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
