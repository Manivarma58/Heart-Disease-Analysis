# Utilization of Data Filters Report

## Description
Utilization of data filters refers to the effective implementation and management of filtering mechanisms within the Project to refine and focus the dataset. Proper use of filters enhances performance by limiting the volume of data processed and displayed, thereby improving responsiveness. It also enables users to interactively explore specific segments of data, leading to more targeted and meaningful insights.

---

## 1. Tableau Filter Case Studies

Based on the interactive Tableau workbooks, the platform implements specific, high-value filters to focus analytics on critical patient cohorts:

### Case Study A: Stroke & Diabetes Cohort analysis
- **Visualization Title**: *People Got Stroke Suffering from Diabetes and Heart Disease*
- **Columns**: `Heart Disease`, `Diabetic`, `Age Category`
- **Rows**: `AVG(BMI)`
- **Active Filter**: `Stroke: Yes`
- **Analytical Value**: By filtering the visualization to show only patients with `Stroke: Yes`, we can observe the distributions of age categories, diabetic categories, and heart disease status specifically for stroke sufferers. 
- **Performance Impact**: Restricts the database scan and rendering process strictly to the subset of stroke patients, which dramatically reduces the rendering and processing overhead.

### Case Study B: General Health & Heart Disease Correlation
- **Visualization Title**: *General Health vs Heart Disease*
- **Visual Encoding**: Bubble Chart (Circle Marks)
- **Active Filter**: `Heart Disease: Yes`
- **Data Points Shown**: 
  - **Good**: 172 cases
  - **Fair**: 140 cases
  - **Poor**: 92 cases
  - **Very Good**: 67 cases
- **Analytical Value**: Isolating the data where `Heart Disease: Yes` allows clinicians to study the self-reported health perceptions of heart disease patients. It shows that the majority of heart disease patients self-report their health as "Good" or "Fair", rather than "Very Good".
- **Performance Impact**: Excludes the large population of healthy patients (`Heart Disease: No`), passing a much smaller, aggregated result set to the charting rendering engine.

---

## 2. Backend Server-Side Filter Implementation

In the CardioViz Flask codebase, filters are utilized at the database query level to optimize network payload and backend speed. For example, in the patient search and dashboard routes, filters are applied dynamically in SQL:

```python
# In app/routes/dashboard.py (or patient search routes)
query = "SELECT * FROM patients WHERE 1=1"
params = []

if age_category:
    query += " AND age_category = ?"
    params.append(age_category)
if diabetic_status:
    query += " AND diabetic = ?"
    params.append(diabetic_status)
if stroke:
    query += " AND stroke = ?"
    params.append(stroke)
```

By applying filters at the query layer via `WHERE` clauses, the database engine returns only the filtered records. This minimizes database I/O, server memory usage, and JSON serialization costs.

---

## 3. Best Practices for Filter Optimization

To ensure optimal responsiveness, the following best practices are implemented across our database and dashboard integrations:

1. **Database-Level Aggregation**: In both the local SQLite database and target MySQL views, data is grouped and aggregated (e.g., `COUNT`, `AVG`) at the database level before rendering.
2. **Indexed Columns**: Columns used for filtering (such as `Stroke`, `HeartDisease`, and `Diabetic`) are indexed in production schemas to allow rapid O(log N) searches.
3. **Tableau Extracts**: For published Tableau dashboards, filters utilize data extracts with pre-computed aggregations, preventing expensive runtime calculations on the live database.
