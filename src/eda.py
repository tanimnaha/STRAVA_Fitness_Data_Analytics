import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# STRAVA FITNESS DATA ANALYTICS
# Python EDA using Matplotlib and Seaborn
# ============================================================

print("=" * 70)
print("STARTING PYTHON EDA")
print("=" * 70)

# ------------------------------------------------------------
# 1. LOAD MASTER DATA
# ------------------------------------------------------------

file_path = "data/processed/master_fitness_data.csv"

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. BASIC INFORMATION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BASIC DATA INFORMATION")
print("=" * 70)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nDataset description:")
print(df.describe().round(2))


# ------------------------------------------------------------
# 3. CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

output_dir = "outputs/charts"

os.makedirs(output_dir, exist_ok=True)


# ------------------------------------------------------------
# 4. DAILY STEPS DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.histplot(
    df["TotalSteps"].dropna(),
    bins=30,
    kde=True
)

plt.title("Distribution of Daily Steps")
plt.xlabel("Total Steps")
plt.ylabel("Number of Days")
plt.tight_layout()

plt.savefig(
    f"{output_dir}/01_daily_steps_distribution.png",
    dpi=300
)

plt.close()

print("Created: 01_daily_steps_distribution.png")


# ------------------------------------------------------------
# 5. STEPS VS CALORIES
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="TotalSteps",
    y="Calories",
    hue="ActivityLevel"
)

plt.title("Daily Steps vs Calories Burned")
plt.xlabel("Total Steps")
plt.ylabel("Calories Burned")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/02_steps_vs_calories.png",
    dpi=300
)

plt.close()

print("Created: 02_steps_vs_calories.png")


# ------------------------------------------------------------
# 6. ACTIVITY LEVEL DISTRIBUTION
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="ActivityLevel"
)

plt.title("Distribution of Activity Levels")
plt.xlabel("Activity Level")
plt.ylabel("Number of Days")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/03_activity_level_distribution.png",
    dpi=300
)

plt.close()

print("Created: 03_activity_level_distribution.png")


# ------------------------------------------------------------
# 7. STEPS BY DAY OF WEEK
# ------------------------------------------------------------

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_data = (
    df.groupby("DayOfWeek")["TotalSteps"]
    .mean()
    .reindex(weekday_order)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=weekday_data.index,
    y=weekday_data.values
)

plt.title("Average Daily Steps by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Steps")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/04_steps_by_weekday.png",
    dpi=300
)

plt.close()

print("Created: 04_steps_by_weekday.png")


# ------------------------------------------------------------
# 8. ACTIVE MINUTES VS CALORIES
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="TotalActiveMinutes",
    y="Calories"
)

plt.title("Active Minutes vs Calories Burned")
plt.xlabel("Total Active Minutes")
plt.ylabel("Calories Burned")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/05_active_minutes_vs_calories.png",
    dpi=300
)

plt.close()

print("Created: 05_active_minutes_vs_calories.png")


# ------------------------------------------------------------
# 9. SLEEP VS DAILY STEPS
# ------------------------------------------------------------

if "SleepHours" in df.columns:

    sleep_df = df.dropna(
        subset=["SleepHours", "TotalSteps"]
    )

    if len(sleep_df) > 0:

        plt.figure(figsize=(10, 6))

        sns.scatterplot(
            data=sleep_df,
            x="SleepHours",
            y="TotalSteps"
        )

        plt.title("Sleep Duration vs Daily Steps")
        plt.xlabel("Sleep Hours")
        plt.ylabel("Total Steps")

        plt.tight_layout()

        plt.savefig(
            f"{output_dir}/06_sleep_vs_steps.png",
            dpi=300
        )

        plt.close()

        print("Created: 06_sleep_vs_steps.png")


# ------------------------------------------------------------
# 10. HEART RATE ANALYSIS
# ------------------------------------------------------------

if "AverageHeartRate" in df.columns:

    hr_df = df.dropna(
        subset=["AverageHeartRate"]
    )

    if len(hr_df) > 0:

        plt.figure(figsize=(10, 6))

        sns.histplot(
            hr_df["AverageHeartRate"],
            bins=30,
            kde=True
        )

        plt.title("Distribution of Average Heart Rate")
        plt.xlabel("Average Heart Rate (BPM)")
        plt.ylabel("Number of Days")

        plt.tight_layout()

        plt.savefig(
            f"{output_dir}/07_heart_rate_distribution.png",
            dpi=300
        )

        plt.close()

        print("Created: 07_heart_rate_distribution.png")


# ------------------------------------------------------------
# 11. CORRELATION HEATMAP
# ------------------------------------------------------------

numeric_columns = [
    "TotalSteps",
    "Calories",
    "TotalDistance",
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
    "SedentaryMinutes",
    "TotalActiveMinutes",
    "SleepHours",
    "AverageHeartRate",
    "WeightKg",
    "BMI"
]

available_columns = [
    col for col in numeric_columns
    if col in df.columns
]

correlation_data = df[available_columns].corr()

plt.figure(figsize=(12, 9))

sns.heatmap(
    correlation_data,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Heatmap of Fitness Metrics")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/08_correlation_heatmap.png",
    dpi=300
)

plt.close()

print("Created: 08_correlation_heatmap.png")


# ------------------------------------------------------------
# 12. TOP 10 MOST ACTIVE DAYS
# ------------------------------------------------------------

top_days = (
    df.sort_values(
        "TotalSteps",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_days,
    x="TotalSteps",
    y="Date"
)

plt.title("Top 10 Most Active Days")
plt.xlabel("Total Steps")
plt.ylabel("Date")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/09_top_10_active_days.png",
    dpi=300
)

plt.close()

print("Created: 09_top_10_active_days.png")


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PYTHON EDA COMPLETE")
print("=" * 70)

print("\nCharts saved in:")
print("outputs/charts/")

print("\nTotal charts generated:")
print(len(os.listdir(output_dir)))

print("\nEDA completed successfully!")