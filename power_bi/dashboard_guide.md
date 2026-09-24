# Power BI Architecture & Dashboard Specification Guide
## Project: STRAVA Fitness Data Analytics
**Author:** Tanim Naha  
**Domain:** Wearable Health Technology & Human Performance Analytics  
**Surveillance Scope:** 33 Unique Participants, 940 Daily Records, 22,099 Hourly Records  
**Data Engine:** SQLite3 3NF Normalized Relational Schema (`data/processed/fitness.db`)

---

## 1. Executive Summary & BI Architecture

The **STRAVA Fitness Data Analytics** Power BI solution provides public health researchers, wearable technology product managers, and fitness coaches with high-impact, interactive business intelligence. Tracking biometric and physical performance telemetry across 33 participants over a 31-day longitudinal surveillance period (April–May 2016), the model normalizes fragmented activity, sleep, cardiovascular, and hourly diurnal metrics into a high-performance **Star Schema**.

### Core Business & Clinical Objectives:
1. **Physical Exertion & Mobility Benchmarking:** Evaluate daily step attainment against the international WHO/CDC 10,000-step benchmark (achieved on 32.2% of logged days).
2. **Cardiovascular & Caloric Dynamics:** Map the metabolic relationship between physical movement intensity and caloric burn ($r = +0.59$), identifying active vs. basal metabolic rates.
3. **Sleep Architecture & Restorative Recovery:** Quantify sleep sufficiency ($6.99\text{ hrs}$ mean sleep vs. $7.64\text{ hrs}$ in bed, $91.6\%$ sleep efficiency) and analyze the impact of daytime sedentary time on nighttime recovery.
4. **Hourly Diurnal Chronotypes:** Isolate peak behavioral surge windows (morning 8–10 AM and evening 5–7 PM) to guide timed engagement nudges and smart workout scheduling.

---

## 2. Connecting Power BI to the Data Warehouse

### Method A: Direct SQLite Connector via ODBC (Recommended for Live Relational Sync)
1. Launch **Power BI Desktop**.
2. Select **Get Data** $\rightarrow$ **More...** $\rightarrow$ **Database** $\rightarrow$ **ODBC**.
3. In the DSN dropdown, choose your configured SQLite ODBC driver (or supply the connection string):
   ```
   Driver={SQLite3 ODBC Driver};Database=/Users/tanimnaha/Desktop/STRAVA_Fitness_Data_Analytics/data/processed/fitness.db;
   ```
4. In the Navigator pane, select the required tables:
   - `master_fitness_data`
   - `hourly_activity`
5. Click **Transform Data** to load into Power Query or **Load** to import directly into the model.

### Method B: Cleaned Processed CSV Folder Connector
1. Select **Get Data** $\rightarrow$ **Folder** $\rightarrow$ Navigate to `STRAVA_Fitness_Data_Analytics/data/processed/`.
2. Load individual processed tables:
   - `master_fitness_data.csv`
   - `hourly_activity_clean.csv`
   - `participant_summary.csv`
   - `sleep_clean.csv`
   - `heartrate_daily_clean.csv`
   - `weight_clean.csv`

---

## 3. Data Model Architecture (Star Schema)

In Power BI **Model View**, establish the following **1-to-Many ($1 : *$) single-directional relationships**:

```
                       +-------------------------+
                       |        Dim_Date         |
                       +-------------------------+
                       | PK  DateKey             |
                       |     FullDate            |
                       |     DayOfWeek           |
                       |     IsWeekend           |
                       |     MonthName           |
                       +------------+------------+
                                    |
          +-------------------------+-------------------------+
          | (1:*)                                             | (1:*)
+---------v-----------------------+                 +---------v-----------------------+
|        Fact_DailyActivity       |                 |        Fact_HourlyActivity      |
+---------------------------------+                 +---------------------------------+
| PK  ActivityKey                 |                 | PK  HourlyKey                   |
| FK  ParticipantKey              |                 | FK  ParticipantKey              |
| FK  DateKey                     |                 | FK  DateKey                     |
|     TotalSteps                  |                 |     Hour (0-23)                 |
|     Calories                    |                 |     StepTotal                   |
|     TotalDistance               |                 |     Calories                    |
|     VeryActiveMinutes           |                 |     TotalIntensity              |
|     FairlyActiveMinutes         |                 |     AverageIntensity            |
|     LightlyActiveMinutes        |                 |     TimeOfDay                   |
|     SedentaryMinutes            |                 |     IntensityCategory           |
|     ActivityLevel               |                 +---------------------------------+
|     SleepHours                  |
|     SleepEfficiencyPct          |
|     AverageHeartRate            |
+-----------------^---------------+
                  |
                  | (*:1)
+-----------------+---------------+
|        Dim_Participant          |
+---------------------------------+
| PK  ParticipantKey              |
|     Id (Biometric Identifier)   |
|     ParticipantLabel            |
|     ActivityCohort              |
|     DaysLogged                  |
|     PrimarySedentaryTier        |
+---------------------------------+
```

