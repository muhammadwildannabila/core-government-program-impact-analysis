# =========================================================
# app.py
# Government Program Impact Analysis
# Streamlit Elite Executive Dashboard
# =========================================================

# =========================================================
# PART 1 — IMPORT LIBRARIES & PAGE CONFIGURATION
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import joblib
from pathlib import Path

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Government Program Impact Analysis",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "program_impact_cleaned.csv"
SUMMARY_PATH = BASE_DIR / "data" / "processed" / "final_program_impact_summary.json"
MODEL_CLASSIFIER_PATH = BASE_DIR / "models" / "impact_classifier.pkl"
MODEL_REGRESSOR_PATH = BASE_DIR / "models" / "effectiveness_regressor.pkl"

# Load dataset
df = pd.read_csv(DATA_PATH, parse_dates=["start_date"])

# Load summary JSON
if SUMMARY_PATH.exists():
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        executive_summary = json.load(f)
else:
    executive_summary = {}

# Optional model loading
impact_model = joblib.load(MODEL_CLASSIFIER_PATH) if MODEL_CLASSIFIER_PATH.exists() else None
effectiveness_model = joblib.load(MODEL_REGRESSOR_PATH) if MODEL_REGRESSOR_PATH.exists() else None


# =========================================================
# PART 2 — CUSTOM CSS (ELITE UI/UX)
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(59,130,246,0.15), transparent 35%),
        radial-gradient(circle at top left, rgba(16,185,129,0.12), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0F172A 50%, #111827 100%);
    color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

.hero-card {
    background: linear-gradient(135deg,
        rgba(15,23,42,0.88),
        rgba(30,41,59,0.78));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 28px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 0.6rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.9;
    color: #CBD5E1;
    max-width: 900px;
}

.metric-card {
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.22);
    min-height: 160px;
}

.metric-label {
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.15;
}

.metric-sub {
    margin-top: 0.65rem;
    font-size: 0.85rem;
    color: #CBD5E1;
    line-height: 1.6;
}

.section-card {
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 26px;
    padding: 1.8rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.22);
}

.section-card h3 {
    color: #F8FAFC;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.status-pill {
    display: inline-block;
    padding: 0.55rem 1.1rem;
    border-radius: 999px;
    font-weight: 700;
    color: white;
    font-size: 0.82rem;
    letter-spacing: 0.03em;
}

.recommendation-card {
    background: rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.9rem;
    color: #E2E8F0;
    line-height: 1.8;
}
</style>
""",
    unsafe_allow_html=True,
)
# =========================================================
# PART 3 — HELPER FUNCTIONS
# Lanjutkan tepat setelah PART 2
# =========================================================

# ---------------------------------------------------------
# METRIC CARD COMPONENT
# ---------------------------------------------------------

def metric_card(title, value, subtitle):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# FORMAT LARGE CURRENCY
# ---------------------------------------------------------

def format_currency(value):
    if value >= 1_000_000_000_000:
        return f"Rp {value / 1_000_000_000_000:.1f} T"
    elif value >= 1_000_000_000:
        return f"Rp {value / 1_000_000_000:.1f} B"
    elif value >= 1_000_000:
        return f"Rp {value / 1_000_000:.1f} M"
    else:
        return f"Rp {value:,.0f}"


# ---------------------------------------------------------
# GET STATUS COLOR
# ---------------------------------------------------------

def get_status_color(status):
    status_colors = {
        "Excellent Performance": "#10B981",
        "Strong Performance": "#3B82F6",
        "Moderate Performance": "#F59E0B",
        "Strategic Intervention Required": "#EF4444",
    }
    return status_colors.get(status, "#64748B")


# ---------------------------------------------------------
# PLOTLY EXECUTIVE THEME
# ---------------------------------------------------------

def apply_executive_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.45)",
        font=dict(
            family="Inter",
            color="#E2E8F0",
            size=12,
        ),
        title=dict(
            font=dict(size=22, color="#F8FAFC"),
            x=0.02,
        ),
        margin=dict(l=40, r=40, t=70, b=40),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    )

    return fig


# =========================================================
# PART 4 — EXECUTIVE KPI CALCULATION
# =========================================================

total_programs = len(df)
total_budget = df["budget_allocated"].sum()
avg_effectiveness = df["effectiveness_score"].mean()
avg_roi = df["roi_score"].mean()
avg_satisfaction = df["satisfaction_score"].mean()
high_impact_rate = (
    (df["impact_category"] == "High Impact").mean() * 100
)

top_program = (
    df.groupby("program_name")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

top_department = (
    df.groupby("department")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

top_district = (
    df.groupby("district")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

program_status = executive_summary.get(
    "government_program_status",
    "Strong Performance"
)

recommendations = executive_summary.get(
    "strategic_recommendations",
    [
        "Scale high-performing programs and redesign low-impact initiatives."
    ],
)

status_color = get_status_color(program_status)
# =========================================================
# PART 5 — SIDEBAR FILTERS (EXECUTIVE CONTROL PANEL)
# Lanjutkan tepat setelah PART 4
# =========================================================

st.sidebar.markdown(
    """
    <div style="padding:0.25rem 0 1rem 0;">
        <h1 style="
            color:#F8FAFC;
            font-size:1.35rem;
            font-weight:700;
            margin-bottom:0.25rem;
        ">
            🎛️ Executive Control Panel
        </h1>
        <p style="
            color:#94A3B8;
            font-size:0.90rem;
            line-height:1.7;
            margin:0;
        ">
            Filter program data to explore performance, budget efficiency,
            and strategic insights across departments and districts.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# FILTER OPTIONS WITH "All"
