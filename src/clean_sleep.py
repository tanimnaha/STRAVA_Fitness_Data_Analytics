import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "sleepDay_merged(2).csv"
OUTPUT_FILE = PROCESSED_FOLDER / "sleep_clean.csv"


# --------------------------------------------------
# 2. Load raw sleep data
# --------------------------------------------------

print("=" * 70)
print("SLEEP DATA CLEANING")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")

print("\nOriginal columns:")
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
# 4. Convert date
# --------------------------------------------------

df["SleepDay"] = pd.to_datetime(
    df["SleepDay"],
    errors="coerce"
)


# --------------------------------------------------
# 5. Check missing values
# --------------------------------------------------

print("\nMissing values before cleaning:")

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

print("\nChecking invalid values...")

invalid_total_sleep = (
    df["TotalMinutesAsleep"] < 0
).sum()

invalid_time_in_bed = (
    df["TotalTimeInBed"] < 0
).sum()

print(
    f"Negative TotalMinutesAsleep : "
    f"{invalid_total_sleep:,}"
)

print(
    f"Negative TotalTimeInBed     : "
    f"{invalid_time_in_bed:,}"
)


# --------------------------------------------------
# 8. Remove invalid dates
# --------------------------------------------------

invalid_dates = df["SleepDay"].isna().sum()

print(f"Invalid dates               : {invalid_dates:,}")

if invalid_dates > 0:
    df = df.dropna(subset=["SleepDay"])


# --------------------------------------------------
# 9. Create useful analytical columns
# --------------------------------------------------

# Convert minutes to hours

df["SleepHours"] = (
    df["TotalMinutesAsleep"] / 60
).round(2)

df["TimeInBedHours"] = (
    df["TotalTimeInBed"] / 60
).round(2)


# Sleep efficiency:
# percentage of time in bed actually spent asleep

df["SleepEfficiencyPct"] = (
    df["TotalMinutesAsleep"]
    / df["TotalTimeInBed"]
    * 100
).round(2)


# Day of week

df["DayOfWeek"] = (
    df["SleepDay"]
    .dt.day_name()
)


# Month

df["Month"] = (
    df["SleepDay"]
    .dt.month
)


df["MonthName"] = (
    df["SleepDay"]
    .dt.month_name()
)


# --------------------------------------------------
# 10. Create sleep category
# --------------------------------------------------

def classify_sleep(hours):

    if hours < 5:
        return "Very Short Sleep"

    elif hours < 7:
        return "Short Sleep"

    elif hours <= 9:
        return "Recommended Range"

    else:
        return "Long Sleep"


df["SleepCategory"] = (
    df["SleepHours"]
    .apply(classify_sleep)
)


# --------------------------------------------------
# 11. Sort data
# --------------------------------------------------

df = df.sort_values(
    ["Id", "SleepDay"]
).reset_index(drop=True)


# --------------------------------------------------
# 12. Save cleaned data
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 13. Final report
# --------------------------------------------------

print("\n" + "=" * 70)
print("SLEEP CLEANING COMPLETE")
print("=" * 70)

print(f"Final rows       : {len(df):,}")
print(f"Final columns    : {len(df.columns)}")

print(f"Output file      : {OUTPUT_FILE}")

print("\nNew analytical columns:")

print(" - SleepHours")
print(" - TimeInBedHours")
print(" - SleepEfficiencyPct")
print(" - DayOfWeek")
print(" - Month")
print(" - MonthName")
print(" - SleepCategory")


print("\nFirst 5 cleaned records:")

print(
    df.head()
    .to_string(index=False)
)

print("\n" + "=" * 70)