import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "dailyActivity_merged(2).csv"
OUTPUT_FILE = PROCESSED_FOLDER / "daily_activity_clean.csv"


# --------------------------------------------------
# 2. Load the raw data
# --------------------------------------------------

print("=" * 70)
print("DAILY ACTIVITY DATA CLEANING")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")


# --------------------------------------------------
# 3. Standardize column names
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)


# --------------------------------------------------
# 4. Convert date column
# --------------------------------------------------

df["ActivityDate"] = pd.to_datetime(
    df["ActivityDate"],
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


# --------------------------------------------------
# 7. Remove exact duplicate rows
# --------------------------------------------------

if duplicates > 0:
    df = df.drop_duplicates()


# --------------------------------------------------
# 8. Check invalid values
# --------------------------------------------------

print("\nChecking invalid values...")

negative_steps = (df["TotalSteps"] < 0).sum()
negative_calories = (df["Calories"] < 0).sum()

print(f"Negative step records    : {negative_steps:,}")
print(f"Negative calorie records : {negative_calories:,}")


# --------------------------------------------------
# 9. Remove records with invalid dates
# --------------------------------------------------

invalid_dates = df["ActivityDate"].isna().sum()

print(f"Invalid dates             : {invalid_dates:,}")

if invalid_dates > 0:
    df = df.dropna(subset=["ActivityDate"])


# --------------------------------------------------
# 10. Create useful analytical columns
# --------------------------------------------------

df["DayOfWeek"] = df["ActivityDate"].dt.day_name()

df["Month"] = df["ActivityDate"].dt.month

df["MonthName"] = df["ActivityDate"].dt.month_name()

df["TotalActiveMinutes"] = (
    df["VeryActiveMinutes"]
    + df["FairlyActiveMinutes"]
    + df["LightlyActiveMinutes"]
)

df["TotalActiveDistance"] = (
    df["VeryActiveDistance"]
    + df["ModeratelyActiveDistance"]
    + df["LightActiveDistance"]
)


# --------------------------------------------------
# 11. Create activity-level category
# --------------------------------------------------

def classify_activity(minutes):
    if minutes == 0:
        return "Sedentary"

    elif minutes < 30:
        return "Low Activity"

    elif minutes < 60:
        return "Moderate Activity"

    else:
        return "High Activity"


df["ActivityLevel"] = df["TotalActiveMinutes"].apply(
    classify_activity
)


# --------------------------------------------------
# 12. Sort the data
# --------------------------------------------------

df = df.sort_values(
    ["Id", "ActivityDate"]
).reset_index(drop=True)


# --------------------------------------------------
# 13. Save cleaned data
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 14. Final report
# --------------------------------------------------

print("\n" + "=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print(f"Final rows       : {len(df):,}")
print(f"Final columns    : {len(df.columns)}")
print(f"Output file      : {OUTPUT_FILE}")

print("\nNew analytical columns:")
print(" - DayOfWeek")
print(" - Month")
print(" - MonthName")
print(" - TotalActiveMinutes")
print(" - TotalActiveDistance")
print(" - ActivityLevel")

print("\nFirst 5 cleaned records:")
print(df.head().to_string(index=False))

print("\n" + "=" * 70)