# ---------------------------------------------------------

department_options = ["All"] + sorted(
    df["department"].dropna().unique().tolist()
)

program_options = ["All"] + sorted(
    df["program_name"].dropna().unique().tolist()
)

district_options = ["All"] + sorted(
    df["district"].dropna().unique().tolist()
)

impact_options = ["All"] + sorted(
    df["impact_category"].dropna().unique().tolist()
)

# ---------------------------------------------------------
# SIDEBAR FILTER WIDGETS
# ---------------------------------------------------------

selected_department = st.sidebar.selectbox(
    "🏛️ Department",
    department_options,
    index=0,
)

selected_program = st.sidebar.selectbox(
    "📦 Program",
    program_options,
    index=0,
)

selected_district = st.sidebar.selectbox(
    "📍 District",
    district_options,
    index=0,
)

selected_impact = st.sidebar.selectbox(
    "📊 Impact Category",
    impact_options,
    index=0,
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["department"] == selected_department
    ]

if selected_program != "All":
    filtered_df = filtered_df[
        filtered_df["program_name"] == selected_program
    ]

if selected_district != "All":
    filtered_df = filtered_df[
        filtered_df["district"] == selected_district
    ]

if selected_impact != "All":
    filtered_df = filtered_df[
        filtered_df["impact_category"] == selected_impact
    ]

# ---------------------------------------------------------
# HANDLE EMPTY FILTER RESULT
# ---------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No data available for the selected filter combination."
    )
    st.stop()

# ---------------------------------------------------------
# FILTERED KPI RECALCULATION
# ---------------------------------------------------------

total_programs = len(filtered_df)
total_budget = filtered_df["budget_allocated"].sum()
avg_effectiveness = filtered_df["effectiveness_score"].mean()
avg_roi = filtered_df["roi_score"].mean()
avg_satisfaction = filtered_df["satisfaction_score"].mean()
high_impact_rate = (
    (filtered_df["impact_category"] == "High Impact").mean() * 100
)

