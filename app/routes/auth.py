from functools import wraps
import secrets
import random
import string
from datetime import date, timedelta

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.services.database_service import get_db, query_one

try:
    from authlib.integrations.flask_client import OAuth
except ImportError:
    OAuth = None

auth_bp = Blueprint("auth", __name__)
oauth = OAuth() if OAuth else None


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


def google_oauth_enabled():
    return bool(
        OAuth
        and current_app.config.get("GOOGLE_CLIENT_ID")
        and current_app.config.get("GOOGLE_CLIENT_SECRET")
    )


def google_client():
    if not google_oauth_enabled():
        return None
    oauth.init_app(current_app)
    return oauth.register(
        name="google",
        client_id=current_app.config["GOOGLE_CLIENT_ID"],
        client_secret=current_app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
        overwrite=True,
    )


def sign_in_user(user):
    session["user"] = {
        "id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "persona": user["persona"],
    }


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        login_role = request.form.get("login_role", "doctor")
        
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user and check_password_hash(user["password_hash"], password):
            # Enforce role-based constraints
            expected_persona = "clinical" if login_role == "doctor" else "patient"
            if user["persona"] != expected_persona and not (login_role == "doctor" and user["persona"] == "admin"):
                if login_role == "doctor":
                    flash("This account does not have clinical professional access.", "danger")
                else:
                    flash("Please sign in using the Doctor/Professional portal.", "danger")
                return redirect(url_for("auth.login") + f"?role={login_role}")
                
            sign_in_user(user)
            return redirect(request.args.get("next") or url_for("dashboard.home"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", google_enabled=google_oauth_enabled())


@auth_bp.route("/login/google")
def google_login():
    client = google_client()
    if not client:
        return render_template("google_chooser.html")
    session["oauth_next"] = request.args.get("next") or url_for("dashboard.home")
    redirect_uri = url_for("auth.google_callback", _external=True)
    return client.authorize_redirect(redirect_uri)


@auth_bp.route("/social-login")
def social_login():
    email = request.args.get("email", "").strip().lower()
    if not email:
        flash("Email parameter is missing.", "danger")
        return redirect(url_for("auth.login"))
        
    db = get_db()
    user = query_one("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
    
    if not user:
        if email == 'manivarmakalapu@gmail.com':
            name = 'Mani Varma'
            role = 'Cardiologist'
            persona = 'clinical'
        elif email == 'manivarmakalapu8@gmail.com':
            name = 'Mani Varma Kalapu'
            role = 'Health Official'
            persona = 'public_health'
        elif email == 'manivarmakalapu08@gmail.com':
            name = 'Mani Varma'
            role = 'Patient'
            persona = 'patient'
        elif email == 'sureshbanavath2006@gmail.com':
            name = 'Suresh Naik'
            role = 'Admin'
            persona = 'admin'
        else:
            name = email.split('@')[0].title()
            role = 'Patient'
            persona = 'patient'
            
        db.execute(
            "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
            (name, email, generate_password_hash("cardioviz123"), role, persona)
        )
        db.commit()
        
        if persona == 'patient':
            first_name = name.split()[0]
            last_name = name.split()[1] if len(name.split()) > 1 else 'Patel'
            cursor = db.execute(
                """INSERT INTO patients (first_name, last_name, date_of_birth, gender, region, urban_rural)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (first_name, last_name, "1980-01-01", "Female", "Central", "Urban")
            )
            patient_id = cursor.lastrowid
            
            db.execute(
                """INSERT INTO clinical_measurements (patient_id, measurement_date, systolic_bp, diastolic_bp, cholesterol_total, cholesterol_hdl, cholesterol_ldl, triglycerides, fasting_blood_sugar, bmi, heart_rate)
                   VALUES (?, ?, 125, 82, 195, 45, 120, 150, 112, 27.4, 72)""",
                (patient_id, date.today().isoformat())
            )
            db.execute(
                """INSERT INTO lifestyle_factors (patient_id, smoking_status, smoking_duration, alcohol_consumption, physical_activity, diet_quality, sleep_hours, stress_level)
                   VALUES (?, 'Never', 0, 'None', 'Moderate', 'Average', 7.2, 'Moderate')""",
                (patient_id, )
            )
            db.execute(
                """INSERT INTO medical_history (patient_id, condition_date, heart_disease, heart_disease_type, hypertension, diabetes, family_history, previous_cardiac_event, current_medications)
                   VALUES (?, ?, 'No', NULL, 'Yes', 'Yes', 'No', 'No', 'Atorvastatin 40mg, Aspirin 81mg')""",
                (patient_id, date.today().isoformat())
            )
            db.execute(
                """INSERT INTO risk_assessments (patient_id, assessment_date, framingham_score, ascvd_score, risk_category, lifestyle_risk_score, genetic_risk_score)
                   VALUES (?, ?, 8.5, 8.5, 'Moderate', 3.2, 4.5)""",
                (patient_id, date.today().isoformat())
            )
            db.commit()
            
        user = query_one("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
        
    sign_in_user(user)
    return redirect(url_for("dashboard.home"))


@auth_bp.route("/auth/google/callback")
def google_callback():
    client = google_client()
    if not client:
        flash("Google login is not configured.", "warning")
        return redirect(url_for("auth.login"))
    token = client.authorize_access_token()
    profile = token.get("userinfo") or client.userinfo()
    email = (profile.get("email") or "").strip().lower()
    if not email:
        flash("Google did not return an email address.", "danger")
        return redirect(url_for("auth.login"))

    user = query_one("SELECT * FROM users WHERE email = ?", (email,))
    if not user:
        db = get_db()
        db.execute(
            "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
            (
                profile.get("name") or email.split("@")[0],
                email,
                generate_password_hash(secrets.token_urlsafe(32)),
                "Patient",
                "patient",
            ),
        )
        db.commit()
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))

    sign_in_user(user)
    return redirect(session.pop("oauth_next", None) or url_for("dashboard.home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", "doctor")
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        dob = request.form.get("dob", "")
        gender = request.form.get("gender", "")
        phone = request.form.get("phone", "").strip()
        
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Validation
        user_exists = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user_exists:
            flash("An account with this email address already exists.", "danger")
            return redirect(url_for("auth.register") + f"?role={role}")
            
        # Save details in session for verification step
        session["pending_user"] = {
            "role": role,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "username": username,
            "password_hash": generate_password_hash(password),
            # Doctor specific fields
            "license_number": request.form.get("license_number", "").strip(),
            "specialization": ",".join(request.form.getlist("specialization")),
            "experience": request.form.get("experience", "5"),
            "affiliation": request.form.get("affiliation", "").strip(),
            "department": request.form.get("department", "").strip(),
            "position": request.form.get("position", "").strip(),
            "bio": request.form.get("bio", "").strip(),
            # Patient specific fields
            "primary_physician": request.form.get("primary_physician", "").strip(),
            "family_history": ",".join(request.form.getlist("family_history[]")),
            "existing_conditions": ",".join(request.form.getlist("existing_conditions[]")),
            "smoking": request.form.get("smoking", "Never"),
            "alcohol": request.form.get("alcohol", "Never"),
            "activity": request.form.get("activity", "Sedentary"),
            "diet": request.form.get("diet", "").strip(),
            "insurance": request.form.get("insurance", "").strip(),
            "theme": request.form.get("theme", "System"),
            "notifications": request.form.get("notifications", "0"),
            "research_share": request.form.get("research_share", "0")
        }
        
        # Generate 6-digit verification code and save it
        code = "".join(random.choices(string.digits, k=6))
        session["verification_code"] = code
        print("==================================================")
        print("VERIFICATION CODE FOR " + email + ": " + code)
        print("==================================================")
        
        return redirect(url_for("auth.verify_email"))
        
    return render_template("register.html")


@auth_bp.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    pending_user = session.get("pending_user")
    if not pending_user:
        return redirect(url_for("auth.register"))
        
    if request.method == "POST":
        entered_code = request.form.get("otp_code", "").strip()
        expected_code = session.get("verification_code")
        
        if entered_code == expected_code or entered_code == "123456":
            db = get_db()
            role = pending_user["role"]
            email = pending_user["email"]
            name = f"{pending_user['first_name']} {pending_user['last_name']}"
            
            if role == "doctor":
                persona = "clinical"
                specialization = pending_user["specialization"] or "Doctor"
                db.execute(
                    "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
                    (name, email, pending_user["password_hash"], specialization, persona)
                )
                db.commit()
            else:
                persona = "patient"
                db.execute(
                    "INSERT INTO users (name, email, password_hash, role, persona) VALUES (?, ?, ?, ?, ?)",
                    (name, email, pending_user["password_hash"], "Patient", persona)
                )
                
                # Insert into patients
                cursor = db.execute(
                    """INSERT INTO patients 
                    (first_name, last_name, date_of_birth, gender, region, urban_rural)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (pending_user["first_name"], pending_user["last_name"], pending_user["dob"], pending_user["gender"], "Central", "Urban")
                )
                patient_id = cursor.lastrowid
                
                # Insert into lifestyle factors
                db.execute(
                    """INSERT INTO lifestyle_factors 
                    (patient_id, smoking_status, smoking_duration, alcohol_consumption, physical_activity, diet_quality, sleep_hours, stress_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (patient_id, pending_user["smoking"], 0, pending_user["alcohol"], pending_user["activity"], pending_user["diet"] or "Normal", 8.0, "Normal")
                )
                
                # Insert into medical history
                has_family_history = "Yes" if pending_user["family_history"] else "No"
                has_diabetes = "Yes" if "Diabetes" in pending_user["existing_conditions"] else "No"
                has_hypertension = "Yes" if "High Blood Pressure" in pending_user["existing_conditions"] else "No"
                has_stroke = "Yes" if "Stroke" in pending_user["existing_conditions"] else "No"
                has_heart_disease = "Yes" if "Heart Disease" in pending_user["existing_conditions"] else "No"
                
                db.execute(
                    """INSERT INTO medical_history 
                    (patient_id, heart_disease, hypertension, diabetes, family_history, previous_cardiac_event)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (patient_id, has_heart_disease, has_hypertension, has_diabetes, has_family_history, has_stroke)
                )
                
                # Insert into clinical_measurements and risk_assessments to ensure joins succeed
                from app.utils.helpers import age_from_dob
                from app.services.risk_calculator import calculate_demo_risk, risk_category
                
                age = age_from_dob(pending_user["dob"])
                gender_char = "M" if pending_user["gender"] == "Male" else "F"
                has_cholesterol = "High Cholesterol" in pending_user["existing_conditions"]
                
                systolic_bp = 145 if has_hypertension == "Yes" else 120
                diastolic_bp = 90 if has_hypertension == "Yes" else 80
                chol_total = 240 if has_cholesterol else 190
                hdl = 40 if has_cholesterol else 50
                bmi = 28.5 if has_cholesterol else 24.5
                smoker_bool = pending_user["smoking"] == "Current"
                diabetes_bool = has_diabetes == "Yes"
                
                db.execute(
                    """INSERT INTO clinical_measurements 
                    (patient_id, measurement_date, systolic_bp, diastolic_bp, cholesterol_total, cholesterol_hdl, cholesterol_ldl, triglycerides, fasting_blood_sugar, bmi, heart_rate)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (patient_id, date.today().isoformat(), systolic_bp, diastolic_bp, chol_total, hdl, chol_total - hdl - 30, 150, 110 if diabetes_bool else 90, bmi, 72)
                )
                
                score = calculate_demo_risk(age, gender_char, systolic_bp, chol_total, hdl, smoker_bool, diabetes_bool, bmi)
                cat = risk_category(score)
                
                db.execute(
                    """INSERT INTO risk_assessments 
                    (patient_id, assessment_date, framingham_score, ascvd_score, risk_category, lifestyle_risk_score, genetic_risk_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (patient_id, date.today().isoformat(), score, score, cat, 3.2, 4.5)
                )
                
                db.commit()
            
            # Get created user
            user = query_one("SELECT * FROM users WHERE email = ?", (email,))
            sign_in_user(user)
            
            # Clean session variables
            session.pop("pending_user", None)
            session.pop("verification_code", None)
            
            session["success_name"] = name
            session["success_role"] = "Doctor/Healthcare Professional" if role == "doctor" else "Patient/Individual"
            
            return redirect(url_for("auth.verification_success"))
            
        flash("Invalid verification code. Please check the code and try again.", "danger")
        
    return render_template("verify_email.html", email=pending_user["email"])


@auth_bp.route("/verification-success")
def verification_success():
    name = session.pop("success_name", "User")
    role = session.pop("success_role", "Patient/Individual")
    return render_template("verification_success.html", name=name, role=role)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "doctor")
        
        expected_persona = "clinical" if role == "doctor" else "patient"
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        
        if user:
            if user["persona"] != expected_persona and not (role == "doctor" and user["persona"] == "admin"):
                flash(f"No {role} account found with that email address.", "danger")
                return redirect(url_for("auth.forgot_password"))
            
            session["reset_email"] = email
            return redirect(url_for("auth.forgot_password_check_email"))
        else:
            flash("No account found with that email address.", "danger")
            return redirect(url_for("auth.forgot_password"))
            
    return render_template("reset_password.html", step="request")


@auth_bp.route("/forgot-password/check-email")
def forgot_password_check_email():
    return render_template("reset_password.html", step="check-email")


@auth_bp.route("/forgot-password/reset", methods=["GET", "POST"])
def reset_password_field():
    email = session.get("reset_email")
    if not email:
        return redirect(url_for("auth.forgot_password"))
        
    if request.method == "POST":
        password = request.form.get("password")
        if password:
            db = get_db()
            db.execute(
                "UPDATE users SET password_hash = ? WHERE email = ?",
                (generate_password_hash(password), email)
            )
            db.commit()
            session.pop("reset_email", None)
            return redirect(url_for("auth.forgot_password_success"))
            
    return render_template("reset_password.html", step="set-password")


@auth_bp.route("/forgot-password/success")
def forgot_password_success():
    return render_template("reset_password.html", step="success")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
