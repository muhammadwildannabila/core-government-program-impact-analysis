# =========================================================
# app.py v2 Premium
# Government Program Impact Intelligence
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
    page_title="Government Program Impact Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "program_impact_cleaned.csv"
SUMMARY_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "final_program_impact_summary.json"
)
CLASSIFIER_PATH = BASE_DIR / "models" / "impact_classifier.pkl"
REGRESSOR_PATH = BASE_DIR / "models" / "effectiveness_regressor.pkl"

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH, parse_dates=["start_date"])

if SUMMARY_PATH.exists():
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        executive_summary = json.load(f)
else:
    executive_summary = {}

impact_model = (
    joblib.load(CLASSIFIER_PATH)
    if CLASSIFIER_PATH.exists()
    else None
)

effectiveness_model = (
    joblib.load(REGRESSOR_PATH)
    if REGRESSOR_PATH.exists()
    else None
)
# =========================================================
# PART 2 — PREMIUM CSS REDESIGN
# Lanjutkan tepat setelah PART 1
# =========================================================

st.markdown(
    """
<style>
/* ======================================================
   GOOGLE FONT
====================================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ======================================================
   GLOBAL STYLING
====================================================== */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 12% 18%,
            rgba(59, 130, 246, 0.22),
            transparent 28%
        ),
        radial-gradient(
            circle at 88% 10%,
            rgba(139, 92, 246, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 78% 78%,
            rgba(16, 185, 129, 0.12),
            transparent 26%
        ),
        radial-gradient(
            circle at 30% 85%,
            rgba(245, 158, 11, 0.08),
            transparent 24%
        ),
        linear-gradient(
            135deg,
            #020617 0%,
            #071126 35%,
            #0F172A 70%,
            #111827 100%
        );

    color: #F8FAFC;
    background-attachment: fixed;
    min-height: 100vh;
}

/* ======================================================
   MAIN CONTAINER
====================================================== */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

/* ======================================================
   SIDEBAR
====================================================== */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0B1120 0%, #111827 55%, #1E1B4B 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.sidebar-panel {
    background:
        linear-gradient(180deg,
            rgba(15,23,42,0.78),
            rgba(30,41,59,0.55));
    border: 1px solid rgba(99,102,241,0.20);
    border-radius: 28px;
    padding: 1.35rem;
    margin-bottom: 1.25rem;
    box-shadow:
        0 20px 50px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.sidebar-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 0.55rem;
    letter-spacing: -0.02em;
}

.sidebar-subtitle {
    color: #94A3B8;
    font-size: 0.88rem;
    line-height: 1.8;
    margin: 0;
}

/* ======================================================
   HERO SECTION
====================================================== */
.hero-card {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg,
            rgba(15,23,42,0.90),
            rgba(30,41,59,0.72));
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 34px;
    padding: 2.6rem 2.8rem;
    margin-bottom: 2rem;
    box-shadow:
        0 28px 80px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.hero-card::before {
    content: "";
    position: absolute;
    top: -30%;
    right: -10%;
    width: 320px;
    height: 320px;
    background: radial-gradient(
        circle,
        rgba(59,130,246,0.18),
        transparent 70%
    );
    pointer-events: none;
}

.hero-title {
    font-size: 3.0rem;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: #FFFFFF;
    margin-bottom: 0.85rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.95;
    color: #CBD5E1;
    max-width: 980px;
}

/* ======================================================
   KPI CARDS
====================================================== */
.metric-card {
    background:
        linear-gradient(180deg,
            rgba(15,23,42,0.78),
            rgba(15,23,42,0.58));
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 28px;
    padding: 1.45rem 1.55rem;
    margin-bottom: 1rem;
    box-shadow:
        0 16px 48px rgba(0,0,0,0.22),
        inset 0 1px 0 rgba(255,255,255,0.03);
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(59,130,246,0.25);
}

.metric-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: #93C5FD;
    margin-bottom: 0.75rem;
}

.metric-value {
    font-size: 2.05rem;
    font-weight: 800;
    line-height: 1.10;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

.metric-sub {
    margin-top: 0.55rem;
    font-size: 0.85rem;
    color: #94A3B8;
    line-height: 1.6;
}

/* ======================================================
   SECTION CARD
====================================================== */
.section-card {
    background:
        linear-gradient(180deg,
            rgba(15,23,42,0.78),
            rgba(15,23,42,0.56));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 30px;
    padding: 1.8rem;
    margin-top: 1rem;
    margin-bottom: 1.75rem;
    box-shadow:
        0 18px 56px rgba(0,0,0,0.24);
}

.section-card h3 {
    font-size: 1.45rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 1rem;
}

/* ======================================================
   STATUS PILL
====================================================== */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1.2rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #FFFFFF;
    box-shadow: 0 8px 24px rgba(0,0,0,0.20);
}

/* ======================================================
   RECOMMENDATION CARD
====================================================== */
.recommendation-card {
    background:
        rgba(15,23,42,0.55);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
    color: #E2E8F0;
    line-height: 1.85;
}

/* ======================================================
   TABS
====================================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.75rem;
    background: rgba(15,23,42,0.42);
    padding: 0.4rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
    font-weight: 600;
    color: #CBD5E1;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.22),
        rgba(139,92,246,0.18)
    );
    color: #FFFFFF !important;
}

/* ======================================================
   DATAFRAME
====================================================== */
[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

/* ======================================================
   FOOTER
====================================================== */
.footer {
    text-align: center;
    color: #64748B;
    font-size: 0.86rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}
</style>
""",
    unsafe_allow_html=True,
)
# =========================================================
# PART 2 v3 — CSS ENHANCEMENT FOR PREMIUM SIDEBAR & STATUS
# TAMBAHKAN CSS INI DI AKHIR PART 2 (setelah </style> lama),
# ATAU SISIPKAN SEBELUM TAG </style> PADA CSS UTAMA.
# =========================================================

