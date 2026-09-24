import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_FOLDER / "weightLogInfo_merged(2).csv"
OUTPUT_FILE = PROCESSED_FOLDER / "weight_clean.csv"


# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

print("=" * 70)
print("WEIGHT DATA CLEANING")
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

df["Date"] = pd.to_datetime(
    df["Date"],
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
# 6. Check duplicate rows
# --------------------------------------------------

duplicates = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicates:,}")

if duplicates > 0:
    df = df.drop_duplicates()


# --------------------------------------------------
# 7. Check invalid values
# --------------------------------------------------

print("\nChecking invalid values...")

negative_weight_kg = (
    df["WeightKg"] < 0
).sum()

negative_weight_lb = (
    df["WeightPounds"] < 0
).sum()

negative_bmi = (
    df["BMI"] < 0
).sum()

print(
    f"Negative WeightKg     : "
    f"{negative_weight_kg:,}"
)

print(
    f"Negative WeightPounds : "
    f"{negative_weight_lb:,}"
)

print(
    f"Negative BMI          : "
    f"{negative_bmi:,}"
)


# --------------------------------------------------
# 8. Remove invalid dates
# --------------------------------------------------

invalid_dates = df["Date"].isna().sum()

print(f"Invalid dates         : {invalid_dates:,}")

if invalid_dates > 0:
    df = df.dropna(subset=["Date"])


# --------------------------------------------------
# 9. Create analytical columns
# --------------------------------------------------

df["DayOfWeek"] = (
    df["Date"].dt.day_name()
)

df["Month"] = (
    df["Date"].dt.month
)

df["MonthName"] = (
    df["Date"].dt.month_name()
)


# --------------------------------------------------
# 10. Sort data
# --------------------------------------------------

df = df.sort_values(
    ["Id", "Date"]
).reset_index(drop=True)


# --------------------------------------------------
# 11. Save cleaned data
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 12. Final report
# --------------------------------------------------

print("\n" + "=" * 70)
print("WEIGHT CLEANING COMPLETE")
print("=" * 70)

print(f"Final rows       : {len(df):,}")
print(f"Final columns    : {len(df.columns)}")

print(f"Output file      : {OUTPUT_FILE}")

print("\nNew analytical columns:")

print(" - DayOfWeek")
print(" - Month")
print(" - MonthName")


print("\nFirst 5 cleaned records:")

print(
    df.head()
    .to_string(index=False)
)

print("\n" + "=" * 70)