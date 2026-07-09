# Calculated Fields and Visualizations

## Number of Calculated Fields

The project includes 9 calculated fields in the Tableau-ready dataset and MySQL views.

Calculated fields are available in:

- CSV: `data/Heart_tableau_ready.csv`
- MySQL view: `tableau_visualization_ready`
- Script: `scripts/create_tableau_ready_csv.py`
- SQL: `scripts/mysql_schema.sql`

## Calculated Fields List

### 1. Heart Disease Flag

Purpose: Convert `Heart Disease` into a numeric measure.

Formula:

```text
IF [Heart Disease] = "Yes" THEN 1 ELSE 0 END
```

### 2. BMI Category

Purpose: Group BMI values into readable categories.

Formula:

```text
IF [BMI] < 18.5 THEN "Underweight"
ELSEIF [BMI] < 25 THEN "Normal"
ELSEIF [BMI] < 30 THEN "Overweight"
ELSE "Obese"
END
```

### 3. Obesity Flag

Purpose: Identify records with BMI of 30 or above.

Formula:

```text
IF [BMI] >= 30 THEN 1 ELSE 0 END
```

### 4. Total Unhealthy Days

Purpose: Combine physical and mental unhealthy days.

Formula:

```text
[Physical Health Days] + [Mental Health Days]
```

### 5. Age Sort

Purpose: Sort age categories correctly in Tableau.

Formula:

```text
Numeric starting value of [Age Category]
```

### 6. General Health Score

Purpose: Convert general health text into a numeric score.

Formula:

```text
Poor = 1
Fair = 2
Good = 3
Very good = 4
Excellent = 5
```

### 7. Sleep Quality

Purpose: Group sleep hours into health categories.

Formula:

```text
IF [Sleep Time] < 6 THEN "Poor (< 6 hrs)"
ELSEIF [Sleep Time] <= 9 THEN "Optimal (6-9 hrs)"
ELSE "Excessive (> 9 hrs)"
END
```

### 8. Risk Segment

Purpose: Classify records into `Low`, `Moderate`, and `High` risk.

Inputs:

- Heart disease
- Smoking
- Stroke
- Diabetes
- Kidney disease
- BMI
- Physical activity
- General health

### 9. High Risk Flag

Purpose: Convert `Risk Segment` into a numeric high-risk indicator.

Formula:

```text
IF [Risk Segment] = "High" THEN 1 ELSE 0 END
```

## Number of Visualizations / Graphs

The project includes 10 visualization topics for Tableau/dashboard analysis.

## Visualization List

### 1. Gender Wise Heart Disease

Chart type: Stacked bar chart

Purpose: Compare heart disease cases across male and female groups.

### 2. Age Wise Heart Disease

Chart type: Vertical bar chart or line chart

Purpose: Show how heart disease rate changes across age categories.

### 3. People Suffering from Diabetic and Stroke

Chart type: Bubble chart or grouped bar chart

Purpose: Compare diabetic status with stroke history.

### 4. Impact of Smoking and Alcohol Drinking on Heart Disease

Chart type: Grouped horizontal bar chart

Purpose: Analyze how smoking and alcohol drinking relate to heart disease outcomes.

### 5. Other Diseases vs Stroke

Chart type: Grouped bar chart

Purpose: Compare stroke cases among people with asthma, kidney disease, and skin cancer.

### 6. Race Wise Heart Disease

Chart type: Pie chart, donut chart, or bar chart

Purpose: Show heart disease distribution by race.

### 7. General Health vs Heart Disease

Chart type: Bar chart

Purpose: Compare heart disease rates across general health categories.

### 8. Physical Activity vs Heart Disease

Chart type: Bar chart

Purpose: Show how active and inactive groups differ in heart disease outcomes.

### 9. Age and BMI vs Heart Disease

Chart type: Scatter plot or age-category bar chart

Purpose: Analyze BMI patterns by age and heart disease risk.

### 10. People Got Stroke Suffering from Diabetes and Heart Disease

Chart type: Cohort bar chart

Purpose: Identify stroke overlap among patients with diabetes, heart disease, both, or neither.

## Dashboard Implementation

The web dashboard route includes all 10 visualization topics:

```text
/dashboard/tableau-style
```

The Tableau-ready MySQL views for these visualizations are included in:

```text
scripts/mysql_schema.sql
```
