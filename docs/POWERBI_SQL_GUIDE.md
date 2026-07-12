# Power BI & SQL Database Integration Guide

This guide details how to integrate Power BI with CardioViz's SQLite/PostgreSQL database structures, configure live dashboards, and leverage the built-in SQL Console.

---

## 1. Connecting Power BI to the SQLite Database

To connect Power BI Desktop to the local SQLite database (`datavibe.db`), follow these steps:

### Step 1: Install the SQLite ODBC Driver
1. Download the SQLite ODBC Driver from [Ch. Werner's SQLite ODBC Driver site](http://www.ch-werner.de/sqliteodbc/).
2. Select the driver version matching your operating system architecture (usually `sqliteodbc_w64.exe` for 64-bit Windows).
3. Run the installer and complete the setup.

### Step 2: Configure a System Data Source Name (DSN)
1. Open the **ODBC Data Source Administrator** (search for "ODBC Data Sources (64-bit)" in the Windows Start Menu).
2. Go to the **System DSN** tab and click **Add...**
3. Select **SQLite3 ODBC Driver** and click **Finish**.
4. Configure the following fields:
   * **Data Source Name (DSN)**: `datavibe_sqlite`
   * **Database Name**: Click *Browse* and navigate to the absolute path of `datavibe.db` inside your repository directory (e.g. `D:\projects\skillwallet\Heart-Disease-Analysis\datavibe.db`).
5. Click **OK** to save the source.

### Step 3: Connect from Power BI Desktop
1. Open Power BI Desktop.
2. Click **Get Data** -> **More...** -> search for **ODBC**.
3. Choose **ODBC** and click **Connect**.
4. In the Data Source Name dropdown, select `datavibe_sqlite` and click **OK**.
5. When prompted for credentials, select **Windows** or **Default / Anonymous** (SQLite has no username/password by default) and click **Connect**.
6. The Navigator window will display the tables: `patients`, `clinical_measurements`, `lifestyle_factors`, `medical_history`, and `risk_assessments`. Select the tables and click **Load**.

---

## 2. Environment Configurations

To embed live Power BI reports/dashboards in CardioViz, publish your workbook to the Power BI Service, grab the embed URL (e.g., File -> Embed report -> Website or portal), and add it to your local environment file (`.env`):

```bash
POWERBI_CLINICAL_URL="https://app.powerbi.com/reportEmbed?reportId=your-report-id&groupId=your-group-id"
POWERBI_PUBLIC_HEALTH_URL="https://app.powerbi.com/reportEmbed?reportId=your-report-id&groupId=your-group-id"
POWERBI_PATIENT_URL="https://app.powerbi.com/reportEmbed?reportId=your-report-id&groupId=your-group-id"
POWERBI_DASHBOARD_URL="https://app.powerbi.com/reportEmbed?reportId=your-report-id&groupId=your-group-id"
```

*Note: If no URL is provided, the platform automatically renders a responsive mock Power BI report with interactive tabs, filtering capabilities, and data exports.*

---

## 3. SQL Query Console & Examples

The built-in **SQL Console** allows admins and clinicians to directly inspect patient records using read-only SQL statements.

### Example A: Patient Cardiovascular Risk Scoring List
Identify patients with high cardiovascular risk categorized by region and income:
```sql
SELECT p.first_name, p.last_name, p.region, p.income_range, r.risk_category, r.framingham_score
FROM patients p
JOIN risk_assessments r ON p.patient_id = r.patient_id
WHERE r.risk_category = 'High'
ORDER BY r.framingham_score DESC;
```

### Example B: Blood Pressure Averages vs. Smoking Cohorts
Examine how smoking status correlates with patient systolic/diastolic blood pressure:
```sql
SELECT l.smoking_status,
       ROUND(AVG(c.systolic_bp), 1) AS avg_systolic,
       ROUND(AVG(c.diastolic_bp), 1) AS avg_diastolic,
       COUNT(*) AS total_patients
FROM lifestyle_factors l
JOIN clinical_measurements c ON l.patient_id = c.patient_id
GROUP BY l.smoking_status;
```

### Example C: Sleep Duration & Stress Levels vs. Average BMI
```sql
SELECT l.stress_level,
       ROUND(AVG(l.sleep_hours), 1) AS avg_sleep,
       ROUND(AVG(c.bmi), 1) AS avg_bmi,
       COUNT(*) AS patients_count
FROM lifestyle_factors l
JOIN clinical_measurements c ON l.patient_id = c.patient_id
GROUP BY l.stress_level
ORDER BY avg_bmi DESC;
```
