USE cardioviz_heart;

TRUNCATE TABLE heart_raw;
TRUNCATE TABLE heart_clean;

LOAD DATA LOCAL INFILE 'Heart_new2.csv'
INTO TABLE heart_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(HeartDisease, BMI, Smoking, AlcoholDrinking, Stroke, PhysicalHealth, MentalHealth,
 DiffWalking, Sex, AgeCategory, Race, Diabetic, PhysicalActivity, GenHealth,
 SleepTime, Asthma, KidneyDisease, SkinCancer);

LOAD DATA LOCAL INFILE 'Heart_new2_clean.csv'
INTO TABLE heart_clean
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(HeartDisease, BMI, Smoking, AlcoholDrinking, Stroke, PhysicalHealth, MentalHealth,
 DiffWalking, Sex, AgeCategory, Race, Diabetic, PhysicalActivity, GenHealth,
 SleepTime, Asthma, KidneyDisease, SkinCancer);
