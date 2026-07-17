CREATE DATABASE IF NOT EXISTS cardioviz_heart;
USE cardioviz_heart;

CREATE TABLE IF NOT EXISTS heart_raw (
  raw_id INT AUTO_INCREMENT PRIMARY KEY,
  HeartDisease VARCHAR(8),
  BMI DECIMAL(5,2),
  Smoking VARCHAR(8),
  AlcoholDrinking VARCHAR(8),
  Stroke VARCHAR(8),
  PhysicalHealth INT,
  MentalHealth INT,
  DiffWalking VARCHAR(8),
  Sex VARCHAR(12),
  AgeCategory VARCHAR(20),
  Race VARCHAR(60),
  Diabetic VARCHAR(40),
  PhysicalActivity VARCHAR(8),
  GenHealth VARCHAR(20),
  SleepTime DECIMAL(4,1),
  Asthma VARCHAR(8),
  KidneyDisease VARCHAR(8),
  SkinCancer VARCHAR(8)
);

CREATE TABLE IF NOT EXISTS heart_clean (
  record_id INT AUTO_INCREMENT PRIMARY KEY,
  HeartDisease VARCHAR(8) NOT NULL,
  BMI DECIMAL(5,2) NOT NULL,
  Smoking VARCHAR(8) NOT NULL,
  AlcoholDrinking VARCHAR(8) NOT NULL,
  Stroke VARCHAR(8) NOT NULL,
  PhysicalHealth INT NOT NULL,
  MentalHealth INT NOT NULL,
  DiffWalking VARCHAR(8) NOT NULL,
  Sex VARCHAR(12) NOT NULL,
  AgeCategory VARCHAR(20) NOT NULL,
  Race VARCHAR(60) NOT NULL,
  Diabetic VARCHAR(40) NOT NULL,
  PhysicalActivity VARCHAR(8) NOT NULL,
  GenHealth VARCHAR(20) NOT NULL,
  SleepTime DECIMAL(4,1) NOT NULL,
  Asthma VARCHAR(8) NOT NULL,
  KidneyDisease VARCHAR(8) NOT NULL,
  SkinCancer VARCHAR(8) NOT NULL,
  CHECK (HeartDisease IN ('Yes', 'No')),
  CHECK (Smoking IN ('Yes', 'No')),
  CHECK (AlcoholDrinking IN ('Yes', 'No')),
  CHECK (Stroke IN ('Yes', 'No')),
  CHECK (PhysicalActivity IN ('Yes', 'No')),
  CHECK (BMI > 0),
  CHECK (PhysicalHealth BETWEEN 0 AND 30),
  CHECK (MentalHealth BETWEEN 0 AND 30),
  CHECK (SleepTime BETWEEN 0 AND 24)
);

CREATE INDEX idx_heart_clean_outcome ON heart_clean(HeartDisease);
CREATE INDEX idx_heart_clean_age_sex ON heart_clean(AgeCategory, Sex);
CREATE INDEX idx_heart_clean_lifestyle ON heart_clean(Smoking, PhysicalActivity, Diabetic);

CREATE OR REPLACE VIEW heart_analysis_ready AS
SELECT
  record_id,
  HeartDisease,
  CASE WHEN HeartDisease = 'Yes' THEN 1 ELSE 0 END AS heart_disease_flag,
  BMI,
  CASE
    WHEN BMI < 18.5 THEN 'Underweight'
    WHEN BMI < 25 THEN 'Normal'
    WHEN BMI < 30 THEN 'Overweight'
    ELSE 'Obese'
  END AS bmi_category,
  CASE WHEN BMI >= 30 THEN 1 ELSE 0 END AS obesity_flag,
  Smoking,
  AlcoholDrinking,
  Stroke,
  PhysicalHealth,
  MentalHealth,
  (PhysicalHealth + MentalHealth) AS total_unhealthy_days,
  DiffWalking,
  Sex,
  AgeCategory,
  Race,
  Diabetic,
  PhysicalActivity,
  GenHealth,
  CASE GenHealth
    WHEN 'Excellent' THEN 5
    WHEN 'Very good' THEN 4
    WHEN 'Good' THEN 3
    WHEN 'Fair' THEN 2
    ELSE 1
  END AS gen_health_score,
  SleepTime,
  CASE
    WHEN SleepTime < 6 THEN 'Poor (< 6 hrs)'
    WHEN SleepTime <= 9 THEN 'Optimal (6-9 hrs)'
    ELSE 'Excessive (> 9 hrs)'
  END AS sleep_quality,
  Asthma,
  KidneyDisease,
  SkinCancer
