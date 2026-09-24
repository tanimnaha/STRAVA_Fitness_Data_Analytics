import pandas as pd
from pathlib import Path

# ============================================================
# STRAVA FITNESS DATA ANALYTICS
# BUILD MASTER DATASET
# ============================================================

PROCESSED = Path("data/processed")

print("=" * 70)
print("BUILDING MASTER ANALYTICAL DATASET")
print("=" * 70)


# ------------------------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------------------------

print("\n1. Loading cleaned datasets...")

daily = pd.read_csv(PROCESSED / "daily_activity_clean.csv")
sleep = pd.read_csv(PROCESSED / "sleep_clean.csv")
heart = pd.read_csv(PROCESSED / "heartrate_daily_clean.csv")
weight = pd.read_csv(PROCESSED / "weight_clean.csv")
hourly = pd.read_csv(PROCESSED / "hourly_activity_clean.csv")

print(f"Daily activity : {len(daily):,} rows")
print(f"Sleep          : {len(sleep):,} rows")
print(f"Heart rate     : {len(heart):,} rows")
print(f"Weight         : {len(weight):,} rows")
print(f"Hourly         : {len(hourly):,} rows")


# ------------------------------------------------------------
# 2. CONVERT DATES
# ------------------------------------------------------------

print("\n2. Converting dates...")

daily["Date"] = pd.to_datetime(daily["ActivityDate"], errors="coerce")

sleep["Date"] = pd.to_datetime(sleep["SleepDay"], errors="coerce")

heart["Date"] = pd.to_datetime(heart["Date"], errors="coerce")

weight["Date"] = pd.to_datetime(weight["Date"], errors="coerce")

hourly["Date"] = pd.to_datetime(hourly["Date"], errors="coerce")


# ------------------------------------------------------------
# 3. PREPARE DAILY DATA
# ------------------------------------------------------------

print("\n3. Preparing daily activity data...")

# Remove duplicate daily records
daily = daily.drop_duplicates(subset=["Id", "Date"])

# Keep only useful columns
daily_columns = [
    "Id",
    "Date",
    "TotalSteps",
    "Calories",
    "TotalDistance",
    "TrackerDistance",
    "LoggedActivitiesDistance",
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
    "SedentaryMinutes",
    "VeryActiveDistance",
    "ModeratelyActiveDistance",
    "LightActiveDistance",
    "SedentaryActiveDistance",
    "DayOfWeek",
    "Month",
    "MonthName",
    "TotalActiveMinutes",
    "TotalActiveDistance",
    "ActivityLevel"
]

daily_columns = [c for c in daily_columns if c in daily.columns]

master = daily[daily_columns].copy()


# ------------------------------------------------------------
# 4. PREPARE SLEEP DATA
# ------------------------------------------------------------

print("\n4. Preparing sleep data...")

sleep_columns = [
    "Id",
    "Date",
    "TotalSleepRecords",
    "TotalMinutesAsleep",
    "TotalTimeInBed",
    "SleepHours",
    "TimeInBedHours",
    "SleepEfficiencyPct",
    "SleepCategory"
]

sleep_columns = [c for c in sleep_columns if c in sleep.columns]

sleep_clean = sleep[sleep_columns].copy()

# One sleep record per user/date
sleep_clean = (
    sleep_clean
    .sort_values(["Id", "Date"])
    .drop_duplicates(subset=["Id", "Date"], keep="last")
)


# ------------------------------------------------------------
# 5. PREPARE HEART-RATE DATA
# ------------------------------------------------------------

print("\n5. Preparing heart-rate data...")

heart_columns = [
    "Id",
    "Date",
    "AverageHeartRate",
    "MinimumHeartRate",
    "MaximumHeartRate",
    "HeartRateReadings"
]

heart_columns = [c for c in heart_columns if c in heart.columns]

heart_clean = heart[heart_columns].copy()

heart_clean = (
    heart_clean
    .drop_duplicates(subset=["Id", "Date"])
)


# ------------------------------------------------------------
# 6. PREPARE WEIGHT DATA
# ------------------------------------------------------------

print("\n6. Preparing weight data...")

weight_columns = [
    "Id",
    "Date",
    "WeightKg",
    "BMI",
    "Fat"
]

weight_columns = [c for c in weight_columns if c in weight.columns]

weight_clean = weight[weight_columns].copy()

