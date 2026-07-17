# Dashboard

## Description

The CardioViz dashboard is a graphical user interface that organizes heart disease data into clear, easy-to-read visual sections. It supports healthcare analysis by showing key metrics, charts, risk patterns, and population-level comparisons in one place.

The dashboard is designed for heart disease analysis and includes:

- KPI cards for total records, heart disease cases, disease rate, and average BMI.
- Gender versus heart disease comparison.
- Diabetic versus stroke relationship.
- Race-wise heart disease distribution.
- Smoking and alcohol impact analysis.
- Heart disease rate by age category.
- Other diseases versus stroke.
- General health versus heart disease.
- Physical activity versus heart disease.
- Age and BMI versus heart disease.
- Stroke overlap among diabetes and heart disease cohorts.
- Legend and dashboard control panel.

The dashboard page is available at:

```text
/dashboard/tableau-style
```

## Responsive and Design of Dashboard

The dashboard uses a responsive layout so it works on desktop, tablet, and mobile screens.

### Desktop Layout

On desktop, the dashboard uses a two-column analytics layout:

- Main visualization area for charts.
- Right-side legend and control panel.
- KPI cards across the top.
- Larger charts arranged in a grid.

### Tablet Layout

On tablet screens:

- KPI cards wrap into fewer columns.
- Chart cards stack more compactly.
- The legend moves below the main chart area when space is limited.

### Mobile Layout

On mobile screens:

- Dashboard cards become single-column.
- Horizontal charts simplify into readable stacked rows.
- Legends and controls remain visible without overlapping charts.
- Fonts and spacing remain touch-friendly.

## Visualization Design

The dashboard uses:

- Blue and orange to distinguish heart disease status.
- Card-based chart sections for readability.
- Consistent labels and chart titles.
- Clear chart spacing to avoid visual clutter.
- Responsive CSS grid layouts.

## Tableau Alignment

The dashboard design follows the same structure used in Tableau dashboards:

- Multiple visual sheets combined into one dashboard.
- A legend panel for interpretation.
- Dashboard-level KPIs.
- Chart sections focused on specific analytical questions.
- Clean field names and calculated fields from `data/Heart_tableau_ready.csv`.

## Files

- Template: `app/templates/dashboard/tableau_style.html`
- Styling: `app/static/css/datavibe.css`
- Route: `app/routes/dashboard.py`
- Tableau-ready data: `data/Heart_tableau_ready.csv`
