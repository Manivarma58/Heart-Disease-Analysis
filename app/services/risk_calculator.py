def calculate_demo_risk(age, gender, systolic_bp, cholesterol_total, hdl, smoker, diabetes, bmi):
    """Approximate cardiovascular risk score for demo and education workflows."""
    score = 0
    score += max(0, age - 30) * 0.45
    score += 8 if gender == "M" else 5
    score += max(0, systolic_bp - 115) * 0.18
    score += max(0, cholesterol_total - 180) * 0.08
    score -= max(0, hdl - 45) * 0.05
    score += 9 if smoker else 0
    score += 7 if diabetes else 0
    score += max(0, bmi - 25) * 0.55
    return round(max(1, min(score, 35)), 1)


def risk_category(score):
    if score < 10:
        return "Low"
    if score < 20:
        return "Moderate"
    return "High"


def recommendation_for(category):
    return {
        "Low": "Maintain preventive habits and review annually.",
        "Moderate": "Schedule clinician review, improve activity, and monitor lipids.",
        "High": "Prioritize cardiology consult, medication review, and close follow-up.",
    }[category]
