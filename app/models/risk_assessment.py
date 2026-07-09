from dataclasses import dataclass


@dataclass
class RiskAssessment:
    patient_id: int
    framingham_score: float
    ascvd_score: float
    risk_category: str