# Weight can have multiple records for the same day.
# Keep the latest record.
weight_clean = (
    weight_clean
    .sort_values(["Id", "Date"])
    .drop_duplicates(subset=["Id", "Date"], keep="last")
)


# ------------------------------------------------------------
# 7. AGGREGATE HOURLY ACTIVITY INTO DAILY ACTIVITY
# ------------------------------------------------------------

print("\n7. Aggregating hourly activity into daily metrics...")

hourly_daily = (
    hourly
    .groupby(["Id", "Date"], as_index=False)
    .agg(
        HourlyCalories=("Calories", "sum"),
        HourlySteps=("StepTotal", "sum"),
        HourlyIntensity=("TotalIntensity", "sum"),
        AverageHourlyIntensity=("AverageIntensity", "mean")
    )
)

print(f"Hourly daily summary : {len(hourly_daily):,} rows")


# ------------------------------------------------------------
# 8. MERGE EVERYTHING
# ------------------------------------------------------------

print("\n8. Merging datasets...")

master = master.merge(
    sleep_clean,
    on=["Id", "Date"],
    how="left"
)

master = master.merge(
    heart_clean,
    on=["Id", "Date"],
    how="left"
)

master = master.merge(
    weight_clean,
    on=["Id", "Date"],
    how="left"
)

master = master.merge(
    hourly_daily,
    on=["Id", "Date"],
    how="left"
)


# ------------------------------------------------------------
# 9. CREATE ADDITIONAL ANALYTICAL FEATURES
# ------------------------------------------------------------

print("\n9. Creating analytical features...")

# Steps per active minute
master["StepsPerActiveMinute"] = (
    master["TotalSteps"] /
    master["TotalActiveMinutes"].replace(0, pd.NA)
)

# Calories per 1,000 steps
master["CaloriesPer1000Steps"] = (
    master["Calories"] /
    (master["TotalSteps"] / 1000).replace(0, pd.NA)
)

# Active minute percentage
master["ActiveMinutePct"] = (
    master["TotalActiveMinutes"] /
    1440 * 100
)

# Sleep sufficiency
if "SleepHours" in master.columns:
    master["SleepSufficient"] = master["SleepHours"] >= 7

# Weekend flag
if "DayOfWeek" in master.columns:
    master["IsWeekend"] = master["DayOfWeek"].isin(
        ["Saturday", "Sunday"]
    )


# ------------------------------------------------------------
# 10. SORT DATA
# ------------------------------------------------------------

master = master.sort_values(
    ["Id", "Date"]
).reset_index(drop=True)


# ------------------------------------------------------------
# 11. REMOVE EXACT DUPLICATES
# ------------------------------------------------------------

master = master.drop_duplicates()


# ------------------------------------------------------------
# 12. SAVE MASTER DATASET
# ------------------------------------------------------------

output_file = PROCESSED / "master_fitness_data.csv"

master.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 13. CREATE PARTICIPANT SUMMARY
# ------------------------------------------------------------

print("\n10. Creating participant summary...")

participant_summary = (
    master
    .groupby("Id", as_index=False)
    .agg(
        DaysRecorded=("Date", "nunique"),
        AverageSteps=("TotalSteps", "mean"),
        AverageCalories=("Calories", "mean"),
        AverageActiveMinutes=("TotalActiveMinutes", "mean"),
        AverageSedentaryMinutes=("SedentaryMinutes", "mean"),
        AverageSleepHours=("SleepHours", "mean"),
        AverageHeartRate=("AverageHeartRate", "mean")
    )
)

participant_summary = participant_summary.sort_values(
    "AverageSteps",
    ascending=False
)

participant_summary.to_csv(
    PROCESSED / "participant_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 14. FINAL REPORT
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MASTER DATASET CREATED SUCCESSFULLY")
print("=" * 70)

print(f"\nMaster rows    : {len(master):,}")
print(f"Master columns : {len(master.columns):,}")

print("\nMaster columns:")
print(list(master.columns))

print("\nMissing values:")
print(
    master.isnull()
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print("\nOutput files:")
print(f" - {output_file}")
print(" - data/processed/participant_summary.csv")

print("\nFirst 5 records:")
print(
    master.head()
    .to_string(index=False)
)

print("\n" + "=" * 70)
print("BUILD COMPLETE")
print("=" * 70)