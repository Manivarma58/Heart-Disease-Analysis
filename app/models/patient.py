from dataclasses import dataclass


@dataclass
class Patient:
    patient_id: int
    first_name: str
    last_name: str
    age: int
    gender: str
    region: str
    urban_rural: str
