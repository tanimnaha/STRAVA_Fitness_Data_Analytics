import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

CALORIES_FILE = RAW_FOLDER / "hourlyCalories_merged(2).csv"
INTENSITIES_FILE = RAW_FOLDER / "hourlyIntensities_merged(2).csv"
STEPS_FILE = RAW_FOLDER / "hourlySteps_merged(2).csv"

OUTPUT_FILE = PROCESSED_FOLDER / "hourly_activity_clean.csv"


# --------------------------------------------------
# 2. Load files
# --------------------------------------------------

print("=" * 70)
print("HOURLY ACTIVITY DATA CLEANING")
print("=" * 70)

print("\nLoading hourly calories...")
calories = pd.read_csv(CALORIES_FILE)

print(f"Calories rows: {len(calories):,}")

print("\nLoading hourly intensities...")
intensities = pd.read_csv(INTENSITIES_FILE)

print(f"Intensity rows: {len(intensities):,}")

print("\nLoading hourly steps...")
steps = pd.read_csv(STEPS_FILE)

print(f"Steps rows: {len(steps):,}")


# --------------------------------------------------
# 3. Standardize column names
# --------------------------------------------------

for df in [calories, intensities, steps]:

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )


# --------------------------------------------------
# 4. Display columns
# --------------------------------------------------

print("\nCalories columns:")
print(list(calories.columns))

print("\nIntensity columns:")
print(list(intensities.columns))

print("\nSteps columns:")
print(list(steps.columns))


# --------------------------------------------------
# 5. Convert ActivityHour
# --------------------------------------------------

calories["ActivityHour"] = pd.to_datetime(
    calories["ActivityHour"],
    errors="coerce"
)

intensities["ActivityHour"] = pd.to_datetime(
    intensities["ActivityHour"],
    errors="coerce"
)

steps["ActivityHour"] = pd.to_datetime(
    steps["ActivityHour"],
    errors="coerce"
)


# --------------------------------------------------
# 6. Check duplicates
# --------------------------------------------------

print("\nDuplicate rows:")

print(
    f"Calories    : {calories.duplicated().sum():,}"
)

print(
    f"Intensities : {intensities.duplicated().sum():,}"
)

print(
    f"Steps       : {steps.duplicated().sum():,}"
)


# Remove exact duplicates

calories = calories.drop_duplicates()
intensities = intensities.drop_duplicates()
steps = steps.drop_duplicates()


# --------------------------------------------------
# 7. Merge datasets
# --------------------------------------------------

print("\nMerging hourly datasets...")

hourly = calories.merge(
    intensities,
    on=["Id", "ActivityHour"],
    how="outer"
)

hourly = hourly.merge(
    steps,
    on=["Id", "ActivityHour"],
    how="outer"
)


# --------------------------------------------------
# 8. Check missing values
# --------------------------------------------------

print("\nMissing values after merging:")

missing = hourly.isnull().sum()

missing = missing[missing > 0]

if len(missing) == 0:
    print("None")
else:
    print(missing)


# --------------------------------------------------
# 9. Fill activity measures
# --------------------------------------------------

numeric_columns = [
    "Calories",
    "TotalIntensity",
    "AverageIntensity",
    "StepTotal"
]

for column in numeric_columns:

    if column in hourly.columns:

        hourly[column] = (
            hourly[column]
            .fillna(0)
        )


# --------------------------------------------------
# 10. Remove invalid dates
# --------------------------------------------------

invalid_dates = hourly["ActivityHour"].isna().sum()

print(
    f"\nInvalid ActivityHour values: "
    f"{invalid_dates:,}"
)

hourly = hourly[
    hourly["ActivityHour"].notna()
].copy()


# --------------------------------------------------
# 11. Check invalid activity values
# --------------------------------------------------

print("\nChecking invalid values...")

for column in numeric_columns:

    if column in hourly.columns:

        invalid = (
            hourly[column] < 0
        ).sum()

        print(
            f"{column}: {invalid:,} negative records"
        )


# --------------------------------------------------
# 12. Remove negative values
# --------------------------------------------------

for column in numeric_columns:

    if column in hourly.columns:

        hourly = hourly[
            hourly[column] >= 0
        ]


# --------------------------------------------------
# 13. Create analytical columns
# --------------------------------------------------

hourly["Date"] = (
    hourly["ActivityHour"]
    .dt.date
)

hourly["Date"] = pd.to_datetime(
    hourly["Date"]
)

hourly["Hour"] = (
    hourly["ActivityHour"]
    .dt.hour
)

hourly["DayOfWeek"] = (
    hourly["ActivityHour"]
    .dt.day_name()
)

hourly["Month"] = (
    hourly["ActivityHour"]
    .dt.month
)

hourly["MonthName"] = (
    hourly["ActivityHour"]
    .dt.month_name()
)


# --------------------------------------------------
# 14. Create time-of-day category
# --------------------------------------------------

def classify_time(hour):

    if 5 <= hour < 12:
        return "Morning"

    elif 12 <= hour < 17:
        return "Afternoon"

    elif 17 <= hour < 21:
        return "Evening"

    else:
        return "Night"


hourly["TimeOfDay"] = (
    hourly["Hour"]
    .apply(classify_time)
)


# --------------------------------------------------
# 15. Create activity intensity category
# --------------------------------------------------

def classify_intensity(value):

    if value == 0:
        return "Sedentary"

    elif value <= 2:
        return "Light"

    elif value <= 5:
        return "Moderate"

    else:
        return "High"


hourly["IntensityCategory"] = (
    hourly["AverageIntensity"]
    .apply(classify_intensity)
)


# --------------------------------------------------
# 16. Sort
# --------------------------------------------------

hourly = hourly.sort_values(
    ["Id", "ActivityHour"]
).reset_index(drop=True)


# --------------------------------------------------
# 17. Save
# --------------------------------------------------

hourly.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 18. Final report
# --------------------------------------------------

print("\n" + "=" * 70)
print("HOURLY ACTIVITY CLEANING COMPLETE")
print("=" * 70)

print(
    f"Final rows       : {len(hourly):,}"
)

print(
    f"Final columns    : {len(hourly.columns)}"
)

print(
    f"Output file      : {OUTPUT_FILE}"
)

print("\nFinal columns:")

print(
    list(hourly.columns)
)

print("\nFirst 5 cleaned records:")

print(
    hourly.head()
    .to_string(index=False)
)

print("\n" + "=" * 70)

# --------------------------------------------------
# 19. Save hourly data to SQLite database
# --------------------------------------------------

import sqlite3

DB_FILE = PROCESSED_FOLDER / "fitness.db"

print("\nSaving hourly data to SQLite database...")

conn = sqlite3.connect(DB_FILE)

hourly.to_sql(
    "hourly_activity",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("SQLite table created: hourly_activity")
print(f"Database: {DB_FILE}")