st.markdown(
    """
<style>

/* ======================================================
   MULTISELECT IMPROVEMENTS
====================================================== */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.20),
        rgba(139,92,246,0.18)
    ) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    color: #E2E8F0 !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] {
    border-radius: 18px !important;
}

section[data-testid="stSidebar"] [data-baseweb="popover"] {
    border-radius: 18px !important;
}

/* ======================================================
   SIDEBAR BUTTON
====================================================== */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.18),
        rgba(139,92,246,0.16)
    );
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 16px;
    color: #FFFFFF;
    font-weight: 700;
    min-height: 48px;
    transition: all 0.25s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: rgba(59,130,246,0.35);
    transform: translateY(-1px);
}

/* ======================================================
   SIDEBAR METRICS
====================================================== */
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(15,23,42,0.40);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 0.65rem 0.75rem;
}

/* ======================================================
   STREAMLIT ALERTS (SUCCESS / INFO)
====================================================== */
[data-testid="stAlert"] {
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}

/* ======================================================
   STATUS BADGE COLOR TUNING
====================================================== */
[data-testid="stAlert"][kind="success"] {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.18),
        rgba(16,185,129,0.12)
    ) !important;
}

[data-testid="stAlert"][kind="warning"] {
    background: linear-gradient(
        135deg,
        rgba(245,158,11,0.16),
        rgba(239,68,68,0.08)
    ) !important;
}

[data-testid="stAlert"][kind="info"] {
    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.16),
        rgba(139,92,246,0.10)
    ) !important;
}

</style>
""",
    unsafe_allow_html=True,
)
# =========================================================
# PART 3 — HELPER FUNCTIONS & EXECUTIVE COMPONENTS
# Lanjutkan tepat setelah PART 2
# =========================================================

# ---------------------------------------------------------
# METRIC CARD COMPONENT
# ---------------------------------------------------------

def metric_card(title, value, subtitle):
    """
    Render a premium KPI card.
    """
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
    """
    Format numeric values into readable Indonesian currency units.
    """
    if value >= 1_000_000_000_000:
        return f"Rp {value / 1_000_000_000_000:.1f} T"
    elif value >= 1_000_000_000:
        return f"Rp {value / 1_000_000_000:.1f} B"
    elif value >= 1_000_000:
        return f"Rp {value / 1_000_000:.1f} M"
    else:
        return f"Rp {value:,.0f}"


