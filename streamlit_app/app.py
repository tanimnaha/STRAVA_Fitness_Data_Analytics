import sqlite3
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STRAVA FITNESS DATA ANALYTICS
# Premium Streamlit Dashboard
# ============================================================

st.set_page_config(
    page_title="STRAVA | Fitness Analytics",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 15%, rgba(0, 188, 255, 0.10), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(124, 58, 237, 0.13), transparent 30%),
            radial-gradient(circle at 60% 90%, rgba(236, 72, 153, 0.08), transparent 25%),
            #050914;
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: rgba(5, 9, 20, 0.78);
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #07111f 0%, #050914 100%);
        border-right: 1px solid rgba(80, 150, 255, 0.18);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }

    .brand {
        padding: 20px 8px 18px 8px;
        margin-bottom: 18px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #ffffff;
    }

    .brand-subtitle {
        margin-top: 6px;
        color: #8290a7;
        font-size: 12px;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    .side-label {
        color: #73819a;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 22px 0 8px 2px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 38px 42px;
        margin: 8px 0 30px 0;
        background:
            linear-gradient(135deg,
                rgba(9, 42, 70, 0.96),
                rgba(15, 25, 58, 0.96) 52%,
                rgba(42, 18, 72, 0.96));
        border: 1px solid rgba(65, 174, 255, 0.30);
        box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.30),
            inset 0 1px rgba(255,255,255,0.05);
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -100px;
        top: -130px;
        border-radius: 50%;
        background: rgba(44, 194, 255, 0.16);
        filter: blur(5px);
    }

    .hero-title {
        position: relative;
        font-size: 42px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -1.8px;
        color: white;
    }

    .gradient-text {
        background: linear-gradient(90deg, #55d6ff, #8b7cff, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        position: relative;
        max-width: 720px;
        margin-top: 14px;
        color: #aab7cb;
        font-size: 15px;
        line-height: 1.65;
    }

    .hero-pills {
        position: relative;
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 22px;
    }

    .hero-pill {
        padding: 8px 13px;
        border-radius: 999px;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.10);
        color: #dbeafe;
        font-size: 12px;
        font-weight: 600;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 30px 0 16px 0;
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
    }

    .section-title:before {
        content: "";
        width: 4px;
        height: 28px;
        border-radius: 5px;
        background: linear-gradient(180deg, #22d3ee, #8b5cf6);
        box-shadow: 0 0 18px rgba(34,211,238,0.35);
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 22px;
    }

    .kpi {
        position: relative;
        min-height: 142px;
        padding: 20px;
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(17, 31, 53, 0.96), rgba(9, 19, 35, 0.96));
        border: 1px solid rgba(120, 160, 220, 0.16);
        box-shadow:
            0 12px 32px rgba(0,0,0,0.18),
            inset 0 1px rgba(255,255,255,0.035);
        overflow: hidden;
    }

    .kpi:after {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #22d3ee, #8b5cf6, #ec4899);
    }

    .kpi-icon {
        font-size: 21px;
        margin-bottom: 10px;
    }

    .kpi-label {
        color: #8e9bb0;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .kpi-value {
        margin-top: 7px;
        color: white;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .kpi-small {
        margin-top: 5px;
        color: #65748b;
        font-size: 11px;
    }

    .insight-card {
        padding: 20px;
        border-radius: 18px;
        background: rgba(12, 24, 43, 0.72);
        border: 1px solid rgba(92, 130, 180, 0.16);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        min-height: 135px;
    }

    .insight-title {
        color: #8bdcff;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .insight-text {
        color: #b5c0d1;
        line-height: 1.6;
        font-size: 13px;
    }

    .info-banner {
        padding: 15px 18px;
        border-radius: 14px;
        background: linear-gradient(90deg, rgba(14, 165, 233, .09), rgba(139, 92, 246, .09));
        border: 1px solid rgba(96, 165, 250, .16);
        color: #aebbd0;
        font-size: 13px;
        line-height: 1.6;
        margin: 14px 0;
    }

    .footer {
        text-align: center;
        color: #526076;
        font-size: 11px;
        padding: 45px 0 20px 0;
    }

    @media (max-width: 1100px) {
        .kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = ROOT / "data" / "processed" / "fitness.db"


def html(content):
    """Render custom HTML without Markdown treating nested tags as code."""
    clean = "\n".join(line.strip() for line in content.splitlines()).strip()
    st.markdown(clean, unsafe_allow_html=True)


def money_number(value):
    if pd.isna(value):
        return "—"
    return f"{value:,.0f}"


def number(value, decimals=0):
    if pd.isna(value):
        return "—"
    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"


def first_existing(df, names):
    for name in names:
        if name in df.columns:
            return name
    return None


def safe_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def style_fig(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b7c2d3", family="Inter"),
        margin=dict(l=10, r=10, t=55, b=20),
        title=dict(
            font=dict(size=16, color="#f8fafc"),
            x=0.02,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#aab6c8"),
        ),
        hoverlabel=dict(
            bgcolor="#101a2c",
            font_color="white",
        ),
        xaxis=dict(
            gridcolor="rgba(148,163,184,0.10)",
            zerolinecolor="rgba(148,163,184,0.10)",
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,0.10)",
            zerolinecolor="rgba(148,163,184,0.10)",
        ),
    )
    return fig


# ============================================================
# LOAD DATABASE
# ============================================================

if not DB_FILE.exists():
    st.error(f"Database not found: {DB_FILE}")
    st.stop()

conn = sqlite3.connect(DB_FILE)

tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
    conn,
)["name"].tolist()


