-- ============================================================
-- STRAVA FITNESS DATA ANALYTICS
-- SQL ANALYSIS
-- ============================================================


-- 1. OVERALL KPI SUMMARY
-- ============================================================

SELECT
    COUNT(DISTINCT Id) AS TotalParticipants,
    COUNT(*) AS TotalDailyRecords,
    ROUND(AVG(TotalSteps), 2) AS AverageDailySteps,
    ROUND(AVG(Calories), 2) AS AverageDailyCalories,
    ROUND(AVG(TotalDistance), 2) AS AverageDailyDistance,
    ROUND(AVG(VeryActiveMinutes), 2) AS AvgVeryActiveMinutes,
    ROUND(AVG(FairlyActiveMinutes), 2) AS AvgFairlyActiveMinutes,
    ROUND(AVG(LightlyActiveMinutes), 2) AS AvgLightlyActiveMinutes,
    ROUND(AVG(SedentaryMinutes), 2) AS AvgSedentaryMinutes
FROM master_fitness_data;


-- 2. ACTIVITY LEVEL DISTRIBUTION
-- ============================================================

SELECT
    ActivityLevel,
    COUNT(*) AS NumberOfDays,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM master_fitness_data),
        2
    ) AS PercentageOfDays
FROM master_fitness_data
GROUP BY ActivityLevel
ORDER BY NumberOfDays DESC;


-- 3. AVERAGE STEPS BY WEEKDAY
-- ============================================================

SELECT
    DayOfWeek,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories,
    COUNT(*) AS NumberOfRecords
FROM master_fitness_data
GROUP BY DayOfWeek
ORDER BY AverageSteps DESC;


-- 4. MOST ACTIVE PARTICIPANTS
-- ============================================================

SELECT
    Id,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories,
    ROUND(AVG(TotalDistance), 2) AS AverageDistance,
    ROUND(AVG(VeryActiveMinutes), 2) AS AverageVeryActiveMinutes,
    ROUND(AVG(SedentaryMinutes), 2) AS AverageSedentaryMinutes
FROM master_fitness_data
GROUP BY Id
ORDER BY AverageSteps DESC
LIMIT 10;


-- 5. CALORIES VS STEPS
-- ============================================================

SELECT
    ActivityLevel,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories,
    ROUND(AVG(TotalDistance), 2) AS AverageDistance
FROM master_fitness_data
GROUP BY ActivityLevel
ORDER BY AverageSteps DESC;


-- 6. SLEEP ANALYSIS
-- ============================================================

SELECT
    SleepCategory,
    COUNT(*) AS NumberOfRecords,
    ROUND(AVG(SleepHours), 2) AS AverageSleepHours,
    ROUND(AVG(SleepEfficiencyPct), 2) AS AverageSleepEfficiency,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories
FROM master_fitness_data
WHERE SleepHours IS NOT NULL
GROUP BY SleepCategory
ORDER BY AverageSleepHours DESC;


-- 7. SLEEP VS ACTIVITY
-- ============================================================

SELECT
    CASE
        WHEN SleepHours < 6 THEN 'Less than 6 hours'
        WHEN SleepHours < 8 THEN '6–8 hours'
        ELSE '8+ hours'
    END AS SleepDurationGroup,
    COUNT(*) AS NumberOfRecords,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories,
    ROUND(AVG(VeryActiveMinutes), 2) AS AverageVeryActiveMinutes
FROM master_fitness_data
WHERE SleepHours IS NOT NULL
GROUP BY SleepDurationGroup
ORDER BY AverageSteps DESC;


-- 8. HEART RATE SUMMARY
-- ============================================================

SELECT
    ROUND(AVG(AverageHeartRate), 2) AS OverallAverageHeartRate,
    MIN(MinimumHeartRate) AS LowestRecordedHeartRate,
    MAX(MaximumHeartRate) AS HighestRecordedHeartRate,
    ROUND(AVG(MaximumHeartRate), 2) AS AverageMaximumHeartRate
FROM master_fitness_data
WHERE AverageHeartRate IS NOT NULL;


-- 9. HEART RATE BY ACTIVITY LEVEL
-- ============================================================

SELECT
    ActivityLevel,
    ROUND(AVG(AverageHeartRate), 2) AS AverageHeartRate,
    ROUND(AVG(MaximumHeartRate), 2) AS AverageMaximumHeartRate,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps
FROM master_fitness_data
WHERE AverageHeartRate IS NOT NULL
GROUP BY ActivityLevel
ORDER BY AverageHeartRate DESC;


-- 10. MONTHLY ACTIVITY TREND
-- ============================================================

SELECT
    Month,
    MonthName,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps,
    ROUND(AVG(Calories), 2) AS AverageCalories,
    ROUND(AVG(TotalDistance), 2) AS AverageDistance
FROM master_fitness_data
GROUP BY Month, MonthName
ORDER BY Month;


-- 11. SEDENTARY BEHAVIOUR
-- ============================================================

SELECT
    ActivityLevel,
    ROUND(AVG(SedentaryMinutes), 2) AS AverageSedentaryMinutes,
    ROUND(AVG(TotalSteps), 2) AS AverageSteps
FROM master_fitness_data
GROUP BY ActivityLevel
ORDER BY AverageSedentaryMinutes DESC;


-- 12. TOP 10 MOST ACTIVE DAYS
-- ============================================================

SELECT
    Id,
    Date,
    TotalSteps,
    Calories,
    TotalDistance,
    VeryActiveMinutes,
    ActivityLevel
FROM master_fitness_data
ORDER BY TotalSteps DESC
LIMIT 10;