top_program = (
    filtered_df.groupby("program_name")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

top_department = (
    filtered_df.groupby("department")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

top_district = (
    filtered_df.groupby("district")["effectiveness_score"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

# Dynamic status
if avg_effectiveness >= 85:
    program_status = "Excellent Performance"
elif avg_effectiveness >= 75:
    program_status = "Strong Performance"
elif avg_effectiveness >= 65:
    program_status = "Moderate Performance"
else:
    program_status = "Strategic Intervention Required"

status_color = get_status_color(program_status)

# Sidebar dataset summary
st.sidebar.markdown("---")
st.sidebar.metric("📄 Filtered Records", f"{len(filtered_df):,}")
st.sidebar.metric(
    "🎯 Avg Effectiveness",
    f"{avg_effectiveness:.1f}"
)
st.sidebar.metric(
    "🚀 High Impact Rate",
    f"{high_impact_rate:.1f}%"
)
# =========================================================
# PART 6 — HERO SECTION, KPI CARDS, STATUS PANEL
# Lanjutkan tepat setelah PART 5
# =========================================================

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">
            🏛️ Government Program Impact Analysis
        </div>
        <div class="hero-subtitle">
            AI-powered executive dashboard for evaluating government
            program effectiveness, budget efficiency, citizen satisfaction,
            and strategic policy outcomes to support evidence-based
            decision-making.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# KPI OVERVIEW
# ---------------------------------------------------------

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    metric_card(
        "📦 Total Programs",
        f"{total_programs:,}",
        "Programs analyzed"
    )

with kpi_col2:
    metric_card(
        "💰 Total Budget",
        format_currency(total_budget),
        "Allocated budget"
    )

with kpi_col3:
    metric_card(
        "🎯 Avg Effectiveness",
        f"{avg_effectiveness:.1f}",
        "Program performance score"
    )

with kpi_col4:
    metric_card(
        "🚀 High Impact Rate",
        f"{high_impact_rate:.1f}%",
        "Top-performing initiatives"
    )

# ---------------------------------------------------------
# GOVERNMENT PROGRAM STATUS PANEL
# ---------------------------------------------------------

# =========================================================
# PART 6 — GOVERNMENT PROGRAM STATUS PANEL (STREAMLIT SAFE)
# SOLUSI TERBAIK: JANGAN GUNAKAN HTML BERSARANG KOMPLEKS
# GANTI SELURUH STATUS PANEL DENGAN KODE INI
# =========================================================

# ---------------------------------------------------------
# GOVERNMENT PROGRAM STATUS PANEL
# ---------------------------------------------------------

st.markdown("## 🏆 Government Program Status")

# Status badge sederhana
st.markdown(
    f"""
    <div style="
        display:inline-block;
        padding:0.55rem 1.1rem;
        border-radius:999px;
        background:{status_color};
        color:white;
        font-weight:700;
        font-size:0.82rem;
        letter-spacing:0.03em;
        margin-bottom:1rem;
    ">
        {program_status}
    </div>
    """,
    unsafe_allow_html=True,
)

# KPI cards menggunakan Streamlit columns (lebih stabil)
status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    metric_card(
        "🏅 Top Program",
        top_program,
        "Highest average effectiveness score"
    )

with status_col2:
    metric_card(
        "🏛️ Top Department",
        top_department,
        "Best-performing institution"
    )

with status_col3:
    metric_card(
        "📍 Top District",
        top_district,
        "Highest regional performance"
    )

# Strategic Assessment
st.markdown(
    f"""
    <div class="section-card">
        <h3>🧠 Strategic Assessment</h3>
        <div style="
            color:#BFD5FF;
            line-height:1.9;
            font-size:0.95rem;
        ">
            Government programs demonstrate
            <b>{program_status.lower()}</b>.
            Current analytics indicate opportunities to optimize
            budget allocation, scale high-performing initiatives,
            and strengthen evidence-based policy planning.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# MAIN NAVIGATION TABS
# ---------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Analytics",
    "🏛️ Program Performance",
    "🤖 AI Prediction Center",
    "🧠 Strategic Insights",
])
# =========================================================
# PART 7 — EXECUTIVE ANALYTICS TAB
# Letakkan tepat setelah PART 6
# =========================================================

with tab1:

    # -----------------------------------------------------
    # IMPACT CATEGORY DISTRIBUTION
    # -----------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        impact_df = (
            filtered_df["impact_category"]
            .value_counts()
            .reset_index()
        )
        impact_df.columns = ["Impact Category", "Count"]

        fig = px.pie(
            impact_df,
            names="Impact Category",
            values="Count",
            hole=0.68,
            title="Program Impact Distribution",
            color="Impact Category",
            color_discrete_map={
                "High Impact": "#10B981",
                "Moderate Impact": "#F59E0B",
                "Low Impact": "#EF4444",
            },
        )

        fig = apply_executive_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # EFFECTIVENESS SCORE DISTRIBUTION
    # -----------------------------------------------------
    with col2:
        fig = px.histogram(
            filtered_df,
            x="effectiveness_score",
            nbins=35,
            title="Effectiveness Score Distribution",
            color_discrete_sequence=["#60A5FA"],
        )

        fig.update_layout(
            xaxis_title="Effectiveness Score",
            yaxis_title="Number of Programs",
        )

        fig = apply_executive_theme(fig)
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # DEPARTMENT PERFORMANCE RANKING
    # -----------------------------------------------------
    department_perf = (
        filtered_df.groupby("department")
        .agg({
            "effectiveness_score": "mean",
            "roi_score": "mean",
            "satisfaction_score": "mean",
        })
        .round(2)
        .sort_values(
            "effectiveness_score",
            ascending=True
        )
        .reset_index()
    )

    fig = px.bar(
        department_perf,
        x="effectiveness_score",
        y="department",
        orientation="h",
        title="Department Performance Ranking",
        color="effectiveness_score",
        color_continuous_scale="Viridis",
        hover_data=[
            "roi_score",
            "satisfaction_score",
        ],
    )

    fig.update_layout(
        xaxis_title="Average Effectiveness Score",
        yaxis_title="",
    )

    fig = apply_executive_theme(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # BUDGET VS EFFECTIVENESS
    # -----------------------------------------------------
    sample_df = filtered_df.sample(
        min(2000, len(filtered_df)),
        random_state=42
    )

    fig = px.scatter(
        sample_df,
        x="budget_allocated",
        y="effectiveness_score",
        color="impact_category",
        size="beneficiaries",
        title="Budget Allocation vs Program Effectiveness",
        hover_data=[
            "program_name",
            "department",
            "district",
            "roi_score",
        ],
        color_discrete_map={
            "High Impact": "#10B981",
            "Moderate Impact": "#F59E0B",
            "Low Impact": "#EF4444",
        },
    )

    fig.update_layout(
        xaxis_title="Budget Allocated (IDR)",
        yaxis_title="Effectiveness Score",
    )

    fig = apply_executive_theme(fig)
    st.plotly_chart(
        fig,
        use_container_width=True
    )
# =========================================================
# PART 8 — PROGRAM PERFORMANCE TAB
# Letakkan tepat setelah PART 7
# =========================================================

with tab2:

    # -----------------------------------------------------
    # TOP 10 HIGH-IMPACT PROGRAMS
    # -----------------------------------------------------
    st.markdown("## 🏆 Top 10 High-Impact Programs")

    top_programs_df = (
        filtered_df
        .sort_values("effectiveness_score", ascending=False)
        [
            [
                "program_name",
                "department",
                "district",
                "budget_allocated",
                "beneficiaries",
                "effectiveness_score",
                "roi_score",
                "impact_category",
            ]
        ]
        .head(10)
        .copy()
    )

    # Format columns for presentation
    top_programs_display = top_programs_df.copy()
    top_programs_display["budget_allocated"] = (
        top_programs_display["budget_allocated"]
        .apply(format_currency)
    )
    top_programs_display["effectiveness_score"] = (
        top_programs_display["effectiveness_score"]
        .round(2)
    )
    top_programs_display["roi_score"] = (
        top_programs_display["roi_score"]
        .round(2)
    )

    st.dataframe(
        top_programs_display,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------------------------
    # DEPARTMENT PERFORMANCE TABLE
    # -----------------------------------------------------
    st.markdown("## 🏛️ Department Performance Ranking")

    department_table = (
        filtered_df.groupby("department")
        .agg({
            "effectiveness_score": "mean",
            "roi_score": "mean",
            "satisfaction_score": "mean",
            "budget_allocated": "sum",
            "beneficiaries": "sum",
        })
        .round(2)
        .sort_values(
            "effectiveness_score",
            ascending=False
        )
        .reset_index()
    )

    department_display = department_table.copy()
    department_display["budget_allocated"] = (
        department_display["budget_allocated"]
        .apply(format_currency)
    )
    department_display["beneficiaries"] = (
        department_display["beneficiaries"]
        .map(lambda x: f"{x:,.0f}")
    )

    st.dataframe(
        department_display,
        use_container_width=True,
        hide_index=True,
    )

    # -----------------------------------------------------
    # ROI DISTRIBUTION BY IMPACT CATEGORY
    # -----------------------------------------------------
    st.markdown("## 💹 ROI Distribution by Impact Category")

    fig = px.box(
        filtered_df,
        x="impact_category",
        y="roi_score",
        color="impact_category",
        title="ROI Score Distribution",
        color_discrete_map={
            "High Impact": "#10B981",
            "Moderate Impact": "#F59E0B",
            "Low Impact": "#EF4444",
        },
    )

    fig.update_layout(
        xaxis_title="Impact Category",
        yaxis_title="ROI Score",
    )

    fig = apply_executive_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
# =========================================================
# PART 9 — AI PREDICTION CENTER TAB
# Letakkan tepat setelah PART 8
# =========================================================

with tab3:

    st.markdown("## 🤖 AI Prediction Center")
    st.caption(
        "Simulate a government program scenario and let the trained "
        "Machine Learning models estimate impact category and "
        "effectiveness score."
    )

    if impact_model is None or effectiveness_model is None:
        st.warning(
            "Prediction models are not available. "
            "Please complete STEP 4 and ensure the .pkl files "
            "exist in the models/ directory."
        )
    else:

        # -------------------------------------------------
        # INPUT FORM
        # -------------------------------------------------
        with st.form("prediction_form"):

            c1, c2, c3 = st.columns(3)

            with c1:
                input_program = st.selectbox(
                    "Program Name",
                    sorted(df["program_name"].unique())
                )
                input_department = st.selectbox(
                    "Department",
                    sorted(df["department"].unique())
                )
                input_district = st.selectbox(
                    "District",
                    sorted(df["district"].unique())
                )
                input_budget = st.number_input(
                    "Budget Allocated (IDR)",
                    min_value=100_000_000,
                    value=5_000_000_000,
                    step=100_000_000,
                )

            with c2:
                input_beneficiaries = st.number_input(
                    "Beneficiaries",
                    min_value=100,
                    value=10000,
                    step=100,
                )
                input_completion = st.slider(
                    "Completion Rate (%)",
                    0.0, 100.0, 85.0
                )
                input_budget_util = st.slider(
                    "Budget Utilization (%)",
                    0.0, 100.0, 90.0
                )
                input_satisfaction = st.slider(
                    "Satisfaction Score",
                    1.0, 5.0, 4.2, 0.1
                )

            with c3:
                input_social = st.number_input(
                    "Social Engagement",
                    min_value=0,
                    value=25000,
                    step=1000,
                )
                input_sentiment = st.slider(
                    "Sentiment Score",
                    -1.0, 1.0, 0.5, 0.01
                )
                input_reach = st.slider(
                    "Reach Rate (%)",
                    0.0, 100.0, 80.0
                )

            submitted = st.form_submit_button(
                "🚀 Run AI Prediction",
                use_container_width=True
            )

        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------
        if submitted:

            cost_per_beneficiary = (
                input_budget / max(input_beneficiaries, 1)
            )

            roi_score = (
                input_completion * 0.30
                + input_budget_util * 0.15
                + (input_satisfaction / 5) * 100 * 0.25
                + input_reach * 0.20
                + ((input_sentiment + 1) / 2) * 100 * 0.10
            )

            effectiveness_formula = roi_score

            budget_efficiency_score = (
                effectiveness_formula /
                max(input_budget_util / 100, 0.01)
            )

            # Derived categorical features
            if input_beneficiaries <= 5000:
                beneficiary_scale = "Small Scale"
            elif input_beneficiaries <= 20000:
                beneficiary_scale = "Medium Scale"
            else:
                beneficiary_scale = "Large Scale"

            if input_satisfaction <= 3.0:
                satisfaction_category = "Low"
            elif input_satisfaction <= 4.0:
                satisfaction_category = "Moderate"
            else:
                satisfaction_category = "High"

            # Estimate budget tier from quartiles
            budget_q = df["budget_allocated"].quantile(
                [0.25, 0.50, 0.75]
            )

            if input_budget <= budget_q.iloc[0]:
                budget_tier = "Tier 1"
            elif input_budget <= budget_q.iloc[1]:
                budget_tier = "Tier 2"
            elif input_budget <= budget_q.iloc[2]:
                budget_tier = "Tier 3"
            else:
                budget_tier = "Tier 4"

            program_age_days = 365
            program_maturity = "Established"

            prediction_input = pd.DataFrame([{
                "program_name": input_program,
                "department": input_department,
                "district": input_district,
                "budget_allocated": input_budget,
                "beneficiaries": input_beneficiaries,
                "completion_rate": input_completion,
                "budget_utilization": input_budget_util,
                "satisfaction_score": input_satisfaction,
                "social_engagement": input_social,
                "sentiment_score": input_sentiment,
                "reach_rate": input_reach,
                "cost_per_beneficiary": cost_per_beneficiary,
                "roi_score": roi_score,
                "budget_efficiency_score": budget_efficiency_score,
                "program_age_days": program_age_days,
                "beneficiary_scale": beneficiary_scale,
                "satisfaction_category": satisfaction_category,
                "budget_tier": budget_tier,
                "program_maturity": program_maturity,
            }])

            predicted_impact = impact_model.predict(
                prediction_input
            )[0]

            predicted_effectiveness = (
                effectiveness_model.predict(
                    prediction_input
                )[0]
            )
                        # -------------------------------------------------
            # DISPLAY PREDICTION RESULTS
            # -------------------------------------------------

            st.markdown("## 🏆 AI Prediction Results")

            result_col1, result_col2, result_col3 = st.columns(3)

            # Predicted Impact Category
            with result_col1:
                impact_color_map = {
                    "High Impact": "#10B981",
                    "Moderate Impact": "#F59E0B",
                    "Low Impact": "#EF4444",
                }

                predicted_color = impact_color_map.get(
                    predicted_impact,
                    "#64748B",
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🏷️ Predicted Impact Category
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;
                                    color:{predicted_color};">
                            {predicted_impact}
                        </div>
                        <div class="metric-sub">
                            Machine Learning classification result
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Predicted Effectiveness Score
            with result_col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🎯 Predicted Effectiveness Score
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;">
                            {predicted_effectiveness:.2f}
                        </div>
                        <div class="metric-sub">
                            Estimated overall program performance
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Formula-Based ROI Score
            with result_col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            💹 Estimated ROI Score
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;">
                            {roi_score:.2f}
                        </div>
                        <div class="metric-sub">
                            Analytical investment efficiency score
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # -------------------------------------------------
            # STRATEGIC INTERPRETATION
            # -------------------------------------------------

            if predicted_impact == "High Impact":
                prediction_recommendation = (
                    "Scale up this program and replicate its design "
                    "across other departments."
                )
            elif predicted_impact == "Moderate Impact":
                prediction_recommendation = (
                    "Optimize execution, stakeholder engagement, and "
                    "budget utilization to improve impact."
                )
            else:
                prediction_recommendation = (
                    "Conduct a strategic review and redesign the "
                    "program before additional budget allocation."
                )

            st.markdown(
                f"""
                <div class="section-card">
                    <h3>🧠 Strategic Recommendation</h3>
                    <div class="recommendation-card">
                        {prediction_recommendation}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # -------------------------------------------------
            # DISPLAY PREDICTION RESULTS
            # -------------------------------------------------

            st.markdown("## 🏆 AI Prediction Results")

            result_col1, result_col2, result_col3 = st.columns(3)

            # Predicted Impact Category
            with result_col1:
                impact_color_map = {
                    "High Impact": "#10B981",
                    "Moderate Impact": "#F59E0B",
                    "Low Impact": "#EF4444",
                }

                predicted_color = impact_color_map.get(
                    predicted_impact,
                    "#64748B",
                )

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🏷️ Predicted Impact Category
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;
                                    color:{predicted_color};">
                            {predicted_impact}
                        </div>
                        <div class="metric-sub">
                            Machine Learning classification result
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Predicted Effectiveness Score
            with result_col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🎯 Predicted Effectiveness Score
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;">
                            {predicted_effectiveness:.2f}
                        </div>
                        <div class="metric-sub">
                            Estimated overall program performance
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Formula-Based ROI Score
            with result_col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            💹 Estimated ROI Score
                        </div>
                        <div class="metric-value"
                             style="font-size:1.45rem;">
                            {roi_score:.2f}
                        </div>
                        <div class="metric-sub">
                            Analytical investment efficiency score
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # -------------------------------------------------
            # STRATEGIC INTERPRETATION
            # -------------------------------------------------

            if predicted_impact == "High Impact":
                prediction_recommendation = (
                    "Scale up this program and replicate its design "
                    "across other departments."
                )
            elif predicted_impact == "Moderate Impact":
                prediction_recommendation = (
                    "Optimize execution, stakeholder engagement, and "
                    "budget utilization to improve impact."
                )
            else:
                prediction_recommendation = (
                    "Conduct a strategic review and redesign the "
                    "program before additional budget allocation."
                )

            st.markdown(
                f"""
                <div class="section-card">
                    <h3>🧠 Strategic Recommendation</h3>
                    <div class="recommendation-card">
                        {prediction_recommendation}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
# =========================================================
# PART 10 — STRATEGIC INSIGHTS TAB
# Letakkan tepat setelah PART 9
# =========================================================

with tab4:

    # -----------------------------------------------------
    # STRATEGIC RECOMMENDATIONS
    # -----------------------------------------------------
    st.markdown("## 🧠 AI Strategic Recommendations")
    st.caption(
        "Automatically generated executive recommendations based on "
        "program performance, budget efficiency, and impact analytics."
    )

    for i, recommendation in enumerate(recommendations, start=1):
        st.markdown(
            f"""
            <div class="recommendation-card">
                <b>{i}.</b> {recommendation}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # EXECUTIVE SUMMARY HIGHLIGHTS
    # -----------------------------------------------------
    st.markdown("## 📄 Executive Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        metric_card(
            "🏛️ Government Status",
            program_status,
            "Overall strategic assessment"
        )

        metric_card(
            "🏆 Top Department",
            top_department,
            "Highest average effectiveness"
        )

        metric_card(
            "📍 Top District",
            top_district,
            "Best-performing regional area"
        )

    with summary_col2:
        metric_card(
            "🎯 Avg ROI Score",
            f"{avg_roi:.2f}",
            "Return on investment indicator"
        )

        metric_card(
            "😊 Citizen Satisfaction",
            f"{avg_satisfaction:.2f} / 5",
            "Average public satisfaction score"
        )

        metric_card(
            "🚀 High Impact Programs",
            f"{high_impact_rate:.1f}%",
            "Programs classified as High Impact"
        )

    # -----------------------------------------------------
    # EXECUTIVE SUMMARY JSON OUTPUT
    # -----------------------------------------------------
    st.markdown("## 📄 Executive Summary (JSON Output)")

    st.json(
        {
            "total_programs": int(total_programs),
            "total_budget_allocated": round(
                float(total_budget), 2
            ),
            "average_effectiveness_score": round(
                float(avg_effectiveness), 2
            ),
            "average_roi_score": round(
                float(avg_roi), 2
            ),
            "average_satisfaction_score": round(
                float(avg_satisfaction), 2
            ),
            "high_impact_program_rate": round(
                float(high_impact_rate), 2
            ),
            "top_program": top_program,
            "top_department": top_department,
            "top_district": top_district,
            "government_program_status": program_status,
            "strategic_recommendations": recommendations,
        }
    )

# =========================================================
# END OF APP
# =========================================================