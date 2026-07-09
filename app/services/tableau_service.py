from flask import current_app


def tableau_view_for(role):
    config_key = {
        "clinical": "TABLEAU_CLINICAL_URL",
        "public_health": "TABLEAU_PUBLIC_HEALTH_URL",
        "patient": "TABLEAU_PATIENT_URL",
        "dashboard": "TABLEAU_DASHBOARD_URL",
        "story": "TABLEAU_STORY_URL",
    }.get(role)
    return current_app.config.get(config_key, "") if config_key else ""


def tableau_status(role):
    url = tableau_view_for(role)
    return {
        "configured": bool(url),
        "url": url,
        "message": "Live Tableau view configured." if url else "Demo analytics shown. Add a Tableau URL in .env to embed a live workbook.",
    }
