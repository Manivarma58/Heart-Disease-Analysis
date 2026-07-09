CREATE INDEX IF NOT EXISTS idx_patients_region ON patients(region);
CREATE INDEX IF NOT EXISTS idx_patients_area ON patients(urban_rural);
CREATE INDEX IF NOT EXISTS idx_risk_patient ON risk_assessments(patient_id);
CREATE INDEX IF NOT EXISTS idx_risk_category ON risk_assessments(risk_category);

CREATE VIEW IF NOT EXISTS high_risk_patients AS
SELECT p.patient_id, p.region, p.urban_rural, r.framingham_score, r.ascvd_score, r.risk_category
FROM patients p
JOIN risk_assessments r ON r.patient_id = p.patient_id
WHERE r.risk_category = 'High';

CREATE VIEW IF NOT EXISTS population_health_statistics AS
SELECT p.region, p.urban_rural, COUNT(*) AS patient_count,
       AVG(r.framingham_score) AS average_risk,
       SUM(CASE WHEN m.heart_disease = 'Yes' THEN 1 ELSE 0 END) AS heart_disease_cases
FROM patients p
JOIN risk_assessments r ON r.patient_id = p.patient_id
JOIN medical_history m ON m.patient_id = p.patient_id
GROUP BY p.region, p.urban_rural;