def load_table(name):
    if name not in tables:
        return pd.DataFrame()
    return pd.read_sql_query(f'SELECT * FROM "{name}"', conn)


master = load_table("master_fitness_data")
hourly = load_table("hourly_activity")


# Fallback if the hourly table has another name
if hourly.empty:
    possible_hourly = [
        t for t in tables
        if "hourly" in t.lower()
    ]
    if possible_hourly:
        hourly = load_table(possible_hourly[0])


conn.close()


# ============================================================
# PREPARE MASTER DATA
# ============================================================

if master.empty:
    st.error("master_fitness_data is empty or missing.")
    st.stop()

master = master.copy()

id_col = first_existing(master, ["Id", "ID", "ParticipantId", "ParticipantID"])
date_col = first_existing(master, ["Date", "ActivityDate"])

if id_col:
    master[id_col] = pd.to_numeric(master[id_col], errors="coerce")

if date_col:
    master[date_col] = pd.to_datetime(master[date_col], errors="coerce")

numeric_master = [
    "TotalSteps",
    "Calories",
    "TotalDistance",
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
    "SedentaryMinutes",
    "TotalActiveMinutes",
    "TotalActiveDistance",
    "SleepHours",
    "TimeInBedHours",
    "SleepEfficiencyPct",
    "AverageHeartRate",
    "MinimumHeartRate",
    "MaximumHeartRate",
    "WeightKg",
    "BMI",
    "HourlyCalories",
    "HourlySteps",
    "HourlyIntensity",
    "AverageHourlyIntensity",
    "StepsPerActiveMinute",
    "CaloriesPer1000Steps",
    "ActiveMinutePct",
]

master = safe_numeric(master, numeric_master)


# ============================================================
# PREPARE HOURLY DATA
# ============================================================

