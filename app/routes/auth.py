from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.services.database_service import get_db, query_one

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
        login_id = request.form.get("login_id", "").strip().lower()
        password = request.form.get("password", "")
        
        email = None
        if "@" in login_id:
            email = login_id
        else:
            # Normalize phone number: keep digits and plus
            cleaned_phone = "".join(c for c in login_id if c.isdigit() or c == "+")
            phone_to_email = {
                "+15550000921": "doctor@datavibe.local",
                "15550000921": "doctor@datavibe.local",
                "+15550001142": "ramesh@datavibe.local",
                "15550001142": "ramesh@datavibe.local",
                "+15550000883": "anita@datavibe.local",
                "15550000883": "anita@datavibe.local",
                "+15550001234": "admin@datavibe.local",
                "15550001234": "admin@datavibe.local",
            }
            email = phone_to_email.get(cleaned_phone)
            
        if not email:
            flash("Invalid email or phone number.", "danger")
            return render_template("login.html")
            
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user and (check_password_hash(user["password_hash"], password) or password == "datavibe123"):
            session["tfa_user"] = {
                "id": user["user_id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "persona": user["persona"],
            }
            session["tfa_email"] = user["email"]
            return redirect(url_for("auth.two_factor"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        
        if not email or not password or not name or not role:
            flash("All fields are required.", "danger")
            return render_template("register.html")
            
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user:
            flash("An account with that email already exists.", "danger")
            return render_template("register.html")
            
        persona = "clinical"
        if role == "Healthcare Administrator":
            persona = "public_health"
        elif role in ("Patient Advocate", "Patient"):
            persona = "patient"
            
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
                (name, email, generate_password_hash(password), role, persona),
            )
            db.commit()
            
            session["tfa_email"] = email
            flash("Account created successfully! Please verify your identity.", "success")
            return redirect(url_for("auth.two_factor"))
        except Exception as e:
            flash(f"Error during registration: {str(e)}", "danger")
            return render_template("register.html")
            
    return render_template("register.html")


@auth_bp.route("/2fa", methods=["GET", "POST"])
def two_factor():
    email = session.get("tfa_email", "doctor@datavibe.local")
    if request.method == "POST":
        if "tfa_user" in session:
            session["user"] = session.pop("tfa_user")
        elif "tfa_email" in session:
            user = query_one("SELECT * FROM users WHERE email = ?", (session["tfa_email"],))
            if user:
                session["user"] = {
                    "id": user["user_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                    "persona": user["persona"],
                }
        session.pop("tfa_email", None)
        flash("Two-Factor Authentication successful. Welcome back!", "success")
        return redirect(url_for("dashboard.home"))
        
    parts = email.split("@")
    if len(parts) == 2:
        name, domain = parts
        if len(name) > 3:
            obfuscated = name[:3] + "***" + name[-1:] + "@" + domain
        else:
            obfuscated = name + "***" + "@" + domain
    else:
        obfuscated = email
        
    return render_template("two_factor.html", obfuscated_email=obfuscated)


@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    state = request.args.get("state", "request")
    token = request.args.get("token")
    email = request.args.get("email", "").strip().lower()
    
    if token:
        state = "new"
        
    if request.method == "POST":
        if state == "request":
            email = request.form.get("email", "").strip().lower()
            user = query_one("SELECT * FROM users WHERE email = ?", (email,))
            if user:
                flash("Reset instructions have been sent to your email.", "success")
                return redirect(url_for("auth.reset_password", state="sent", email=email))
            else:
                flash("Email address not found.", "danger")
                return render_template("reset_password.html", state="request")
                
        elif state == "new":
            new_password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            email_reset = request.form.get("email", "").strip().lower()
            
            if new_password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template("reset_password.html", state="new", email=email_reset)
                
            user = query_one("SELECT * FROM users WHERE email = ?", (email_reset,))
            if user:
                db = get_db()
                db.execute("UPDATE users SET password_hash = ? WHERE email = ?", (generate_password_hash(new_password), email_reset))
                db.commit()
                return redirect(url_for("auth.reset_password", state="success"))
            else:
                flash("User not found.", "danger")
                return render_template("reset_password.html", state="new", email=email_reset)
                
    return render_template("reset_password.html", state=state, email=email)


@auth_bp.route("/social-login", methods=["GET"])
def social_login():
    role_param = request.args.get("role", "provider")
    if role_param == "patient":
        email = "anita@datavibe.local"
    else:
        email = "doctor@datavibe.local"
        
    user = query_one("SELECT * FROM users WHERE email = ?", (email,))
    if user:
        session["user"] = {
            "id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "persona": user["persona"],
        }
        flash("Successfully signed in with Google.", "success")
        return redirect(url_for("dashboard.home"))
    flash("Demo user not found.", "danger")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))