FROM heart_clean;

CREATE OR REPLACE VIEW tableau_visualization_ready AS
SELECT
  record_id AS `Record ID`,
  HeartDisease AS `Heart Disease`,
  heart_disease_flag AS `Heart Disease Flag`,
  BMI,
  bmi_category AS `BMI Category`,
  obesity_flag AS `Obesity Flag`,
  Smoking AS `Smoking Status`,
  AlcoholDrinking AS `Alcohol Drinking`,
  Stroke AS `Stroke History`,
  PhysicalHealth AS `Physical Health Days`,
  MentalHealth AS `Mental Health Days`,
  total_unhealthy_days AS `Total Unhealthy Days`,
  DiffWalking AS `Difficulty Walking`,
  Sex,
  AgeCategory AS `Age Category`,
  CASE
    WHEN AgeCategory = '80 or older' THEN 80
    ELSE CAST(SUBSTRING_INDEX(AgeCategory, '-', 1) AS UNSIGNED)
  END AS `Age Sort`,
  Race,
  Diabetic AS `Diabetic Status`,
  PhysicalActivity AS `Physical Activity`,
  GenHealth AS `General Health`,
  gen_health_score AS `General Health Score`,
  SleepTime AS `Sleep Time`,
  sleep_quality AS `Sleep Quality`,
  Asthma,
  KidneyDisease AS `Kidney Disease`,
  SkinCancer AS `Skin Cancer`,
  CASE
    WHEN (
      (CASE WHEN HeartDisease = 'Yes' THEN 5 ELSE 0 END) +
      (CASE WHEN Smoking = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN Stroke = 'Yes' THEN 3 ELSE 0 END) +
      (CASE WHEN Diabetic <> 'No' THEN 2 ELSE 0 END) +
      (CASE WHEN KidneyDisease = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN BMI >= 30 THEN 2 ELSE 0 END) +
      (CASE WHEN PhysicalActivity = 'No' THEN 1 ELSE 0 END) +
      (CASE WHEN gen_health_score <= 2 THEN 1 ELSE 0 END)
    ) >= 8 THEN 'High'
    WHEN (
      (CASE WHEN HeartDisease = 'Yes' THEN 5 ELSE 0 END) +
      (CASE WHEN Smoking = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN Stroke = 'Yes' THEN 3 ELSE 0 END) +
      (CASE WHEN Diabetic <> 'No' THEN 2 ELSE 0 END) +
      (CASE WHEN KidneyDisease = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN BMI >= 30 THEN 2 ELSE 0 END) +
      (CASE WHEN PhysicalActivity = 'No' THEN 1 ELSE 0 END) +
      (CASE WHEN gen_health_score <= 2 THEN 1 ELSE 0 END)
    ) >= 4 THEN 'Moderate'
    ELSE 'Low'
  END AS `Risk Segment`,
  CASE
    WHEN (
      (CASE WHEN HeartDisease = 'Yes' THEN 5 ELSE 0 END) +
      (CASE WHEN Smoking = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN Stroke = 'Yes' THEN 3 ELSE 0 END) +
      (CASE WHEN Diabetic <> 'No' THEN 2 ELSE 0 END) +
      (CASE WHEN KidneyDisease = 'Yes' THEN 2 ELSE 0 END) +
      (CASE WHEN BMI >= 30 THEN 2 ELSE 0 END) +
      (CASE WHEN PhysicalActivity = 'No' THEN 1 ELSE 0 END) +
      (CASE WHEN gen_health_score <= 2 THEN 1 ELSE 0 END)
    ) >= 8 THEN 1
    ELSE 0
  END AS `High Risk Flag`