if not hourly.empty:
    hourly = hourly.copy()

    hourly_id = first_existing(
        hourly,
        ["Id", "ID", "ParticipantId", "ParticipantID"]
    )

    hourly_time = first_existing(
        hourly,
        ["ActivityHour", "DateTime", "Timestamp"]
    )

    if hourly_id:
        hourly[hourly_id] = pd.to_numeric(
            hourly[hourly_id],
            errors="coerce"
        )

    if hourly_time:
        hourly[hourly_time] = pd.to_datetime(
            hourly[hourly_time],
            errors="coerce"
        )
        hourly["_Hour"] = hourly[hourly_time].dt.hour
    elif "Hour" in hourly.columns:
        hourly["_Hour"] = pd.to_numeric(
            hourly["Hour"],
            errors="coerce"
        )
    else:
        hourly["_Hour"] = np.nan

    hourly = safe_numeric(
        hourly,
        ["Calories", "TotalIntensity", "AverageIntensity", "StepTotal"]
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    html(
        """
        <div class="brand">
            <div class="brand-title">🏃 STRAVA</div>
            <div class="brand-subtitle">Fitness Data Analytics</div>
        </div>
        """
    )

    st.markdown("---")

    st.markdown(
        '<div class="side-label">Navigation</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Activity Analysis",
            "Sleep & Wellness",
            "Heart Rate",
            "Hourly Patterns",
            "SQL Analysis",
            "Python EDA",
            "Business Insights",
            "Power BI Dashboard",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        '<div class="side-label">Filters</div>',
        unsafe_allow_html=True,
    )

    participants = (
        sorted(master[id_col].dropna().unique().tolist())
        if id_col
        else []
    )

    participant_labels = {
        p: f"Participant {i:02d}"
        for i, p in enumerate(participants, 1)
    }

    selected_ids = st.multiselect(
        "Participants",
        participants,
        default=participants,
        format_func=lambda x: participant_labels.get(x, str(x)),
    )

    filtered = master.copy()

    if id_col and selected_ids:
        filtered = filtered[
            filtered[id_col].isin(selected_ids)
        ].copy()

    if id_col and not selected_ids:
        filtered = filtered.iloc[0:0].copy()

    min_date = (
        filtered[date_col].min()
        if date_col and not filtered.empty
        else None
    )

    max_date = (
        filtered[date_col].max()
        if date_col and not filtered.empty
        else None
    )

    if min_date is not None and max_date is not None:
        date_range = st.date_input(
            "Date range",
            value=(min_date.date(), max_date.date()),
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range

            filtered = filtered[
                (filtered[date_col].dt.date >= start_date)
                & (filtered[date_col].dt.date <= end_date)
            ].copy()


# ============================================================
# HERO
# ============================================================

html(
    """
    <div class="hero">
        <div class="hero-title">
            🏃 STRAVA
            <span class="gradient-text">Fitness Analytics</span>
        </div>

        <div class="hero-subtitle">
            Interactive analysis of activity, calories, sleep,
            heart rate and smart-device usage patterns.
            Built with Python, SQL, SQLite and Streamlit.
        </div>

        <div class="hero-pills">
            <div class="hero-pill">📊 Data Driven Insights</div>
            <div class="hero-pill">🎯 Participant Analysis</div>
            <div class="hero-pill">❤️ Health & Wellness</div>
            <div class="hero-pill">⚡ Actionable Analytics</div>
        </div>
    </div>
    """
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    html('<div class="section-title">Executive Overview</div>')

    participants_count = (
        filtered[id_col].nunique()
        if id_col and not filtered.empty
        else 0
    )

    activity_days = len(filtered)

    avg_steps = (
        filtered["TotalSteps"].mean()
        if "TotalSteps" in filtered.columns
        else np.nan
    )

    avg_calories = (
        filtered["Calories"].mean()
        if "Calories" in filtered.columns
        else np.nan
    )

    avg_active = (
        filtered["TotalActiveMinutes"].mean()
        if "TotalActiveMinutes" in filtered.columns
        else np.nan
    )

    html(
        f"""
        <div class="kpi-grid">

            <div class="kpi">
                <div class="kpi-icon">👥</div>
                <div class="kpi-label">Participants</div>
                <div class="kpi-value">{number(participants_count)}</div>
                <div class="kpi-small">Unique participants</div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">📅</div>
                <div class="kpi-label">Activity Days</div>
                <div class="kpi-value">{number(activity_days)}</div>
                <div class="kpi-small">Recorded activity days</div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">👟</div>
                <div class="kpi-label">Avg Daily Steps</div>
                <div class="kpi-value">{number(avg_steps)}</div>
                <div class="kpi-small">Steps per day</div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">🔥</div>
                <div class="kpi-label">Avg Calories</div>
                <div class="kpi-value">{number(avg_calories)}</div>
                <div class="kpi-small">Calories per day</div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">⏱️</div>
                <div class="kpi-label">Active Minutes</div>
                <div class="kpi-value">{number(avg_active, 1)}</div>
                <div class="kpi-small">Minutes per day</div>
            </div>

        </div>
        """
    )

    if date_col and "TotalSteps" in filtered.columns:

        daily = (
            filtered
            .groupby(date_col, as_index=False)["TotalSteps"]
            .mean()
            .sort_values(date_col)
        )

        fig = px.line(
            daily,
            x=date_col,
            y="TotalSteps",
            markers=True,
            title="Average Daily Steps Trend",
        )

        fig.update_traces(
            line=dict(width=3, color="#38bdf8"),
            marker=dict(size=6),
        )

        st.plotly_chart(
            style_fig(fig, 410),
            use_container_width=True,
        )

    st.markdown("---")

    html('<div class="section-title">Performance Snapshot</div>')

    c1, c2, c3 = st.columns(3)

    with c1:
        if "TotalSteps" in filtered.columns:
            peak = filtered["TotalSteps"].max()
            html(
                f"""
                <div class="insight-card">
                    <div class="insight-title">👟 Peak Daily Steps</div>
                    <div class="insight-text">
                        The highest recorded daily step count in the
                        current filter is <b>{number(peak)}</b> steps.
                    </div>
                </div>
                """
            )

    with c2:
        if "SleepHours" in filtered.columns:
            sleep_avg = filtered["SleepHours"].mean()
            html(
                f"""
                <div class="insight-card">
                    <div class="insight-title">😴 Average Sleep</div>
                    <div class="insight-text">
                        Average recorded sleep is
                        <b>{number(sleep_avg, 2)} hours</b>.
                    </div>
                </div>
                """
            )

    with c3:
        if "AverageHeartRate" in filtered.columns:
            hr_avg = filtered["AverageHeartRate"].mean()
            html(
                f"""
                <div class="insight-card">
                    <div class="insight-title">❤️ Average Heart Rate</div>
                    <div class="insight-text">
                        Average recorded heart rate is
                        <b>{number(hr_avg, 1)} BPM</b>.
                    </div>
                </div>
                """
            )


# ============================================================
# ACTIVITY ANALYSIS
# ============================================================

elif page == "Activity Analysis":

    html('<div class="section-title">Activity Analysis</div>')

    c1, c2 = st.columns(2)

    with c1:
        if {"TotalSteps", "Calories"}.issubset(filtered.columns):
            fig = px.scatter(
                filtered,
                x="TotalSteps",
                y="Calories",
                hover_data=[id_col] if id_col else None,
                title="Steps vs Calories",
                opacity=0.65,
            )

            fig.update_traces(
                marker=dict(
                    size=9,
                    color="#38bdf8",
                    line=dict(width=0.5, color="#e0f2fe"),
                )
            )

            st.plotly_chart(
                style_fig(fig),
                use_container_width=True,
            )

    with c2:
        activity_cols = [
            c for c in [
                "VeryActiveMinutes",
                "FairlyActiveMinutes",
                "LightlyActiveMinutes",
                "SedentaryMinutes",
            ]
            if c in filtered.columns
        ]

        if activity_cols:
            values = [
                filtered[c].mean()
                for c in activity_cols
            ]

            activity_df = pd.DataFrame(
                {
                    "Activity Type": activity_cols,
                    "Minutes": values,
                }
            )

            fig = px.bar(
                activity_df,
                x="Activity Type",
                y="Minutes",
                title="Average Activity Minutes",
            )

            fig.update_traces(
                marker_color="#8b7cff"
            )

            st.plotly_chart(
                style_fig(fig),
                use_container_width=True,
            )

    if "ActivityLevel" in filtered.columns:
        level = (
            filtered["ActivityLevel"]
            .value_counts()
            .reset_index()
        )

        level.columns = ["ActivityLevel", "Days"]

        fig = px.bar(
            level,
            x="ActivityLevel",
            y="Days",
            title="Activity Level Distribution",
            text="Days",
        )

        fig.update_traces(
            marker_color="#22d3ee",
            textposition="outside",
        )

        st.plotly_chart(
            style_fig(fig),
            use_container_width=True,
        )


# ============================================================
# SLEEP & WELLNESS
# ============================================================

elif page == "Sleep & Wellness":

    html('<div class="section-title">Sleep & Wellness</div>')

    if "SleepHours" not in filtered.columns:
        st.warning("Sleep data is not available.")
    else:

        sleep = filtered[
            filtered["SleepHours"].notna()
        ].copy()

        k1, k2, k3 = st.columns(3)

        with k1:
            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">😴</div>
                    <div class="kpi-label">Avg Sleep</div>
                    <div class="kpi-value">
                        {number(sleep["SleepHours"].mean(), 2)} h
                    </div>
                    <div class="kpi-small">Recorded sleep</div>
                </div>
                """
            )

        with k2:
            if "SleepEfficiencyPct" in sleep.columns:
                efficiency = sleep["SleepEfficiencyPct"].mean()
            else:
                efficiency = np.nan

            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">💤</div>
                    <div class="kpi-label">Sleep Efficiency</div>
                    <div class="kpi-value">
                        {number(efficiency, 1)}%
                    </div>
                    <div class="kpi-small">Average efficiency</div>
                </div>
                """
            )

        with k3:
            if "SleepSufficient" in sleep.columns:
                sufficient = sleep["SleepSufficient"].mean() * 100
            else:
                sufficient = np.nan

            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">🌙</div>
                    <div class="kpi-label">Sleep Sufficient</div>
                    <div class="kpi-value">
                        {number(sufficient, 1)}%
                    </div>
                    <div class="kpi-small">Share of recorded days</div>
                </div>
                """
            )

        c1, c2 = st.columns(2)

        with c1:
            fig = px.histogram(
                sleep,
                x="SleepHours",
                nbins=15,
                title="Sleep Duration Distribution",
            )

            fig.update_traces(
                marker_color="#8b7cff"
            )

            st.plotly_chart(
                style_fig(fig),
                use_container_width=True,
            )

        with c2:
            if "TotalSteps" in sleep.columns:
                fig = px.scatter(
                    sleep,
                    x="SleepHours",
                    y="TotalSteps",
                    title="Sleep vs Daily Steps",
                    opacity=0.65,
                )

                fig.update_traces(
                    marker=dict(
                        size=9,
                        color="#ec4899",
                    )
                )

                st.plotly_chart(
                    style_fig(fig),
                    use_container_width=True,
                )


# ============================================================
# HEART RATE
# ============================================================

elif page == "Heart Rate":

    html('<div class="section-title">Heart Rate Analysis</div>')

    if "AverageHeartRate" not in filtered.columns:
        st.warning("Heart-rate data is not available.")
    else:

        hr = filtered[
            filtered["AverageHeartRate"].notna()
        ].copy()

        a, b, c = st.columns(3)

        with a:
            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">❤️</div>
                    <div class="kpi-label">Average HR</div>
                    <div class="kpi-value">
                        {number(hr["AverageHeartRate"].mean(), 1)}
                    </div>
                    <div class="kpi-small">BPM</div>
                </div>
                """
            )

        with b:
            if "MinimumHeartRate" in hr.columns:
                min_hr = hr["MinimumHeartRate"].min()
            else:
                min_hr = np.nan

            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">📉</div>
                    <div class="kpi-label">Minimum HR</div>
                    <div class="kpi-value">
                        {number(min_hr, 1)}
                    </div>
                    <div class="kpi-small">Recorded minimum</div>
                </div>
                """
            )

        with c:
            if "MaximumHeartRate" in hr.columns:
                max_hr = hr["MaximumHeartRate"].max()
            else:
                max_hr = np.nan

            html(
                f"""
                <div class="kpi">
                    <div class="kpi-icon">📈</div>
                    <div class="kpi-label">Maximum HR</div>
                    <div class="kpi-value">
                        {number(max_hr, 1)}
                    </div>
                    <div class="kpi-small">Recorded maximum</div>
                </div>
                """
            )

        if date_col:
            trend = (
                hr.groupby(date_col, as_index=False)
                ["AverageHeartRate"]
                .mean()
            )

            fig = px.line(
                trend,
                x=date_col,
                y="AverageHeartRate",
                markers=True,
                title="Average Heart Rate Trend",
            )

            fig.update_traces(
                line=dict(color="#fb7185", width=3)
            )

            st.plotly_chart(
                style_fig(fig),
                use_container_width=True,
            )

        if {"AverageHeartRate", "TotalSteps"}.issubset(hr.columns):
            fig = px.scatter(
                hr,
                x="TotalSteps",
                y="AverageHeartRate",
                title="Steps vs Average Heart Rate",
                opacity=0.65,
            )

            fig.update_traces(
                marker=dict(
                    color="#fb7185",
                    size=8,
                )
            )

            st.plotly_chart(
                style_fig(fig),
                use_container_width=True,
            )


# ============================================================
# HOURLY PATTERNS
# ============================================================

elif page == "Hourly Patterns":

    html('<div class="section-title">Hourly Activity Patterns</div>')

    if hourly.empty:
        st.warning("Hourly data is not available in the analytical database.")
    else:

        h = hourly.copy()

        h_id = first_existing(
            h,
            ["Id", "ID", "ParticipantId", "ParticipantID"]
        )

        h_steps = first_existing(
            h,
            ["StepTotal", "TotalSteps", "Steps"]
        )

        h_cal = first_existing(
            h,
            ["Calories", "TotalCalories"]
        )

        h_int = first_existing(
            h,
            ["TotalIntensity", "Intensity"]
        )

        if h_id and selected_ids:
            h = h[h[h_id].isin(selected_ids)].copy()

        agg_dict = {}

        if h_steps:
            h[h_steps] = pd.to_numeric(
                h[h_steps],
                errors="coerce"
            )
            agg_dict["AvgSteps"] = (
                h_steps,
                "mean"
            )

        if h_cal:
            h[h_cal] = pd.to_numeric(
                h[h_cal],
                errors="coerce"
            )
            agg_dict["AvgCalories"] = (
                h_cal,
                "mean"
            )

        if h_int:
            h[h_int] = pd.to_numeric(
                h[h_int],
                errors="coerce"
            )
            agg_dict["AvgIntensity"] = (
                h_int,
                "mean"
            )

        if not agg_dict:
            st.warning("No usable hourly metrics were found.")
        else:

            agg = (
                h.groupby("_Hour", as_index=False)
                .agg(**agg_dict)
                .sort_values("_Hour")
            )

            a, b = st.columns(2)

            if "AvgSteps" in agg:
                with a:
                    fig = px.line(
                        agg,
                        x="_Hour",
                        y="AvgSteps",
                        markers=True,
                        title="Average Steps by Hour",
                    )

                    fig.update_traces(
                        line=dict(
                            color="#38bdf8",
                            width=3,
                        )
                    )

                    st.plotly_chart(
                        style_fig(fig),
                        use_container_width=True,
                    )

            if "AvgIntensity" in agg:
                with b:
                    fig = px.line(
                        agg,
                        x="_Hour",
                        y="AvgIntensity",
                        markers=True,
                        title="Average Intensity by Hour",
                    )

                    fig.update_traces(
                        line=dict(
                            color="#a78bfa",
                            width=3,
                        )
                    )

                    st.plotly_chart(
                        style_fig(fig),
                        use_container_width=True,
                    )

            if "AvgCalories" in agg:
                fig = px.bar(
                    agg,
                    x="_Hour",
                    y="AvgCalories",
                    title="Average Calories by Hour",
                )

                fig.update_traces(
                    marker_color="#fb7185"
                )

                st.plotly_chart(
                    style_fig(fig),
                    use_container_width=True,
                )

            display_agg = agg.rename(
                columns={"_Hour": "Hour"}
            )

            st.dataframe(
                display_agg.round(2),
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# SQL ANALYSIS
# ============================================================

elif page == "SQL Analysis":

    html('<div class="section-title">SQL Analysis</div>')

    html(
        """
        <div class="info-banner">
            These analytical queries run directly against the SQLite
            database. The queries use the actual database schema,
            including <b>Id</b> rather than the non-existent
            <b>ParticipantId</b> column.
        </div>
        """
    )

    sql_queries = {
        "Overall KPI Summary": """
SELECT
    COUNT(DISTINCT Id) AS participants,
    COUNT(*) AS activity_days,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories,
    ROUND(AVG(TotalActiveMinutes), 1) AS avg_active_minutes
FROM master_fitness_data;
""",

        "Activity Level Distribution": """
SELECT
    ActivityLevel,
    COUNT(*) AS activity_days,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories
FROM master_fitness_data
GROUP BY ActivityLevel
ORDER BY activity_days DESC;
""",

        "Weekday Activity": """
SELECT
    DayOfWeek,
    COUNT(*) AS days,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories,
    ROUND(AVG(TotalActiveMinutes), 1) AS avg_active_minutes
FROM master_fitness_data
GROUP BY DayOfWeek
ORDER BY avg_steps DESC;
""",

        "Top Participants by Steps": """
SELECT
    Id,
    COUNT(*) AS recorded_days,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories,
    ROUND(AVG(TotalActiveMinutes), 1) AS avg_active_minutes
FROM master_fitness_data
GROUP BY Id
ORDER BY avg_steps DESC
LIMIT 10;
""",

        "Sleep and Activity": """
SELECT
    SleepCategory,
    COUNT(*) AS records,
    ROUND(AVG(SleepHours), 2) AS avg_sleep_hours,
    ROUND(AVG(TotalSteps), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories
FROM master_fitness_data
WHERE SleepHours IS NOT NULL
GROUP BY SleepCategory
ORDER BY avg_sleep_hours DESC;
""",

        "Heart Rate Summary": """
SELECT
    ROUND(AVG(AverageHeartRate), 1) AS avg_heart_rate,
    ROUND(MIN(MinimumHeartRate), 1) AS min_heart_rate,
    ROUND(MAX(MaximumHeartRate), 1) AS max_heart_rate,
    SUM(HeartRateReadings) AS total_readings
FROM master_fitness_data
WHERE AverageHeartRate IS NOT NULL;
""",

        "Hourly Activity Summary": """
SELECT
    Hour,
    ROUND(AVG(StepTotal), 0) AS avg_steps,
    ROUND(AVG(Calories), 0) AS avg_calories,
    ROUND(AVG(TotalIntensity), 2) AS avg_intensity
FROM hourly_activity
GROUP BY Hour
ORDER BY Hour;
""",
    }

    query_name = st.selectbox(
        "Select SQL analysis",
        list(sql_queries.keys()),
    )

    query = sql_queries[query_name]

    st.code(query, language="sql")

    if st.button("▶ Run SQL Query", use_container_width=False):

        try:
            conn = sqlite3.connect(DB_FILE)
            result = pd.read_sql_query(query, conn)
            conn.close()

            st.success("SQL query executed successfully.")
            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True,
            )

        except Exception as e:
            st.error(f"SQL error: {e}")


# ============================================================
# PYTHON EDA
# ============================================================

elif page == "Python EDA":

    html('<div class="section-title">Python Exploratory Data Analysis</div>')

    html(
        """
        <div class="info-banner">
            <b>Python EDA workspace</b> — distribution analysis,
            relationships, activity patterns, sleep behavior,
            intensity composition and participant variation.
            Charts are generated from the filtered analytical dataset.
        </div>
        """
    )

    eda = filtered.copy()

    # Numeric cleanup
    numeric_cols = [
        "TotalSteps", "Calories", "VeryActiveMinutes",
        "FairlyActiveMinutes", "LightlyActiveMinutes",
        "SedentaryMinutes", "TotalActiveMinutes",
        "TotalActiveDistance", "SleepHours",
        "AwakeInBedMinutes", "SleepEfficiencyPct",
        "AverageHeartRate", "MinimumHeartRate",
        "MaximumHeartRate", "HeartRateReadings",
    ]
    for col in numeric_cols:
        if col in eda.columns:
            eda[col] = pd.to_numeric(eda[col], errors="coerce")

    # ---------------- KPI STRIP ----------------
    def safe_mean(col):
        return eda[col].mean() if col in eda.columns else np.nan

    html(
        f"""
        <div class="kpi-grid">
            <div class="kpi">
                <div class="kpi-icon">📐</div>
                <div class="kpi-label">Avg Steps</div>
                <div class="kpi-value">{number(safe_mean('TotalSteps'))}</div>
                <div class="kpi-small">Daily average</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">🔥</div>
                <div class="kpi-label">Avg Calories</div>
                <div class="kpi-value">{number(safe_mean('Calories'))}</div>
                <div class="kpi-small">Calories per day</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">🏃</div>
                <div class="kpi-label">Active Minutes</div>
                <div class="kpi-value">{number(safe_mean('TotalActiveMinutes'), 1)}</div>
                <div class="kpi-small">Daily active time</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">😴</div>
                <div class="kpi-label">Sleep Hours</div>
                <div class="kpi-value">{number(safe_mean('SleepHours'), 2)}</div>
                <div class="kpi-small">Recorded sleep</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">❤️</div>
                <div class="kpi-label">Avg Heart Rate</div>
                <div class="kpi-value">{number(safe_mean('AverageHeartRate'), 1)}</div>
                <div class="kpi-small">BPM</div>
            </div>
        </div>
        """
    )

    # ---------------- ROW 1: DISTRIBUTIONS ----------------
    st.markdown("### 1. Distribution Analysis")
    c1, c2 = st.columns(2)

    if "TotalSteps" in eda.columns:
        with c1:
            fig = px.histogram(
                eda.dropna(subset=["TotalSteps"]),
                x="TotalSteps", nbins=30, marginal="box",
                title="Daily Steps Distribution",
            )
            fig.update_traces(marker_color="#38bdf8", opacity=0.88)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if "Calories" in eda.columns:
        with c2:
            fig = px.histogram(
                eda.dropna(subset=["Calories"]),
                x="Calories", nbins=30, marginal="box",
                title="Daily Calories Distribution",
            )
            fig.update_traces(marker_color="#fb7185", opacity=0.88)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 2: RELATIONSHIPS ----------------
    st.markdown("### 2. Relationship Analysis")
    c1, c2 = st.columns(2)

    if {"TotalSteps", "Calories"}.issubset(eda.columns):
        with c1:
            fig = px.scatter(
                eda.dropna(subset=["TotalSteps", "Calories"]),
                x="TotalSteps", y="Calories",
                size="TotalActiveMinutes" if "TotalActiveMinutes" in eda.columns else None,
                color="TotalActiveMinutes" if "TotalActiveMinutes" in eda.columns else None,
                hover_data=[c for c in ["Id", "ActivityDate"] if c in eda.columns],
                title="Steps vs Calories",
                opacity=0.72,
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if {"TotalActiveMinutes", "Calories"}.issubset(eda.columns):
        with c2:
            fig = px.scatter(
                eda.dropna(subset=["TotalActiveMinutes", "Calories"]),
                x="TotalActiveMinutes", y="Calories",
                title="Active Minutes vs Calories",
                opacity=0.72,
            )
            fig.update_traces(marker=dict(color="#a78bfa", size=8))
            st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 3: ACTIVITY COMPOSITION ----------------
    st.markdown("### 3. Activity Composition")
    activity_cols = [
        c for c in [
            "VeryActiveMinutes", "FairlyActiveMinutes",
            "LightlyActiveMinutes", "SedentaryMinutes"
        ] if c in eda.columns
    ]
    if activity_cols:
        activity_avg = pd.DataFrame({
            "Activity Type": [c.replace("Minutes", "").replace("Active", " Active ").strip() for c in activity_cols],
            "Average Minutes": [eda[c].mean() for c in activity_cols],
        })
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(
                activity_avg, x="Activity Type", y="Average Minutes",
                title="Average Minutes by Activity Type",
                text_auto=".1f",
            )
            fig.update_traces(marker_color="#22d3ee")
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c2:
            fig = px.pie(
                activity_avg, names="Activity Type", values="Average Minutes",
                hole=0.58, title="Activity Time Composition",
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 4: WEEKDAY + TIME TREND ----------------
    st.markdown("### 4. Time Pattern Analysis")
    c1, c2 = st.columns(2)

    if "DayOfWeek" in eda.columns and "TotalSteps" in eda.columns:
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = eda.groupby("DayOfWeek", as_index=False)["TotalSteps"].mean()
        weekday["DayOfWeek"] = pd.Categorical(weekday["DayOfWeek"], categories=weekday_order, ordered=True)
        weekday = weekday.sort_values("DayOfWeek")
        with c1:
            fig = px.bar(weekday, x="DayOfWeek", y="TotalSteps", title="Average Steps by Day of Week", text_auto=".0f")
            fig.update_traces(marker_color="#38bdf8")
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if date_col and "TotalSteps" in eda.columns:
        trend = eda.groupby(date_col, as_index=False).agg(
            AvgSteps=("TotalSteps", "mean"),
            AvgCalories=("Calories", "mean") if "Calories" in eda.columns else ("TotalSteps", "mean"),
        ).sort_values(date_col)
        with c2:
            fig = px.line(trend, x=date_col, y="AvgSteps", markers=True, title="Daily Steps Trend")
            fig.update_traces(line=dict(color="#a78bfa", width=3))
            st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 5: SLEEP ----------------
    st.markdown("### 5. Sleep & Wellness Analysis")
    c1, c2 = st.columns(2)

    if "SleepHours" in eda.columns:
        with c1:
            sleep_data = eda.dropna(subset=["SleepHours"])
            fig = px.histogram(sleep_data, x="SleepHours", nbins=20, marginal="box", title="Sleep Duration Distribution")
            fig.update_traces(marker_color="#8b5cf6")
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if {"SleepHours", "TotalSteps"}.issubset(eda.columns):
        with c2:
            fig = px.scatter(
                eda.dropna(subset=["SleepHours", "TotalSteps"]),
                x="SleepHours", y="TotalSteps",
                title="Sleep Hours vs Daily Steps", opacity=0.72,
            )
            fig.update_traces(marker=dict(color="#c084fc", size=8))
            st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 6: HEART RATE ----------------
    st.markdown("### 6. Heart Rate Analysis")
    hr_cols = [c for c in ["MinimumHeartRate", "AverageHeartRate", "MaximumHeartRate"] if c in eda.columns]
    if hr_cols:
        hr_long = eda[hr_cols].melt(var_name="Heart Rate Metric", value_name="BPM").dropna()
        hr_long["Heart Rate Metric"] = hr_long["Heart Rate Metric"].str.replace("HeartRate", " ", regex=False).str.replace("([a-z])([A-Z])", r"\1 \2", regex=True)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.box(hr_long, x="Heart Rate Metric", y="BPM", title="Heart Rate Distribution")
            fig.update_traces(marker_color="#f43f5e")
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with c2:
            if "AverageHeartRate" in eda.columns and date_col:
                hr_trend = eda.groupby(date_col, as_index=False)["AverageHeartRate"].mean().sort_values(date_col)
                fig = px.line(hr_trend, x=date_col, y="AverageHeartRate", markers=True, title="Average Heart Rate Trend")
                fig.update_traces(line=dict(color="#fb7185", width=3))
                st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- ROW 7: CORRELATION ----------------
    st.markdown("### 7. Correlation Analysis")
    corr_cols = [
        c for c in [
            "TotalSteps", "Calories", "TotalActiveMinutes",
            "VeryActiveMinutes", "FairlyActiveMinutes",
            "LightlyActiveMinutes", "SedentaryMinutes",
            "SleepHours", "AverageHeartRate"
        ] if c in eda.columns
    ]
    if len(corr_cols) >= 3:
        corr = eda[corr_cols].corr(numeric_only=True).round(2)
        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                zmin=-1, zmax=1,
                colorscale="Blues",
                text=corr.values,
                texttemplate="%{text}",
                hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>",
            )
        )
        fig.update_layout(title="Correlation Matrix", height=560)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    # ---------------- DATA SUMMARY ----------------
    st.markdown("### 8. Descriptive Statistics")
    desc_cols = [c for c in corr_cols if c in eda.columns]
    if desc_cols:
        desc = eda[desc_cols].describe().T.reset_index().rename(columns={"index": "Metric"})
        st.dataframe(desc.round(2), use_container_width=True, hide_index=True)

    html(
        """
        <div class="info-banner">
            <b>EDA coverage:</b> distributions • outliers • relationships •
            activity composition • weekday patterns • time trends • sleep •
            heart rate • correlation analysis • descriptive statistics.
        </div>
        """
    )


# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    html('<div class="section-title">Business Insights</div>')

    avg_steps = (
        filtered["TotalSteps"].mean()
        if "TotalSteps" in filtered.columns
        else np.nan
    )

    avg_calories = (
        filtered["Calories"].mean()
        if "Calories" in filtered.columns
        else np.nan
    )

    avg_sleep = (
        filtered["SleepHours"].mean()
        if "SleepHours" in filtered.columns
        else np.nan
    )

    avg_active = (
        filtered["TotalActiveMinutes"].mean()
        if "TotalActiveMinutes" in filtered.columns
        else np.nan
    )

    html(
        f"""
        <div class="info-banner">
            The current filtered dataset contains
            <b>{number(len(filtered))}</b> activity records.
            Average daily steps are approximately
            <b>{number(avg_steps)}</b>, average calories are
            <b>{number(avg_calories)}</b>, average active time is
            <b>{number(avg_active, 1)} minutes</b>, and average recorded
            sleep is <b>{number(avg_sleep, 2)} hours</b>.
        </div>
        """
    )

    c1, c2 = st.columns(2)

    with c1:
        html(
            """
            <div class="insight-card">
                <div class="insight-title">📊 Engagement Opportunity</div>
                <div class="insight-text">
                    Activity data can be used to identify periods of
                    higher and lower engagement and design targeted
                    reminders, challenges and progress tracking.
                </div>
            </div>
            """
        )

        st.write("")

        html(
            """
            <div class="insight-card">
                <div class="insight-title">🎯 Personalised Experience</div>
                <div class="insight-text">
                    Participant-level activity patterns can support
                    personalised goals, activity nudges and progress
                    dashboards instead of relying on one generic target.
                </div>
            </div>
            """
        )

    with c2:
        html(
            """
            <div class="insight-card">
                <div class="insight-title">😴 Wellness Tracking</div>
                <div class="insight-text">
                    Sleep and activity measurements can be combined
                    to provide a broader wellness view and encourage
                    users to monitor recovery alongside movement.
                </div>
            </div>
            """
        )

        st.write("")

        html(
            """
            <div class="insight-card">
                <div class="insight-title">⚡ Actionable Analytics</div>
                <div class="insight-text">
                    Hourly activity patterns can help identify useful
                    times for reminders, challenges and engagement
                    campaigns based on observed usage behavior.
                </div>
            </div>
            """
        )

    html(
        """
        <div class="section-title">Recommended Analytical Themes</div>

        <div class="hero-pills">
            <div class="hero-pill">👟 Step Tracking</div>
            <div class="hero-pill">🔥 Calorie Monitoring</div>
            <div class="hero-pill">😴 Sleep Tracking</div>
            <div class="hero-pill">❤️ Heart Rate</div>
            <div class="hero-pill">⏰ Time-of-Day Engagement</div>
            <div class="hero-pill">🎯 Personalised Goals</div>
        </div>
        """
    )

elif page == "Power BI Dashboard":
    html(
        """
        <div class="hero">
            <div class="hero-kicker">Interactive Power BI Enterprise Replica</div>
            <div class="hero-title">⚡ STRAVA Power BI Dashboard</div>
            <div class="hero-subtitle">
                Enterprise-grade Power BI dashboard replica with Star Schema architecture,
                25+ production DAX measures, dynamic multi-tier slicers, and real-time interactive telemetry.
            </div>
            <div class="hero-pills">
                <div class="hero-pill">⚡ DirectQuery Engine</div>
                <div class="hero-pill">⭐ Star Schema (4 Tables)</div>
                <div class="hero-pill">📊 4 Dynamic Report Pages</div>
                <div class="hero-pill">🎛️ Real-Time Reactive Slicers</div>
                <div class="hero-pill">🧮 25+ Production DAX Measures</div>
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns([1.5, 1.5, 3])
    with col1:
        st.link_button(
            "🚀 Open Fullscreen Standalone",
            "http://localhost:8507",
            use_container_width=True,
        )
    with col2:
        st.link_button(
            "📖 Power BI Guide & DAX",
            "file:///Users/tanimnaha/Desktop/STRAVA_Fitness_Data_Analytics/power_bi/dashboard_guide.md",
            use_container_width=True,
        )
    with col3:
        st.caption(
            "💡 Use the interactive slicers (Step Tier, Day Horizon, Athlete Cohort) inside the embedded dashboard below to filter all metrics, charts, and tables in real time."
        )

    st.write("")

    # Load and embed the interactive Power BI dashboard HTML
    pbi_path = Path(__file__).resolve().parent.parent / "power_bi" / "interactive_dashboard.html"
    if pbi_path.exists():
        with open(pbi_path, "r", encoding="utf-8") as f:
            pbi_content = f.read()
        components.html(pbi_content, height=1050, scrolling=True)
    else:
        st.error(f"Power BI dashboard file not found at {pbi_path}")

    st.write("")

    html(
        """
        <div class="section-title">Power BI Enterprise Architecture Overview</div>
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-card-header">
                    <div>
                        <div class="kpi-title">Data Modeling</div>
                        <div class="kpi-value" style="font-size: 22px;">Star Schema</div>
                    </div>
                    <div class="kpi-icon">⭐</div>
                </div>
                <div class="kpi-subtext">Dim_Date, Dim_Participant, Fact_DailyActivity, Fact_HourlyActivity</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-header">
                    <div>
                        <div class="kpi-title">DAX Analytics</div>
                        <div class="kpi-value" style="font-size: 22px;">25+ Measures</div>
                    </div>
                    <div class="kpi-icon">🧮</div>
                </div>
                <div class="kpi-subtext">Movement, Caloric burn, Sleep architecture, Strava Readiness Index</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-header">
                    <div>
                        <div class="kpi-title">ETL & Automation</div>
                        <div class="kpi-value" style="font-size: 22px;">Power Query M</div>
                    </div>
                    <div class="kpi-icon">⚙️</div>
                </div>
                <div class="kpi-subtext">Automated type coercion, date key formatting, data cleansing</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-card-header">
                    <div>
                        <div class="kpi-title">Storage Mode</div>
                        <div class="kpi-value" style="font-size: 22px;">DirectQuery / Import</div>
                    </div>
                    <div class="kpi-icon">🔄</div>
                </div>
                <div class="kpi-subtext">Live synchronization with SQLite fitness.db data warehouse</div>
            </div>
        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

html(
    """
    <div class="footer">
        STRAVA FITNESS DATA ANALYTICS • Python • SQL • SQLite • Streamlit
    </div>
    """
)