# ---------------------------------------------------------
# STATUS COLOR MAPPING
# ---------------------------------------------------------

def get_status_color(status):
    """
    Map strategic status labels to executive colors.
    """
    status_map = {
        "Excellent Performance": "#10B981",
        "Strong Performance": "#3B82F6",
        "Moderate Performance": "#F59E0B",
        "Strategic Intervention Required": "#EF4444",
    }
    return status_map.get(status, "#64748B")


# ---------------------------------------------------------
# PLOTLY EXECUTIVE THEME
# ---------------------------------------------------------

def apply_executive_theme(fig):
    """
    Apply a consistent premium dark theme to Plotly charts.
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.30)",
        font=dict(
            family="Inter",
            color="#E2E8F0",
            size=12,
        ),
        title=dict(
            font=dict(
                size=22,
                color="#FFFFFF",
            ),
            x=0.02,
        ),
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.08)",
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        linecolor="rgba(255,255,255,0.08)",
    )

    return fig


# ---------------------------------------------------------
# SAFE JSON SERIALIZATION
# ---------------------------------------------------------

def make_json_safe(obj):
    """
    Convert numpy/pandas types into JSON-serializable Python types.
    """
    if isinstance(obj, dict):
        return {
            k: make_json_safe(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [
            make_json_safe(v)
            for v in obj
        ]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj
# =========================================================
# PART 4 — EXECUTIVE KPI CALCULATION
# Lanjutkan tepat setelah PART 3
# =========================================================

# ---------------------------------------------------------
# BASE KPI CALCULATION
# ---------------------------------------------------------

total_programs = len(df)
total_budget = df["budget_allocated"].sum()
avg_effectiveness = df["effectiveness_score"].mean()
avg_roi = df["roi_score"].mean()
avg_satisfaction = df["satisfaction_score"].mean()
avg_budget_utilization = df["budget_utilization"].mean()

high_impact_rate = (
    (df["impact_category"] == "High Impact").mean() * 100
)

# ---------------------------------------------------------
# TOP PERFORMERS
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# STRATEGIC STATUS
# ---------------------------------------------------------

program_status = executive_summary.get(
    "government_program_status",
    "Strong Performance",
)

if avg_effectiveness >= 85:
    program_status = "Excellent Performance"
elif avg_effectiveness >= 75:
    program_status = "Strong Performance"
elif avg_effectiveness >= 65:
    program_status = "Moderate Performance"
else:
    program_status = "Strategic Intervention Required"

status_color = get_status_color(program_status)

# ---------------------------------------------------------
# STRATEGIC RECOMMENDATIONS
# ---------------------------------------------------------

recommendations = executive_summary.get(
    "strategic_recommendations",
    [
        "Scale high-performing programs and redesign low-impact initiatives.",
        "Optimize budget allocation to maximize public value.",
        "Strengthen evidence-based policy planning and monitoring.",
    ],
)

# ---------------------------------------------------------
# EXECUTIVE SUMMARY OBJECT
# ---------------------------------------------------------

executive_summary_live = {
    "total_programs": int(total_programs),
    "total_budget_allocated": float(total_budget),
    "average_effectiveness_score": round(float(avg_effectiveness), 2),
    "average_roi_score": round(float(avg_roi), 2),
    "average_satisfaction_score": round(float(avg_satisfaction), 2),
    "average_budget_utilization": round(
        float(avg_budget_utilization), 2
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

executive_summary_live = make_json_safe(
    executive_summary_live
)
# =========================================================
# PART 5 — EXECUTIVE CONTROL PANEL (SIDEBAR FILTERS)
# Lanjutkan tepat setelah PART 4
# =========================================================

# =========================================================
# PART 5 v3 — EXECUTIVE CONTROL PANEL PREMIUM
# GANTI SELURUH PART 5 DENGAN KODE BERIKUT
# =========================================================

# ---------------------------------------------------------
# SIDEBAR HEADER
# ---------------------------------------------------------

st.sidebar.markdown(
    """
    <div class="sidebar-panel">
        <div class="sidebar-title">
            🎛️ Executive Control Panel
        </div>
        <p class="sidebar-subtitle">
            Filter and compare departments, programs, districts,
            and impact categories using advanced multi-selection.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# RESET ALL FILTERS
