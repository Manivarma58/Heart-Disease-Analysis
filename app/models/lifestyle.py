from dataclasses import dataclass


@dataclass
class LifestyleFactor:
    patient_id: int
    smoking_status: str
    physical_activity: str
    diet_quality: str
    stress_level: str
