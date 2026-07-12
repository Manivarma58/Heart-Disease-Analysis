from flask import current_app


def powerbi_view_for(role):
    config_key = {
        "clinical": "POWERBI_CLINICAL_URL",
        "public_health": "POWERBI_PUBLIC_HEALTH_URL",
        "patient": "POWERBI_PATIENT_URL",
        "dashboard": "POWERBI_DASHBOARD_URL",
    }.get(role)
    return current_app.config.get(config_key, "") if config_key else ""


def powerbi_status(role):
    url = powerbi_view_for(role)
    return {
        "configured": bool(url),
        "url": url,
        "message": "Live Power BI view configured." if url else "Demo Power BI analytics shown. Add a Power BI URL in .env to embed a live report.",
    }
