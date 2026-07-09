# Performance Testing Report

## Description
Performance testing involves assessing the volume of data rendered from the database, the impact of data filters on system responsiveness, and the complexity introduced by the number of visualizations. Optimizing these factors ensures the dashboard operates efficiently, providing timely and reliable insights.

---

## 1. Amount of Data to DB

### Description
Monitor the volume of data being pulled and rendered from the database to ensure queries are optimized and not overloading the system. The amount of data that is rendered to a database depends on the size of the dataset and the capacity of the database to store and retrieve data.

### Database Table Metrics
Using MySQL Workbench to analyze the imported dataset (`data.heart_new2`), we gathered the following table storage and structure details:

| Metric | Value |
| :--- | :--- |
| **Database Schema** | `data` |
| **Table Name** | `heart_new2` |
| **Database Engine** | `InnoDB` |
| **Row Format** | `Dynamic` |
| **Column Count** | `18` |
| **Table Rows** | `4,416` |
| **Average Row Length** | `122 bytes` |
| **Data Length** | `528.0 KiB` |
| **Index Length** | `0.0 bytes` |
| **Table Size (estimate)** | `528.0 KiB` |
| **Create Time** | `2023-06-05 15:19:42` |

### Query & Storage Analysis
- **Low Memory Footprint**: With a total estimated size of **528.0 KiB**, the entire dataset easily fits in memory (RAM). This ensures extremely fast read/write operations (sub-millisecond execution times).
- **Column Count Efficiency**: Having 18 columns allows for a comprehensive set of features (demographics, lifestyle, comorbidities) without creating overly wide rows, keeping the average row length at a compact 122 bytes.

---

## 2. Impact of Data Filters on System Responsiveness

### Analysis
Data filtering on fields such as `AgeCategory`, `Sex`, `Smoking`, and `AlcoholDrinking` allows users to dynamically segment patient risks.
- **Current Performance**: Since the active dataset is small (~4,400 rows), filtering queries (e.g., `WHERE Sex = 'Male' AND HeartDisease = 'Yes'`) run in under `1ms` on standard SQL engines (SQLite and MySQL).
- **Scalability Strategy**: If the dataset scales to millions of records, standard linear scans (O(N) complexity) will degrade responsiveness. To maintain sub-second response times, we recommend implementing **B-Tree indexes** on frequently filtered columns:
  ```sql
  CREATE INDEX idx_heart_demographics ON heart_new2 (Sex, AgeCategory);
  CREATE INDEX idx_heart_disease ON heart_new2 (HeartDisease);
  ```

---

## 3. Complexity Introduced by the Number of Visualizations

### Analysis
The DataVibe dashboard renders multiple key charts in a single view:
1. KPI metrics (Total records, cases, rate, BMI).
2. Gender vs Heart Disease stacked columns.
3. Diabetic vs Stroke bubble grid.
4. Race-wise Heart Disease list.
5. Smoking/Alcohol impact horizontal bars.
6. Heart Disease Rate by Age category trend.

### Optimization Best Practices
To ensure that rendering 6+ visual charts simultaneously does not introduce rendering lag:
- **Aggregated Queries**: Rather than pulling raw records and aggregating in the frontend or Flask layer, we utilize pre-aggregated SQL views. This minimizes network payload size.
- **Client-Side Rendering**: Using standard CSS layouts and HTML layouts for charts ensures that load time is governed entirely by standard lightweight browser engines instead of heavy JavaScript visualization packages.
- **Caching**: For dashboard overview endpoints, query results can be cached (e.g., in-memory or via Redis) for brief periods to avoid hitting the database on every page reload.
