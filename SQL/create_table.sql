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

