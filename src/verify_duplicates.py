import pandas as pd
from pathlib import Path

RAW = Path("data/raw")

files = [
    RAW / "heartrate_seconds_merged(1)(2).xlsx",
    RAW / "heartrate_seconds_merged(2).csv",
    RAW / "heartrate_seconds_merged(3).xlsx"
]

print("=" * 70)
print("HEART-RATE DUPLICATE FILE VERIFICATION")
print("=" * 70)

dataframes = []

for file in files:
    print(f"\nReading: {file.name}")

    if file.suffix.lower() == ".csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df["Time"] = pd.to_datetime(df["Time"])

    # Sort so row order does not affect comparison
    df = df.sort_values(["Id", "Time"]).reset_index(drop=True)

    dataframes.append(df)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)

first = dataframes[0]

for i in range(1, len(dataframes)):
    same = first.equals(dataframes[i])

    print(
        f"\nFile 1 vs File {i + 1}: "
        f"{'IDENTICAL' if same else 'DIFFERENT'}"
    )

print("\nVerification complete.")