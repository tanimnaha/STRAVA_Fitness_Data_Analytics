# ⚡ STRAVA Fitness Data Analytics
> **Enterprise Wearable Telemetry, Diurnal Chronotypes, Sleep Architecture & Interactive Power BI Intelligence Suite**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit 1.64](https://img.shields.io/badge/Streamlit-1.64-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Power BI DirectQuery](https://img.shields.io/badge/Power_BI-DirectQuery-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![SQLite 3](https://img.shields.io/badge/SQLite-Warehouse-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Plotly 7.1](https://img.shields.io/badge/Plotly-7.1-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![Chart.js 4.4](https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chartdotjs&logoColor=white)](https://chartjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 1. Project Overview

The **STRAVA Fitness Data Analytics** project delivers an enterprise-grade physiological and behavioral telemetry intelligence platform. Built on longitudinal biometric data spanning **33 participants, 940 daily records, and 22,099 high-frequency hourly observations** (April 12 – May 12, 2016), the system analyzes multidimensional relationships across:
* **Exertional Movement**: Steps, distance (km), intensity zones (Very Active, Fairly Active, Lightly Active, Sedentary).
* **Metabolic Burn**: Active and basal caloric expenditure (kcal), METs, and burn efficiency.
* **Sleep Architecture**: Total sleep hours, time in bed, sleep latency/restlessness gap, and physiological efficiency index.
* **Cardiovascular Diurnal Curves**: Resting heart rate, diurnal peaks, morning commute surges, and nocturnal basal troughs.

The platform provides dual complementary analytical interfaces:
1. **Interactive Streamlit Web App (`streamlit_app/app.py`)**: 9 comprehensive analytical pages with custom cyber-dark UX, interactive Plotly visualizations, SQL sandbox, and full cohort telemetry.
2. **Interactive Power BI Dashboard Suite (`power_bi/`)**: A production-grade Power BI dashboard replica with Star Schema semantic modeling, 25+ production DAX formulas, Power Query M ETL automation, and dynamic multi-tier slicers.

---

## 📊 2. Key Telemetry Findings & Benchmarks

| Metric Dimension | Cohort Mean / Value | Clinical / Product Benchmark | Insight & Strategic Relevance |
| :--- | :---: | :---: | :--- |
| **Total Steps Logged** | **7,179,828 steps** | — | Cumulative volume across 31-day monitoring campaign |
| **Daily Mean Steps** | **7,638 steps/day** | 10,000 steps (WHO / Tudor-Locke) | 76.4% of recommended target; high opportunity for gamification |
| **10k Goal Attainment** | **32.2% of days** | ≥ 50% target | Only ~1 in 3 days achieves recommended cardiovascular load |
| **Daily Caloric Burn** | **2,304 kcal/day** | 2,000–2,500 kcal baseline | Strong linear correlation with distance traversed (R² > 0.65) |
| **Sedentary Time** | **991 min/day (16.5 hrs)** | < 600 min/day | High non-active time; sedentary interruptions required |
| **Very Active Time** | **21.2 min/day** | ≥ 20 min/day (AHA) | Active cohort achieves vigorous cardio guidelines |
| **Daily Mean Distance** | **5.49 km/day** | 7.0–8.0 km target | Corresponds closely with step totals |
| **Mean Sleep Duration** | **6.99 hrs (419 min)** | 7.0–9.0 hrs (NSF) | Borderline optimal; 55.9% of nights meet recommended ≥7h |
| **Sleep Efficiency** | **91.6%** | ≥ 85% clinical threshold | High nocturnal sleep consolidation |
| **Bed Restlessness Gap** | **39.1 min/night** | < 30 min | Time awake in bed; target for wind-down sleep hygiene |
| **Peak Exertion Hour** | **6:00 PM (18:00)** | 599 steps/hr | Primary evening workout wave across participants |
| **Morning Surge Hour** | **9:00 AM (09:00)** | 446 steps/hr | Active commute wave; secondary campaign window |
| **Nocturnal Basal Burn** | **68.1 kcal/hr** | 03:00–04:00 AM | Basal metabolic rate trough during deep sleep |

---

## 🏗️ 3. System Architecture & Data Pipeline

```
[ Raw Multi-Table Data ]
   ├── dailyActivity_merged.csv
   ├── sleepDay_merged.csv
   ├── heartrate_seconds_merged.csv
   ├── hourlyActivity (Steps, Calories, Intensities)
   └── weightLogInfo_merged.csv
                │
                ▼
[ Python ETL Pipeline (src/) ]
   ├── clean_daily.py       (Deduplication, ISO dates, bounds checking)
   ├── clean_sleep.py       (Efficiency calculation, duration conversion)
   ├── clean_heartrate.py   (Second-level resampling to daily min/mean/max)
   ├── clean_hourly.py      (24-hour diurnal binning, time-of-day categories)
   └── build_master.py      (Unified star schema join & data warehouse build)
                │
                ▼
[ SQLite Data Warehouse (data/processed/fitness.db) ]
   ├── master_fitness_data  (940 rows, 44 analytical features)
   └── hourly_activity      (22,099 rows, 13 temporal features)
                │
        ┌───────┴────────────────────────┐
        ▼                                ▼
[ Streamlit Web Application ]    [ Power BI Enterprise Suite ]
   ├── 9 Interactive Pages          ├── Star Schema Semantic Model
   ├── SQL Sandbox Engine           ├── 25+ Production DAX Measures
   ├── Plotly Cyber Visualizations  ├── Power Query M Script
   └── Embedded Power BI Tab        └── 4-Page Reactive Dashboard (Chart.js)
```

---

## 🎛️ 4. Power BI Enterprise Dashboard Suite (`power_bi/`)

The Power BI suite is completely self-contained in `power_bi/` and features:

### 1. Multi-Dimensional Interactive Slicers
* **Step Tier**:
  * `All Step Tiers (940 Logs)`: Complete population baseline.
  * `Highly Active (≥10,000 steps)`: 303 logs, mean 13,337 steps, 2,744 kcal, 100% goal hit rate.
  * `Moderately Active (7,500–9,999 steps)`: 163 logs, mean 8,726 steps, 2,461 kcal.
  * `Lightly Active (5,000–7,499 steps)`: 171 logs, mean 6,264 steps, 2,254 kcal.
  * `Sedentary (<5,000 steps)`: 303 logs, mean 2,128 steps, 1,807 kcal.
* **Day Horizon**: `All Days`, `Weekdays Only (Mon–Fri)`, `Weekends Only (Sat–Sun)`.
* **Athlete Cohort**: `All 33 Athletes`, `Top 10 High-Volume Athletes`, `Consistent Trackers (>25 Logged Days)`.
* **Athlete ID**: Drilldown dropdown with master ranking (`#1` to `#33`) and individual volume metrics.
* **Active Filter Chips**: Dynamic tag chips with one-click dismiss (`✕`) and instant reset button.

### 2. 4 Navigable Dashboard Pages
1. **📊 1. Executive Summary & KPIs**:
   * Total steps logged (7.18M), daily mean steps (7,638), caloric burn (2,304 kcal), 10k goal rate (32.2%).
   * 31-day longitudinal step and calorie dual-axis trend.
   * Day of week movement profile (Mon–Sun) with target reference line.
   * Activity minutes breakdown doughnut chart.
   * Master athlete standings leaderboard table.
2. **🏃 2. Movement & Intensity Profiles**:
   * Mean distance (5.49 km), very active time (21.2 min), sedentary time (991 min), active/sedentary ratio (19.3%).
   * Active minutes stacked bar chart across intensity zones.
   * Distance vs caloric burn scatter correlation.
   * Multi-dimensional Weekday vs Weekend radar chart.
   * 10k step goal attainment % by Day of Week.
3. **😴 3. Sleep Architecture & Recovery**:
   * Mean sleep duration (6.99 hrs), sleep efficiency index (91.6%), restlessness bed gap (39.1 min), sufficient sleep rate (55.9%).
   * Sleep duration vs time in bed by Day of Week.
   * Sleep efficiency distribution doughnut (Optimal ≥90%, Fair 80–89%, Suboptimal <80%).
   * Sleep duration vs daytime step volume quadrant scatter plot.
   * Sleep duration health category breakdown (Optimal, Short, Deprived).
4. **⏰ 4. Diurnal Chronotype & Hourly Patterns**:
   * Peak exertion window (6:00 PM at 599 st/h), morning commute surge (9:00 AM at 446 st/h), nocturnal basal burn (68.1 kcal/h), 22,099 observations.
   * 24-hour diurnal step curve dynamically linked to step tier, day horizon, or individual athlete.
   * 24-hour caloric expenditure curve.
   * Granular 24-hour tabular chronotype matrix with period, steps, calories, intensity score, and chronotype zone.
   * Step volume distribution across day periods.

### 3. Star Schema Data Model & DAX Library
* **`power_bi/dashboard_guide.md`**: Full architecture guide, table schemas (`Dim_Date`, `Dim_Participant`, `Fact_DailyActivity`, `Fact_HourlyActivity`), relationship definitions (1-to-many, single direction), and wireframes.
* **`power_bi/dax_measures.dax`**: 25+ production DAX formulas including `Total Steps (M)`, `Step Goal Attainment %`, `Sleep Efficiency Pct`, `Strava Readiness Index`, and diurnal chronotype aggregators.
* **`power_bi/power_query_etl.m`**: Power Query M ETL script for data transformation, typecasting, and key generation.

---

## 💻 5. Streamlit Web Application (`streamlit_app/`)

The Streamlit web application (`streamlit_app/app.py`) provides 9 dedicated pages:

1. **Executive Overview**: High-level KPI grid, 31-day longitudinal trends, weekday performance, and top athlete rankings.
2. **Activity Analysis**: Deep dive into distance, active minutes, and sedentary behavior correlations.
3. **Sleep & Wellness**: Sleep duration, bed latency, efficiency distributions, and daytime activity relationships.
4. **Heart Rate**: Cardiovascular analysis, resting heart rate distributions, and exertion heart rate metrics.
5. **Hourly Patterns**: 24-hour diurnal chronotype analysis, commute spikes, and time-of-day behavioral breakdowns.
6. **SQL Analysis**: Direct SQLite querying interface with pre-built business queries and query execution engine.
7. **Python EDA**: In-depth exploratory data analysis with statistical distributions, box plots, heatmaps, and outlier checks.
8. **Business Insights**: Strategic business recommendations, wearable product opportunities, and behavioral nudges.
9. **Power BI Dashboard**: Embedded interactive Power BI dashboard replica with standalone fullscreen launcher.

---

## 📂 6. Repository Structure

```
STRAVA_Fitness_Data_Analytics/
├── .gitignore                      # Operating system, virtualenv, cache, and GitHub limits ignore
├── README.md                       # Comprehensive project documentation
├── requirements.txt                # Python package dependencies
├── app.py                          # Root deployment entrypoint for Streamlit Community Cloud
├── STRAVA_Fitness_Data_Analytics_Dashboard_Report_Tanim_Naha.docx # Executive project report (Word DOC format)
├── docs/
│   ├── STRAVA_Fitness_Data_Analytics_Dashboard_Report_Tanim_Naha.docx # Detailed project report
│   └── images/                     # 15 High-resolution dashboard snapshots (PBI & Streamlit)
├── data/
│   ├── raw/                        # Original raw wearable logs (daily, hourly, minute, sleep, weight)
│   └── processed/                  # Cleaned data warehouse
│       ├── fitness.db              # SQLite Database (master_fitness_data, hourly_activity)
│       ├── master_fitness_data.csv # Unified 940-record master analytical dataset
│       ├── daily_activity_clean.csv# Cleaned daily activity
│       ├── hourly_activity_clean.csv# Cleaned 22,099 hourly records
│       ├── sleep_clean.csv         # Cleaned sleep logs
│       └── participant_summary.csv # Athlete summary metrics
├── power_bi/
│   ├── interactive_dashboard.html  # Standalone interactive Power BI 4-page replica (Chart.js)
│   ├── index.html                  # Symlink entry point to interactive_dashboard.html
│   ├── dashboard_guide.md          # Star Schema modeling specs, DAX reference & wireframes
│   ├── dax_measures.dax            # 25+ Production DAX measure formulas
│   └── power_query_etl.m           # Power Query M ETL transformation script
├── sql/
│   └── analysis.sql                # Production SQL queries for business intelligence
├── src/
│   ├── clean_daily.py              # Cleaning daily activity records
│   ├── clean_sleep.py              # Cleaning and validating sleep architecture
│   ├── clean_heartrate.py          # Processing high-frequency heart rate data
│   ├── clean_hourly.py             # Binning hourly activity into 24h diurnal profiles
│   ├── clean_weight.py             # Processing weight and BMI metrics
│   ├── build_master.py             # Master ETL script assembling fitness.db
│   ├── eda.py                      # Exploratory data analysis scripts
│   └── verify_duplicates.py        # Integrity and duplicate verification
├── streamlit_app/
│   └── app.py                      # Main Streamlit web application (9 pages)
└── outputs/
    ├── charts/                     # Exported figures and charts
    └── data_inspection.txt         # Data schema and field inspection logs
```

---

## 🚀 7. Installation & Quickstart Guide

### Step 1: Clone Repository & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/STRAVA_Fitness_Data_Analytics.git
cd STRAVA_Fitness_Data_Analytics

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Streamlit Web Application
```bash
streamlit run streamlit_app/app.py --server.port 8508
```
* Access the app in your browser at: **`http://localhost:8508`**
* Navigate to **"Power BI Dashboard"** in the sidebar to interact with the embedded dashboard.

### Step 3: Run the Standalone Power BI Interactive Dashboard
```bash
python -m http.server 8507 --directory power_bi
```
* Access the standalone Power BI replica at: **`http://localhost:8507`**

---

## 📈 8. Strategic Product & Behavioral Recommendations

1. **Precision Notification Scheduling**:
   * **Morning Surge (8:15 – 8:45 AM)**: Deploy daily goal notifications and route recommendations right before the 9:00 AM commute peak.
   * **Evening Surge (5:15 – 5:45 PM)**: Trigger workout challenges, club group rides/runs, and goal-closing reminders ahead of the 6:00 PM peak exertion wave.
2. **Sedentary Interruption Engine**:
   * Cohort average sedentary duration is **16.5 hours/day (991 minutes)**. Implementing gentle 250-step hourly movement reminders during typical work hours (10:00 AM – 4:00 PM) can significantly reduce metabolic stagnation.
3. **Sleep Hygiene & Recovery Coaching**:
   * The average bed latency/restlessness gap is **39.1 minutes**. Introduce evening wind-down routines and recovery score notifications for athletes with >45 minutes of restless bed time.
4. **Micro-Goal Laddering for Sub-10k Athletes**:
   * With 67.8% of days failing to hit the 10,000-step mark, dynamic personalized goals (e.g., advancing a 5k athlete to 7k before targeting 10k) will increase retention and goal attainment satisfaction.

---

## 📜 9. License

This project is licensed under the **MIT License** — feel free to use and adapt this project for research, analytics, or enterprise reporting.
