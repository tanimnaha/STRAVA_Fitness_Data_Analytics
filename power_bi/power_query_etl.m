// ============================================================================
// STRAVA FITNESS DATA ANALYTICS: POWER QUERY (M) ETL TRANSFORMATION SCRIPT
// Environment: Microsoft Power BI Desktop
// Purpose: Load and normalize daily activity, sleep, heart rate, and hourly tables
// ============================================================================

let
    // 1. Source Database Connection (SQLite ODBC)
    Source = Odbc.DataSource("dsn=SQLite3 Datasource", [HierarchicalNavigation=true]),
    fitness_Database = Source{[Name="fitness.db",Kind="Database"]}[Data],
    
    // 2. Load Master Fitness Data
    master_fitness_data_Table = fitness_Database{[Name="master_fitness_data",Kind="Table"]}[Data],
    #"Changed Type Master" = Table.TransformColumnTypes(master_fitness_data_Table,{
        {"Id", Int64.Type},
        {"Date", type date},
        {"TotalSteps", Int64.Type},
        {"Calories", Int64.Type},
        {"TotalDistance", type number},
        {"VeryActiveMinutes", Int64.Type},
        {"FairlyActiveMinutes", Int64.Type},
        {"LightlyActiveMinutes", Int64.Type},
        {"SedentaryMinutes", Int64.Type},
        {"TotalActiveMinutes", Int64.Type},
        {"TotalActiveDistance", type number},
        {"DayOfWeek", type text},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"ActivityLevel", type text},
        {"SleepHours", type number},
        {"TimeInBedHours", type number},
        {"SleepEfficiencyPct", type number},
        {"SleepCategory", type text},
        {"AverageHeartRate", type number},
        {"MinimumHeartRate", type number},
        {"MaximumHeartRate", type number},
        {"WeightKg", type number},
        {"BMI", type number},
        {"IsWeekend", Int64.Type}
    }),

    // 3. Derived Dimension: Dim_Date
    DatesList = List.Dates(#date(2016, 4, 1), 60, #duration(1, 0, 0, 0)),
    #"Date Table" = Table.FromList(DatesList, Splitter.SplitByNothing(), {"FullDate"}, null, ExtraValues.Error),
    #"Typed Date Table" = Table.TransformColumnTypes(#"Date Table",{{"FullDate", type date}}),
    #"Added DateKey" = Table.AddColumn(#"Typed Date Table", "DateKey", each Date.ToText([FullDate], "yyyyMMdd"), type text),
    #"Added DayName" = Table.AddColumn(#"Added DateKey", "DayOfWeekName", each Date.DayOfWeekName([FullDate]), type text),
    #"Added DayNumber" = Table.AddColumn(#"Added DayName", "DayOfWeekNumber", each Date.DayOfWeek([FullDate], Day.Monday) + 1, Int64.Type),
    #"Added IsWeekend" = Table.AddColumn(#"Added DayNumber", "IsWeekend", each if [DayOfWeekNumber] >= 6 then 1 else 0, Int64.Type),
    #"Added MonthName" = Table.AddColumn(#"Added IsWeekend", "MonthName", each Date.MonthName([FullDate]), type text),

    // 4. Derived Dimension: Dim_Participant
    #"Distinct Participants" = Table.SelectColumns(#"Changed Type Master", {"Id"}),
    #"Removed Duplicates Participant" = Table.Distinct(#"Distinct Participants"),
    #"Added Participant Label" = Table.AddColumn(#"Removed Duplicates Participant", "ParticipantLabel", each "Participant " & Text.End(Text.From([Id]), 4), type text),
    
    // 5. Fact Table: Fact_HourlyActivity
    hourly_activity_Table = fitness_Database{[Name="hourly_activity",Kind="Table"]}[Data],
    #"Changed Type Hourly" = Table.TransformColumnTypes(hourly_activity_Table,{
        {"Id", Int64.Type},
        {"Date", type date},
        {"Hour", Int64.Type},
        {"Calories", Int64.Type},
        {"TotalIntensity", type number},
        {"AverageIntensity", type number},
        {"StepTotal", Int64.Type},
        {"DayOfWeek", type text},
        {"TimeOfDay", type text},
        {"IntensityCategory", type text}
    })
in
    #"Changed Type Master"
