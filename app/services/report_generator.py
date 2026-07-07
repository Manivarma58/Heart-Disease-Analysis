from datetime import datetime

from app.services.database_service import query_all


def population_report():
    rows = query_all(
        """SELECT p.region, COUNT(*) AS patients,
                  ROUND(AVG(r.framingham_score), 1) AS avg_risk,
                  SUM(CASE WHEN r.risk_category='High' THEN 1 ELSE 0 END) AS high_risk
           FROM patients p
           JOIN risk_assessments r ON r.patient_id = p.patient_id
           GROUP BY p.region
           ORDER BY high_risk DESC"""
    )
    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "regions": rows,
    }
