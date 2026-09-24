import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "heartrate_seconds_merged(2).csv"
OUTPUT_FILE = PROCESSED_FOLDER / "heartrate_daily_clean.csv"


# --------------------------------------------------
# 2. Load heart-rate data
# --------------------------------------------------

print("=" * 70)
print("HEART RATE DATA CLEANING")
print("=" * 70)

print("\nLoading heart-rate data...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")

print("\nColumns:")
print(list(df.columns))


# --------------------------------------------------
# 3. Standardize column names
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)


# --------------------------------------------------
# 4. Convert Time
# --------------------------------------------------

df["Time"] = pd.to_datetime(
    df["Time"],
    errors="coerce"
)


# --------------------------------------------------
# 5. Check missing values
# --------------------------------------------------

print("\nMissing values:")

missing = df.isnull().sum()
missing = missing[missing > 0]

if len(missing) == 0:
    print("None")
else:
    print(missing)


# --------------------------------------------------
# 6. Check duplicates
# --------------------------------------------------

duplicates = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicates:,}")

if duplicates > 0:
    df = df.drop_duplicates()


# --------------------------------------------------
# 7. Check invalid values
# --------------------------------------------------

print("\nChecking invalid heart-rate values...")

invalid_hr = (
    (df["Value"] <= 0)
).sum()

print(f"Invalid heart-rate records: {invalid_hr:,}")


# --------------------------------------------------
# 8. Remove invalid records
# --------------------------------------------------

df = df[
    (df["Value"] > 0) &
    (df["Time"].notna())
].copy()


# --------------------------------------------------
# 9. Create Date
# --------------------------------------------------

df["Date"] = df["Time"].dt.date


# --------------------------------------------------
# 10. Aggregate to daily level
# --------------------------------------------------

print("\nCreating daily heart-rate summary...")

daily_hr = (
    df.groupby(["Id", "Date"])["Value"]
    .agg(
        AverageHeartRate="mean",
        MinimumHeartRate="min",
        MaximumHeartRate="max",
        HeartRateReadings="count"
    )
    .reset_index()
)


# --------------------------------------------------
# 11. Round values
# --------------------------------------------------

daily_hr["AverageHeartRate"] = (
    daily_hr["AverageHeartRate"]
    .round(2)
)


daily_hr["MinimumHeartRate"] = (
    daily_hr["MinimumHeartRate"]
    .round(2)
)


daily_hr["MaximumHeartRate"] = (
    daily_hr["MaximumHeartRate"]
    .round(2)
)


# --------------------------------------------------
# 12. Convert Date to datetime
# --------------------------------------------------

daily_hr["Date"] = pd.to_datetime(
    daily_hr["Date"]
)


# --------------------------------------------------
# 13. Add analytical columns
# --------------------------------------------------

daily_hr["DayOfWeek"] = (
    daily_hr["Date"]
    .dt.day_name()
)

daily_hr["Month"] = (
    daily_hr["Date"]
    .dt.month
)

daily_hr["MonthName"] = (
    daily_hr["Date"]
    .dt.month_name()
)


# --------------------------------------------------
# 14. Sort
# --------------------------------------------------

daily_hr = daily_hr.sort_values(
    ["Id", "Date"]
).reset_index(drop=True)


# --------------------------------------------------
# 15. Save
# --------------------------------------------------

daily_hr.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 16. Final report
# --------------------------------------------------

print("\n" + "=" * 70)
print("HEART RATE CLEANING COMPLETE")
print("=" * 70)

print(f"Original records : {len(df):,}")
print(f"Daily records    : {len(daily_hr):,}")

print(f"Output file      : {OUTPUT_FILE}")

print("\nFinal columns:")

print(
    list(daily_hr.columns)
)

print("\nFirst 5 records:")

print(
    daily_hr.head()
    .to_string(index=False)
)

print("\n" + "=" * 70)