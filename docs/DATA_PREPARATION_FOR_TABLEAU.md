# Data Preparation for Tableau

## Description

This phase prepares the heart disease dataset for accurate and meaningful Tableau visualization. The source dataset was already mostly clean, but a final preparation process was completed to confirm quality, improve field clarity, add calculated fields, and organize the data for dashboard development.

## Prepared Files

- Original dataset: `data/Heart_new2.csv`
- Clean dataset: `data/Heart_new2_clean.csv`
- Tableau-ready dataset: `data/Heart_tableau_ready.csv`
- Validation report: `docs/DATASET_VALIDATION_REPORT.json`
- SQL preparation script: `scripts/mysql_schema.sql`
- Tableau-ready CSV generator: `scripts/create_tableau_ready_csv.py`

## Data Review and Exploration

The dataset was reviewed before visualization to understand its structure and confirm analysis readiness.

Review results:

- Total source records: 4,500
- Final clean records: 4,494
- Total columns: 18
- Missing values: 0
- Duplicate records removed: 6
- Invalid records removed: 0
- Target variable: `HeartDisease`

Key fields reviewed:

- Demographics: `Sex`, `AgeCategory`, `Race`
- Lifestyle factors: `Smoking`, `AlcoholDrinking`, `PhysicalActivity`, `SleepTime`
- Health indicators: `BMI`, `Stroke`, `Diabetic`, `GenHealth`, `Asthma`, `KidneyDisease`, `SkinCancer`
- Wellbeing metrics: `PhysicalHealth`, `MentalHealth`, `DiffWalking`

## Cleaning and Consistency

The final preparation process confirmed:

- No null or blank values.
- Boolean fields consistently use `Yes` and `No`.
- Numeric fields such as `BMI`, `PhysicalHealth`, `MentalHealth`, and `SleepTime` are valid.
- Duplicate rows were removed from the clean dataset.
- Field values are consistent enough for Tableau grouping and filtering.

## Filtering and Structuring for Purpose

The dataset was structured around the project goal: heart disease risk analysis.

Recommended Tableau filters:

- `Heart Disease`
- `Age Category`
- `Sex`
- `Race`
- `BMI Category`
- `Smoking Status`
- `Diabetic Status`
- `Physical Activity`
- `General Health`
- `Risk Segment`

These filters support the three dashboard personas:

- Clinical dashboard: patient risk factors, BMI, diabetes, stroke, and smoking.
- Public health dashboard: population trends by age, race, sex, and lifestyle.
- Patient dashboard: personal health indicators and risk category.

## Field Renaming and Final Formatting

To make Tableau dashboards easier to understand, a Tableau-ready dataset was created with readable field names.

Examples:

- `HeartDisease` became `Heart Disease`
- `PhysicalHealth` became `Physical Health Days`
- `MentalHealth` became `Mental Health Days`
- `DiffWalking` became `Difficulty Walking`
- `AgeCategory` became `Age Category`
- `PhysicalActivity` became `Physical Activity`
- `GenHealth` became `General Health`
- `KidneyDisease` became `Kidney Disease`

The MySQL view `tableau_visualization_ready` applies the same naming logic for Tableau database connections.

## Calculated Fields

Several calculated fields were created to make visualization easier and more insightful.

### Heart Disease Flag

Converts the outcome into a numeric field for aggregation.

```text
IF [Heart Disease] = "Yes" THEN 1 ELSE 0 END
```

Use:

- Disease rate
- Case count
- Percentage charts

### BMI Category

Groups BMI into standard categories.

```text
IF [BMI] < 18.5 THEN "Underweight"
ELSEIF [BMI] < 25 THEN "Normal"
ELSEIF [BMI] < 30 THEN "Overweight"
ELSE "Obese"
END
```

Use:

- BMI distribution charts
- BMI versus heart disease comparison

### Age Sort

Creates a numeric sorting field for age categories.

Use:

- Correct ordering of `18-24`, `25-29`, through `80 or older`

### General Health Score

Converts general health categories into numeric scores.

```text
Poor = 1
Fair = 2
Good = 3
Very good = 4
Excellent = 5
```

Use:

- Trend analysis
- Average health score by group

### Risk Segment

Creates an easy risk category for dashboards.

The segment uses a weighted points-based scoring system (up to 18 points total) to categorize patients:
- **Heart Disease**: 5 points if Heart Disease is 'Yes'
- **Stroke History**: 3 points if Stroke is 'Yes'
- **Kidney Disease**: 2 points if Kidney Disease is 'Yes'
- **Diabetic Status**: 2 points if Diabetic Status is anything other than 'No'
- **Obesity (BMI >= 30)**: 2 points if BMI >= 30
- **Smoking Status**: 2 points if Smoking Status is 'Yes'
- **Physical Activity**: 1 point if Physical Activity is 'No'
- **General Health**: 1 point if General Health is 'Fair' or 'Poor' (General Health Score <= 2)

Risk levels:
- **High**: 8 or more points (represents multiple combined clinical conditions or key chronic diseases)
- **Moderate**: 4 to 7 points (represents combined lifestyle risk factors or early signs of health issues)
- **Low**: 0 to 3 points (represents minimal risk factors)

### Obesity Flag

A binary flag to identify patients with BMI >= 30, which is the clinical threshold for obesity.

```text
IF [BMI] >= 30 THEN 1 ELSE 0 END
```

Use:

- Rapid population obesity rate reporting
- Quick patient-level sorting in clinical worklists

### Total Unhealthy Days

The sum of `Physical Health Days` and `Mental Health Days` (maximum of 60 days total), indicating overall patient wellbeing status over the past 30 days.

```text
[Physical Health Days] + [Mental Health Days]
```

Use:

- Correlation analysis between lifestyle factors and overall unhealthy duration
- Patient wellbeing profiling

### Sleep Quality

Groups sleep hours into qualitative intervals to highlight bad sleep habits.

```text
IF [Sleep Time] < 6 THEN "Poor (< 6 hrs)"
ELSEIF [Sleep Time] <= 9 THEN "Optimal (6-9 hrs)"
ELSE "Excessive (> 9 hrs)"
END
```

Use:

- Lifestyle risk factors vs sleep habits breakdown in dashboards
- Patient advisory recommendations

### High Risk Flag

A binary flag indicating whether the patient falls into the `High` Risk Segment category.

```text
IF [Risk Segment] = "High" THEN 1 ELSE 0 END
```

Use:

- Direct aggregation of high-risk cases count
- Percentage of total patients marked as high risk

## Tableau-Ready SQL View

The database includes a dedicated Tableau view:

```sql
tableau_visualization_ready
```

This view provides:

- Friendly column names
- Calculated fields
- BMI categories
- Risk segments
- Numeric flags
- Age sorting field

Use this view as the main Tableau data source when connecting through MySQL.

## Validation for Accuracy

Validation was performed using:

```powershell
.\.venv\Scripts\python scripts\validate_and_prepare_dataset.py
```

The output report confirms the dataset is ready for visualization:

- `docs/DATASET_VALIDATION_REPORT.json`

The Tableau-ready CSV can be regenerated using:

```powershell
.\.venv\Scripts\python scripts\create_tableau_ready_csv.py
```

## Final Tableau Preparation Status

The dataset is ready for Tableau visualization. It has been cleaned, reviewed, deduplicated, renamed for clarity, enriched with calculated fields, and structured for clinical, public health, and patient-focused dashboards.