# ---------------------------------------------------------

if st.sidebar.button(
    "🔄 Reset All Filters",
    use_container_width=True
):
    st.rerun()

# ---------------------------------------------------------
# MASTER OPTIONS
# ---------------------------------------------------------

department_options = sorted(
    df["department"].dropna().unique().tolist()
)

program_options = sorted(
    df["program_name"].dropna().unique().tolist()
)

district_options = sorted(
    df["district"].dropna().unique().tolist()
)

impact_options = sorted(
    df["impact_category"].dropna().unique().tolist()
)

# ---------------------------------------------------------
# FILTERS
# Default kosong = interpreted as "All"
# ---------------------------------------------------------

selected_departments = st.sidebar.multiselect(
    "🏛️ Departments",
    options=department_options,
    default=[],
    help="Leave empty to include all departments.",
)

selected_programs = st.sidebar.multiselect(
    "📦 Programs",
    options=program_options,
    default=[],
    help="Leave empty to include all programs.",
)

selected_districts = st.sidebar.multiselect(
    "📍 Districts",
    options=district_options,
    default=[],
    help="Leave empty to include all districts.",
)

selected_impacts = st.sidebar.multiselect(
    "📊 Impact Categories",
    options=impact_options,
    default=[],
    help="Leave empty to include all impact categories.",
)

# ---------------------------------------------------------
# INTERPRET EMPTY SELECTION AS ALL
# ---------------------------------------------------------

effective_departments = (
    selected_departments
    if selected_departments
    else department_options
)

effective_programs = (
    selected_programs
    if selected_programs
    else program_options
)

effective_districts = (
    selected_districts
    if selected_districts
    else district_options
)

effective_impacts = (
    selected_impacts
    if selected_impacts
    else impact_options
)

# ---------------------------------------------------------
# FILTER SUMMARY
# ---------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Active Filter Summary")

def summarize_selection(selected, label):
    if not selected:
        return f"**{label}:** All"
    return f"**{label}:** {len(selected)} selected"

st.sidebar.markdown(
    summarize_selection(selected_departments, "Departments")
)
st.sidebar.markdown(
    summarize_selection(selected_programs, "Programs")
)
st.sidebar.markdown(
    summarize_selection(selected_districts, "Districts")
)
st.sidebar.markdown(
    summarize_selection(selected_impacts, "Impact Categories")
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df[
    df["department"].isin(effective_departments)
    & df["program_name"].isin(effective_programs)
    & df["district"].isin(effective_districts)
    & df["impact_category"].isin(effective_impacts)
].copy()

# ---------------------------------------------------------
# HANDLE EMPTY RESULTS
# ---------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No data available for the selected filter combination."
    )
    st.stop()

# ---------------------------------------------------------
# RECALCULATE KPI
# ---------------------------------------------------------

total_programs = len(filtered_df)
total_budget = filtered_df["budget_allocated"].sum()
avg_effectiveness = filtered_df["effectiveness_score"].mean()
avg_roi = filtered_df["roi_score"].mean()
avg_satisfaction = filtered_df["satisfaction_score"].mean()
avg_budget_utilization = (
    filtered_df["budget_utilization"].mean()
)

high_impact_rate = (
    (filtered_df["impact_category"] == "High Impact").mean()
    * 100
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

# ---------------------------------------------------------
# STRATEGIC STATUS
# ---------------------------------------------------------

if avg_effectiveness >= 85:
    program_status = "Excellent Performance"
elif avg_effectiveness >= 75:
    program_status = "Strong Performance"
elif avg_effectiveness >= 65:
    program_status = "Moderate Performance"
else:
    program_status = "Strategic Intervention Required"

status_color = get_status_color(program_status)

# ---------------------------------------------------------
# SIDEBAR QUICK METRICS
# ---------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick Metrics")

st.sidebar.metric(
    "📄 Filtered Records",
    f"{total_programs:,}"
)

st.sidebar.metric(
    "🎯 Avg Effectiveness",
    f"{avg_effectiveness:.1f}"
)

st.sidebar.metric(
    "🚀 High Impact Rate",
    f"{high_impact_rate:.1f}%"
)

st.sidebar.metric(
    "💰 Total Budget",
    format_currency(total_budget)
)

# ---------------------------------------------------------
# SIDEBAR FOOTER
# ---------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.caption(
    "🤖 AI Models: "
    + (
        "Ready"
        if impact_model is not None
        and effectiveness_model is not None
        else "Unavailable"
    )
)
st.sidebar.caption(
    f"🕒 Last Updated: {pd.Timestamp.now():%d %b %Y %H:%M}"
)