FROM heart_analysis_ready;

CREATE OR REPLACE VIEW tableau_population_overview AS
SELECT
  AgeCategory,
  Sex,
  Race,
  GenHealth,
  COUNT(*) AS records,
  SUM(CASE WHEN HeartDisease = 'Yes' THEN 1 ELSE 0 END) AS heart_disease_cases,
  ROUND(100 * AVG(CASE WHEN HeartDisease = 'Yes' THEN 1 ELSE 0 END), 2) AS disease_rate_pct,
  ROUND(AVG(BMI), 2) AS avg_bmi,
  ROUND(AVG(SleepTime), 2) AS avg_sleep_time
FROM heart_raw
GROUP BY AgeCategory, Sex, Race, GenHealth;

CREATE OR REPLACE VIEW tableau_population_overview_clean AS
SELECT
  AgeCategory,
  Sex,
  Race,
  GenHealth,
  COUNT(*) AS records,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100 * AVG(heart_disease_flag), 2) AS disease_rate_pct,
  ROUND(AVG(BMI), 2) AS avg_bmi,
  ROUND(AVG(SleepTime), 2) AS avg_sleep_time
FROM heart_analysis_ready
GROUP BY AgeCategory, Sex, Race, GenHealth;

CREATE OR REPLACE VIEW tableau_lifestyle_risk AS
SELECT
  Smoking,
  AlcoholDrinking,
  PhysicalActivity,
  Diabetic,
  COUNT(*) AS records,
  ROUND(100 * AVG(CASE WHEN HeartDisease = 'Yes' THEN 1 ELSE 0 END), 2) AS disease_rate_pct,
  ROUND(AVG(PhysicalHealth), 2) AS avg_physical_unhealthy_days,
  ROUND(AVG(MentalHealth), 2) AS avg_mental_unhealthy_days
FROM heart_raw
GROUP BY Smoking, AlcoholDrinking, PhysicalActivity, Diabetic;

CREATE OR REPLACE VIEW tableau_lifestyle_risk_clean AS
SELECT
  Smoking,
  AlcoholDrinking,
  PhysicalActivity,
  Diabetic,
  bmi_category,
  COUNT(*) AS records,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100 * AVG(heart_disease_flag), 2) AS disease_rate_pct,
  ROUND(AVG(PhysicalHealth), 2) AS avg_physical_unhealthy_days,
  ROUND(AVG(MentalHealth), 2) AS avg_mental_unhealthy_days
FROM heart_analysis_ready
GROUP BY Smoking, AlcoholDrinking, PhysicalActivity, Diabetic, bmi_category;

CREATE OR REPLACE VIEW tableau_patient_monitoring AS
SELECT
  raw_id AS patient_number,
  HeartDisease,
  BMI,
  Smoking,
  Stroke,
  DiffWalking,
  Sex,
  AgeCategory,
  Diabetic,
  PhysicalActivity,
  GenHealth,
  SleepTime,
  Asthma,
  KidneyDisease
FROM heart_raw;

-- ==========================================
-- Tableau Visualization Views for Subtasks
-- ==========================================

-- 1. Gender vs Heart Disease
CREATE OR REPLACE VIEW view_viz_gender_heart_disease AS
SELECT
  Sex,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY Sex;

-- 2. Age vs Heart Disease
CREATE OR REPLACE VIEW view_viz_age_heart_disease AS
SELECT
  AgeCategory,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY AgeCategory;

-- 3. Diabetic vs Stroke
CREATE OR REPLACE VIEW view_viz_diabetic_stroke AS
SELECT
  Diabetic AS diabetic_status,
  COUNT(*) AS total_patients,
  SUM(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END) AS stroke_cases,
  ROUND(100.0 * AVG(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END), 2) AS stroke_rate_pct
