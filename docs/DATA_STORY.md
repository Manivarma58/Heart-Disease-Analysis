# Heart Disease Data Story

## Story

### Description

A data story presents analysis in a narrative format so that users can understand not only what the data shows, but also why the findings matter. For the Heart Disease Analysis project, the story guides users through key health patterns step by step: starting with the dataset context, moving through demographic and lifestyle comparisons, and ending with practical insights for prevention and dashboard design.

The story is available in the Flask application at:

```text
/story/heart-disease
```

## Number of Scenes of Story

The Heart Disease Story contains 6 scenes. This number is appropriate because the analysis covers multiple dimensions: dataset context, gender, physical activity, diabetes and stroke, smoking and alcohol, and final insights.

## Storyboard Scenes

### Scene 1: Understanding the Heart Disease Dataset

Purpose:

Introduce the dataset and explain the analysis context.

Visuals:

- Total records
- Heart disease cases
- Observed disease rate

Insight:

The dataset provides enough records and variables to analyze heart disease patterns across clinical, demographic, and lifestyle factors.

### Scene 2: Gender Shows Different Case Volumes

Purpose:

Compare heart disease distribution by sex.

Visuals:

- Stacked bar chart for Female and Male groups
- Heart disease status split into Yes and No

Insight:

Gender comparison gives an initial demographic view before deeper clinical and lifestyle analysis.

### Scene 3: Physical Activity Helps Separate Risk Groups

Purpose:

Analyze the relationship between physical activity and heart disease status.

Visuals:

- Horizontal bar chart comparing active and inactive groups

Insight:

Physical activity is an actionable factor, making it useful for patient education and prevention planning.

### Scene 4: Diabetes and Stroke Add Clinical Context

Purpose:

Show how comorbidities relate to heart disease risk.

Visuals:

- Bubble chart for diabetic status and stroke history

Insight:

Diabetes and stroke history help identify clinically important risk groups.

### Scene 5: Smoking and Alcohol Shape Lifestyle Risk

Purpose:

Explore how smoking and alcohol drinking combine with heart disease outcomes.

Visuals:

- Horizontal bar chart grouped by smoking, alcohol, and heart disease status

Insight:

Lifestyle factors provide practical intervention points for reducing heart disease risk.

### Scene 6: Key Finding and Conclusion

Purpose:

Summarize the story and highlight implications.

Visuals:

- Age category trend chart

Insight:

Heart disease analysis becomes more useful when age, lifestyle habits, and clinical conditions are studied together. Dashboards should support filtering by age, sex, activity, diabetes, stroke, smoking, BMI, and general health.

## Story Design

The story is designed like a Tableau Story:

- Scene navigation tabs appear at the top.
- Each scene contains narrative text and one focused visual.
- The story progresses from broad context to specific risk drivers.
- The final scene summarizes insights and connects them to healthcare decision-making.

## Files

- Route: `app/routes/dashboard.py`
- Template: `app/templates/dashboard/heart_story.html`
- Styling: `app/static/css/datavibe.css`
- Documentation: `docs/DATA_STORY.md`