# =========================================================
# PART 6 — HERO SECTION, KPI OVERVIEW & STATUS PANEL
# Lanjutkan tepat setelah PART 5
# =========================================================

# =========================================================
# PART 6 v3 — HERO SECTION PREMIUM + WOW STATUS PANEL
# GANTI SELURUH PART 6 DENGAN KODE BERIKUT
# =========================================================

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">
            🏛️ Government Program Impact Intelligence
        </div>
        <div class="hero-subtitle">
            AI-powered executive analytics platform for evaluating
            government program effectiveness, budget efficiency,
            citizen satisfaction, and strategic policy outcomes to
            support evidence-based public sector decision-making.
        </div>
        <div style="
            margin-top:1.2rem;
            display:flex;
            flex-wrap:wrap;
            gap:0.6rem;
        ">
            <span class="status-pill"
                  style="background:rgba(59,130,246,0.20);
                         border:1px solid rgba(59,130,246,0.35);">
                🤖 AI-Powered
            </span>
            <span class="status-pill"
                  style="background:rgba(16,185,129,0.20);
                         border:1px solid rgba(16,185,129,0.35);">
                📊 Interactive Analytics
            </span>
            <span class="status-pill"
                  style="background:rgba(139,92,246,0.20);
                         border:1px solid rgba(139,92,246,0.35);">
                🏛️ Policy Intelligence
            </span>
            <span class="status-pill"
                  style="background:rgba(245,158,11,0.20);
                         border:1px solid rgba(245,158,11,0.35);">
                🎯 Decision Support
            </span>
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
        "Allocated public budget"
    )

with kpi_col3:
    metric_card(
        "🎯 Avg Effectiveness",
        f"{avg_effectiveness:.1f}",
        "Composite performance score"
    )

with kpi_col4:
    metric_card(
        "🚀 High Impact Rate",
        f"{high_impact_rate:.1f}%",
        "Programs with strategic impact"
    )

# ---------------------------------------------------------
# GOVERNMENT PROGRAM STATUS PANEL
# ---------------------------------------------------------

st.markdown("## 🏆 Government Program Status")

# Premium status badge (native Streamlit safe)
st.success(f"**{program_status}**")

# Executive highlights
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
            color:#CBD5E1;
            line-height:1.95;
            font-size:0.95rem;
        ">
            Government programs currently demonstrate
            <b>{program_status.lower()}</b>.
            Analytics indicate opportunities to optimize budget
            allocation, scale high-performing initiatives, and
            strengthen evidence-based policy planning for
            improved public value creation.
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
# Lanjutkan tepat setelah PART 6
# =========================================================