FROM heart_analysis_ready
GROUP BY Diabetic;

-- 4. Impact of Smoking and Alcohol on Heart Disease
CREATE OR REPLACE VIEW view_viz_smoking_alcohol_heart AS
SELECT
  Smoking AS smoking_status,
  AlcoholDrinking AS alcohol_drinking,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY Smoking, AlcoholDrinking;

-- 5. Other Health Diseases (Asthma, Kidney Disease, Skin Cancer) vs Stroke
CREATE OR REPLACE VIEW view_viz_other_diseases_stroke AS
SELECT
  'Asthma' AS condition_name,
  Asthma AS status,
  COUNT(*) AS total_patients,
  SUM(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END) AS stroke_cases,
  ROUND(100.0 * AVG(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END), 2) AS stroke_rate_pct
FROM heart_analysis_ready
GROUP BY Asthma
UNION ALL
SELECT
  'Kidney Disease' AS condition_name,
  KidneyDisease AS status,
  COUNT(*) AS total_patients,
  SUM(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END) AS stroke_cases,
  ROUND(100.0 * AVG(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END), 2) AS stroke_rate_pct
FROM heart_analysis_ready
GROUP BY KidneyDisease
UNION ALL
SELECT
  'Skin Cancer' AS condition_name,
  SkinCancer AS status,
  COUNT(*) AS total_patients,
  SUM(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END) AS stroke_cases,
  ROUND(100.0 * AVG(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END), 2) AS stroke_rate_pct
FROM heart_analysis_ready
GROUP BY SkinCancer;

-- 6. Race wise Heart Disease
CREATE OR REPLACE VIEW view_viz_race_heart_disease AS
SELECT
  Race,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY Race;

-- 7. General Health vs Heart Disease
CREATE OR REPLACE VIEW view_viz_gen_health_heart AS
SELECT
  GenHealth AS general_health,
  gen_health_score,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY GenHealth, gen_health_score;

-- 8. Physical Activity vs Heart Disease
CREATE OR REPLACE VIEW view_viz_activity_heart_disease AS
SELECT
  PhysicalActivity AS physical_activity,
  COUNT(*) AS total_patients,
  SUM(heart_disease_flag) AS heart_disease_cases,
  ROUND(100.0 * AVG(heart_disease_flag), 2) AS disease_rate_pct
FROM heart_analysis_ready
GROUP BY PhysicalActivity;

-- 9. Age and BMI vs Diabetic
CREATE OR REPLACE VIEW view_viz_age_bmi_diabetic AS
SELECT
  record_id,
  AgeCategory,
  CASE
    WHEN AgeCategory = '80 or older' THEN 80
    ELSE CAST(SUBSTRING_INDEX(AgeCategory, '-', 1) AS UNSIGNED)
  END AS age_sort,
  BMI,
  Diabetic AS diabetic_status
FROM heart_analysis_ready;

-- 10. Stroke Overlap in Heart Disease and Diabetic Cohorts
CREATE OR REPLACE VIEW view_viz_stroke_heart_diabetic_overlap AS
SELECT
  CASE
    WHEN HeartDisease = 'Yes' AND Diabetic <> 'No' THEN 'Both (Heart Disease & Diabetes)'
    WHEN HeartDisease = 'Yes' AND Diabetic = 'No' THEN 'Heart Disease Only'
    WHEN HeartDisease = 'No' AND Diabetic <> 'No' THEN 'Diabetes Only'
    ELSE 'Neither'
  END AS patient_cohort,
  COUNT(*) AS total_patients,
  SUM(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END) AS stroke_cases,
  ROUND(100.0 * AVG(CASE WHEN Stroke = 'Yes' THEN 1 ELSE 0 END), 2) AS stroke_rate_pct
FROM heart_analysis_ready
GROUP BY patient_cohort;
