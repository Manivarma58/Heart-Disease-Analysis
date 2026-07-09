from dataclasses import dataclass


@dataclass
class ClinicalMeasurement:
    patient_id: int
    systolic_bp: int
    diastolic_bp: int
    cholesterol_total: int
    bmi: float
    fasting_blood_sugar: int