with tab1:

    # -----------------------------------------------------
    # SECTION HEADER
    # -----------------------------------------------------
    st.markdown("## 📊 Executive Analytics")
    st.caption(
        "Interactive analytics for understanding program impact, "
        "budget efficiency, and institutional performance."
    )

    # -----------------------------------------------------
    # ROW 1 — IMPACT DISTRIBUTION & EFFECTIVENESS HISTOGRAM
    # -----------------------------------------------------
    analytics_col1, analytics_col2 = st.columns(2)

    # Impact Category Distribution
    with analytics_col1:
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
            hole=0.70,
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

    # Effectiveness Score Distribution
    with analytics_col2:
        fig = px.histogram(
            filtered_df,
            x="effectiveness_score",
            nbins=35,
            title="Effectiveness Score Distribution",
            color_discrete_sequence=["#3B82F6"],
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
    # ROW 2 — DEPARTMENT PERFORMANCE RANKING
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
    # ROW 3 — BUDGET VS EFFECTIVENESS
    # -----------------------------------------------------
    st.markdown("## 💰 Budget Efficiency Analytics")

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
        hover_data=[
            "program_name",
            "department",
            "district",
            "roi_score",
        ],
        title="Budget Allocation vs Program Effectiveness",
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
# Lanjutkan tepat setelah PART 7
# =========================================================

with tab2:

    # -----------------------------------------------------
    # SECTION HEADER
    # -----------------------------------------------------
    st.markdown("## 🏛️ Program Performance Intelligence")
    st.caption(
        "Detailed rankings and operational benchmarks for programs, "
        "departments, and investment returns."
    )

    # -----------------------------------------------------
    # TOP 10 HIGH-IMPACT PROGRAMS
    # -----------------------------------------------------
    st.markdown("### 🏆 Top 10 High-Impact Programs")

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

    # Format for presentation
    top_programs_display = top_programs_df.copy()
    top_programs_display["budget_allocated"] = (
        top_programs_display["budget_allocated"]
        .apply(format_currency)
    )
    top_programs_display["beneficiaries"] = (
        top_programs_display["beneficiaries"]
        .map(lambda x: f"{x:,.0f}")
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
    st.markdown("### 🏛️ Department Performance Ranking")

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
    # ROI DISTRIBUTION
    # -----------------------------------------------------
    st.markdown("### 💹 ROI Distribution by Impact Category")

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
# Lanjutkan tepat setelah PART 8
# =========================================================

with tab3:

    st.markdown("## 🤖 AI Prediction Center")
    st.caption(
        "Simulate a new government program scenario and let the "
        "Machine Learning models estimate its impact category and "
        "overall effectiveness score."
    )

    # -----------------------------------------------------
    # CHECK MODEL AVAILABILITY
    # -----------------------------------------------------
    if impact_model is None or effectiveness_model is None:
        st.warning(
            "Prediction models are not available. "
            "Please complete STEP 4 and ensure the model files "
            "exist in the models/ directory."
        )

    else:

        # -------------------------------------------------
        # PREDICTION FORM
        # -------------------------------------------------
        with st.form("prediction_form"):

            form_col1, form_col2, form_col3 = st.columns(3)

            # ---------------------------------------------
            # COLUMN 1
            # ---------------------------------------------
            with form_col1:
                input_program = st.selectbox(
                    "📦 Program Name",
                    sorted(df["program_name"].unique())
                )

                input_department = st.selectbox(
                    "🏛️ Department",
                    sorted(df["department"].unique())
                )

                input_district = st.selectbox(
                    "📍 District",
                    sorted(df["district"].unique())
                )

                input_budget = st.number_input(
                    "💰 Budget Allocated (IDR)",
                    min_value=100_000_000,
                    value=5_000_000_000,
                    step=100_000_000,
                )

            # ---------------------------------------------
            # COLUMN 2
            # ---------------------------------------------
            with form_col2:
                input_beneficiaries = st.number_input(
                    "👥 Beneficiaries",
                    min_value=100,
                    value=10_000,
                    step=100,
                )

                input_completion = st.slider(
                    "📈 Completion Rate (%)",
                    0.0, 100.0, 85.0
                )

                input_budget_util = st.slider(
                    "💸 Budget Utilization (%)",
                    0.0, 100.0, 90.0
                )

                input_satisfaction = st.slider(
                    "😊 Satisfaction Score",
                    1.0, 5.0, 4.2, 0.1
                )

            # ---------------------------------------------
            # COLUMN 3
            # ---------------------------------------------
            with form_col3:
                input_social = st.number_input(
                    "📣 Social Engagement",
                    min_value=0,
                    value=25_000,
                    step=1_000,
                )

                input_sentiment = st.slider(
                    "💬 Sentiment Score",
                    -1.0, 1.0, 0.5, 0.01
                )

                input_reach = st.slider(
                    "🌐 Reach Rate (%)",
                    0.0, 100.0, 80.0
                )

            submitted = st.form_submit_button(
                "🚀 Run AI Prediction",
                use_container_width=True
            )

        # -------------------------------------------------
        # RUN PREDICTION
        # -------------------------------------------------
        if submitted:

            # Derived metrics
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

            budget_efficiency_score = (
                roi_score /
                max(input_budget_util / 100, 0.01)
            )

            # Derived categorical features
            if input_beneficiaries <= 5_000:
                beneficiary_scale = "Small Scale"
            elif input_beneficiaries <= 20_000:
                beneficiary_scale = "Medium Scale"
            else:
                beneficiary_scale = "Large Scale"

            if input_satisfaction <= 3.0:
                satisfaction_category = "Low"
            elif input_satisfaction <= 4.0:
                satisfaction_category = "Moderate"
            else:
                satisfaction_category = "High"

            # Budget tier
            budget_quantiles = df["budget_allocated"].quantile(
                [0.25, 0.50, 0.75]
            )

            if input_budget <= budget_quantiles.iloc[0]:
                budget_tier = "Tier 1"
            elif input_budget <= budget_quantiles.iloc[1]:
                budget_tier = "Tier 2"
            elif input_budget <= budget_quantiles.iloc[2]:
                budget_tier = "Tier 3"
            else:
                budget_tier = "Tier 4"

            # Static derived features
            program_age_days = 365
            program_maturity = "Established"

            # Build prediction dataframe
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

            # Predictions
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

            st.markdown("### 🏆 AI Prediction Results")

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

            # Analytical ROI Score
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
            # STRATEGIC RECOMMENDATION
            # -------------------------------------------------

            if predicted_impact == "High Impact":
                prediction_recommendation = (
                    "Scale this program and replicate its design "
                    "across departments to maximize public value."
                )
            elif predicted_impact == "Moderate Impact":
                prediction_recommendation = (
                    "Optimize execution quality, stakeholder "
                    "engagement, and budget utilization."
                )
            else:
                prediction_recommendation = (
                    "Conduct a strategic redesign before allocating "
                    "additional budget resources."
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
# PART 10 — STRATEGIC INSIGHTS TAB & EXECUTIVE SUMMARY
# Lanjutkan tepat setelah PART 9
# =========================================================

with tab4:

    # -----------------------------------------------------
    # SECTION HEADER
    # -----------------------------------------------------
    st.markdown("## 🧠 Strategic Insights")
    st.caption(
        "AI-generated recommendations and executive summaries to support "
        "evidence-based policy and budget decisions."
    )

    # -----------------------------------------------------
    # STRATEGIC RECOMMENDATIONS
    # -----------------------------------------------------
    st.markdown("### 📌 Strategic Recommendations")

    for idx, recommendation in enumerate(recommendations, start=1):
        st.markdown(
            f"""
            <div class="recommendation-card">
                <b>{idx}.</b> {recommendation}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # EXECUTIVE HIGHLIGHTS
    # -----------------------------------------------------
    st.markdown("### 🏛️ Executive Highlights")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        metric_card(
            "🏆 Government Status",
            program_status,
            "Overall strategic assessment"
        )

        metric_card(
            "🏛️ Top Department",
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
            "🎯 Average ROI Score",
            f"{avg_roi:.2f}",
            "Return on investment indicator"
        )

        metric_card(
            "😊 Citizen Satisfaction",
            f"{avg_satisfaction:.2f} / 5",
            "Average public satisfaction"
        )

        metric_card(
            "🚀 High Impact Programs",
            f"{high_impact_rate:.1f}%",
            "Programs classified as High Impact"
        )

    # -----------------------------------------------------
    # EXECUTIVE SUMMARY JSON OUTPUT
    # -----------------------------------------------------
    st.markdown("### 📄 Executive Summary (JSON Output)")

    executive_summary_live = {
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
        "average_budget_utilization": round(
            float(avg_budget_utilization), 2
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

    st.json(
        make_json_safe(executive_summary_live)
    )


# =========================================================
# PART 11 — PREMIUM FOOTER
# Letakkan di bagian paling akhir app.py
# =========================================================

st.markdown(
    """
    <div class="footer">
        🏛️ Government Program Impact Intelligence<br>
        Core Experience Project — Internship Project (DISKOMINFO Kota Batu)<br>
        M.Wildan Nabila
    </div>
    """,
    unsafe_allow_html=True,
)
