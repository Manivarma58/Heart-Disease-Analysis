from flask import current_app


def powerbi_view_for(role):
    config_key = {
        "clinical": "TABLEAU_CLINICAL_URL",
        "public_health": "TABLEAU_PUBLIC_HEALTH_URL",
        "patient": "TABLEAU_PATIENT_URL",
        "dashboard": "TABLEAU_DASHBOARD_URL",
    }.get(role)
    return current_app.config.get(config_key, "") if config_key else ""


def powerbi_status(role):
    url = powerbi_view_for(role)
    return {
        "configured": bool(url),
        "url": url,
        "message": "Live Tableau view configured." if url else "Demo Tableau analytics shown. Add a Tableau URL in .env to embed a live report.",
    }
