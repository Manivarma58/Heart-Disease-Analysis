import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-datavibe-change-me")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "datavibe.db"))
    TABLEAU_CLINICAL_URL = os.getenv("TABLEAU_CLINICAL_URL", "")
    TABLEAU_PUBLIC_HEALTH_URL = os.getenv("TABLEAU_PUBLIC_HEALTH_URL", "")
    TABLEAU_PATIENT_URL = os.getenv("TABLEAU_PATIENT_URL", "")
    TABLEAU_DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", "")
    TABLEAU_STORY_URL = os.getenv("TABLEAU_STORY_URL", "")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