---

## 4. Multi-Page Executive Dashboard Wireframes

### Page 1: Executive Fitness & Caloric Overview
- **Executive KPI Ribbon (Top):**
  - *Total Cumulative Steps:* `7.18 M`
  - *Average Daily Steps:* `7,638` (vs. 10,000 WHO Target)
  - *Average Caloric Burn:* `2,304 kcal`
  - *10k Step Goal Attainment:* `32.2%`
- **Visual 1 (Top Left, Dual-Axis Line/Area):** Longitudinal Steps vs. Caloric Burn trend across 31 surveillance days.
- **Visual 2 (Top Right, Column Chart):** Step Volume by Day of Week (identifying Saturday at 8,153 and Tuesday at 8,125 as peak movement days).
- **Visual 3 (Bottom Left, Donut Chart):** Activity Cohort Distribution (High Activity 86.4%, Sedentary 8.8%, Moderate 2.4%, Low 2.3%).
- **Visual 4 (Bottom Right, Stacked Bar):** Daily Active Minutes Composition (Very Active 21m, Fairly Active 14m, Lightly Active 193m, Sedentary 991m).

### Page 2: Cardiovascular & Intensity Analytics
- **Executive KPI Ribbon:**
  - *Mean Very Active Minutes:* `21.2 min`
  - *Mean Total Distance:* `5.49 km`
  - *Average Heart Rate:* `78.6 bpm`
  - *Peak Recorded HR:* `109.8 bpm`
- **Visual 1 (Scatter Plot):** Active Minutes vs. Calorie Burn with regression line ($R^2 = 0.59$).
- **Visual 2 (Bar Chart):** Heart Rate Distribution across Rest, Fat Burn, Cardio, and Peak zones.
- **Visual 3 (Data Table / Matrix):** Top Participant Leaderboard sorted by Average Steps, Calories, and Logged Days.

### Page 3: Sleep Architecture & Restorative Recovery
- **Executive KPI Ribbon:**
  - *Mean Sleep Duration:* `6.99 hrs` (419 mins)
  - *Sleep Efficiency Index:* `91.6%`
  - *Mean Time in Bed:* `7.64 hrs` (458 mins)
  - *Restorative Sleep Days:* `64.8%` ($\ge 7\text{ hrs}$)
- **Visual 1 (Scatter Plot):** Sleep Duration vs. Daytime Step Exertion.
- **Visual 2 (Donut Chart):** Sleep Sufficiency Breakdown (Optimal $\ge 7\text{h}$, Sub-optimal $<7\text{h}$).
- **Visual 3 (Grouped Bar):** Time Asleep vs. Time Awake in Bed by Day of Week.
- **Visual 4 (Card Matrix):** Participant Sleep Regularity & Sleep Debt Tracker.

### Page 4: Hourly Diurnal Chronotypes & Peak Surge Zones
- **Executive KPI Ribbon:**
  - *Peak Diurnal Movement Hour:* `6:00 PM` (599 avg steps)
  - *Peak Caloric Burn Hour:* `6:00 PM` (124 avg kcal)
  - *Secondary Morning Surge:* `8:00 AM – 10:00 AM`
  - *Sedentary Window:* `11:00 PM – 5:00 AM`
- **Visual 1 (Area / Spline Chart):** 24-Hour Diurnal Step Profile ($0\text{h} \rightarrow 23\text{h}$).
- **Visual 2 (Line Chart):** 24-Hour Diurnal Caloric Burn Curve.
- **Visual 3 (Heatmap / Matrix):** Hourly Intensity Categories across Morning, Afternoon, Evening, and Night.
- **Visual 4 (Table):** Hourly Activity Breakdown Table with conditional heat shading.

---

## 5. Strategic Recommendations & Public Health Policy Impact

1. **Break Up Prolonged Sedentary Blocks:** 991 minutes (16.5 hours) of daily sedentary time indicates a critical need for hourly haptic movement reminders during office hours (10 AM to 4 PM).
2. **Target Midweek Slumps:** Steps drop to weekly lows on Thursdays (7,406) and Sundays (6,933). Strava challenges should target midweek and Sunday group walks.
3. **Bridge the 10,000-Step Gap:** 67.8% of daily records fail to meet 10k steps. Introducing tiered micro-goals (7,500 $\rightarrow$ 10,000 $\rightarrow$ 12,500) prevents user burnout and improves adherence.
4. **Sleep Hygiene Interventions:** Participants spend an average of 39 minutes awake in bed prior to sleep onset. Bedtime wind-down notifications can optimize latency.
