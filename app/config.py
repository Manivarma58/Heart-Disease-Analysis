import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-cardioviz-change-me")
    
    # On serverless platforms like Vercel, the repository root is read-only.
    # We copy our default seeded SQLite database to /tmp so database writes function.
    if os.getenv("VERCEL") or os.environ.get("VERCEL_ENV"):
        import shutil
        original_db = BASE_DIR / "datavibe.db"
        target_db = Path("/tmp") / "datavibe.db"
        if original_db.exists() and not target_db.exists():
            try:
                shutil.copy2(original_db, target_db)
            except Exception as e:
                print("Error copying database to /tmp:", e)
        DATABASE_PATH = str(target_db)
    else:
        DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "datavibe.db"))
    TABLEAU_CLINICAL_URL = os.getenv("TABLEAU_CLINICAL_URL", "")
    TABLEAU_PUBLIC_HEALTH_URL = os.getenv("TABLEAU_PUBLIC_HEALTH_URL", "")
    TABLEAU_PATIENT_URL = os.getenv("TABLEAU_PATIENT_URL", "")
    TABLEAU_DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", "")
    TABLEAU_STORY_URL = os.getenv("TABLEAU_STORY_URL", "")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
