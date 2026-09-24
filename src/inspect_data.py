import pandas as pd
from pathlib import Path

# Location of our raw datasets
RAW_FOLDER = Path("data/raw")

print("=" * 80)
print("STRAVA FITNESS DATA - RAW DATA INSPECTION")
print("=" * 80)

# Find all CSV and Excel files
files = sorted(
    list(RAW_FOLDER.glob("*.csv")) +
    list(RAW_FOLDER.glob("*.xlsx"))
)

print(f"\nTotal files found: {len(files)}\n")

for file in files:
    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    try:
        # Read the file
        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Basic information
        print(f"Rows       : {df.shape[0]:,}")
        print(f"Columns    : {df.shape[1]}")
        print(f"Duplicates : {df.duplicated().sum():,}")

        print("\nColumns:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nMissing values:")
        missing = df.isnull().sum()

        missing_found = False

        for column, count in missing.items():
            if count > 0:
                print(f"  - {column}: {count:,}")
                missing_found = True

        if not missing_found:
            print("  None")

        print("\nData types:")
        print(df.dtypes.to_string())

        print("\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))

    except Exception as e:
        print(f"ERROR reading {file.name}:")
        print(e)

print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)