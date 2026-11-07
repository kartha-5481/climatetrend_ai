"""
ClimateTrend AI - Main Entry Point & Executive Climate Dashboard
Consolidates decades of weather station data for trend dashboards.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Streamlit Page Configuration
st.set_page_config(
    page_title="ClimateTrend AI - Executive Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

import config
from modules.data_warehouse import query_consolidated_warehouse, get_warehouse_summary_statistics, init_warehouse_schema
from modules.etl_pipeline import ClimateETLPipeline
from modules.analytics import compute_annual_summary, compute_climate_trend_metrics, compute_station_comparison
from modules.visualizations import plot_temperature_trend, plot_annual_rainfall, plot_station_comparison_bar


# Helper to inject custom CSS
def load_css():
    if config.CSS_PATH.exists():
        with open(config.CSS_PATH, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# Ensure Database has baseline records on initial launch
@st.cache_resource(show_spinner=False)
def ensure_warehouse_seeded():
    init_warehouse_schema()
    stats = get_warehouse_summary_statistics()
    if stats["total_records"] == 0:
        pipeline = ClimateETLPipeline()
        pipeline.run_etl()


ensure_warehouse_seeded()


# Sidebar Navigation & Context
with st.sidebar:
    st.markdown("### 🌐 ClimateTrend AI")
    st.caption("Decadal Weather Station Data Warehouse & Analytics")
    st.divider()

    st.markdown("#### ⚡ Quick Actions")
    if st.button("🔄 Refresh Data from Warehouse", use_container_width=True):
        st.cache_data.clear()
        st.success("Warehouse cache refreshed.")

    st.markdown("---")
    st.markdown("#### 📍 Monitored Benchmark Stations")
    for stn_id, meta in config.STATION_METADATA.items():
        st.markdown(f"• **{meta['name']}** ({meta['state']}) — `{meta['elevation_m']}m`")

    st.markdown("---")
    st.caption("ClimateTrend AI v1.0.0 | Star-Schema SQLite Engine")


# Load warehouse data
@st.cache_data(ttl=600)
def load_dashboard_data():
    df = query_consolidated_warehouse()
    stats = get_warehouse_summary_statistics()
    return df, stats


df, stats = load_dashboard_data()

# Main Header
st.markdown("""
<div class="main-header">
    <div class="main-title">
        <span>🌍 ClimateTrend</span><span class="highlight"> AI</span>
    </div>
    <div class="subtitle">
        An Intelligent System to Consolidate Decades of Station Data for Trend Dashboards
    </div>
</div>
""", unsafe_allow_html=True)

# Transparent Demo Data Disclaimer
st.markdown("""
<div class="demo-badge">
    ⚠️ <strong>DEMONSTRATION SYNTHETIC DATA</strong>: Baseline dataset is synthetically generated with realistic seasonal physics for demonstration and testing. You can upload authentic CSV archives on the Data Upload page.
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("No data found in the warehouse. Initializing demonstration ETL pipeline...")
    pipeline = ClimateETLPipeline()
    pipeline.run_etl()
    st.rerun()

# KPI Metric Cards
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="kpi-card emerald">
        <div class="kpi-title">Total Records</div>
        <div class="kpi-value">{stats['total_records']:,}</div>
        <div class="kpi-subtitle">Fact Observations</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Stations</div>
        <div class="kpi-value">{stats['total_stations']}</div>
        <div class="kpi-subtitle">Integrated Centers</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card cyan">
        <div class="kpi-title">Timespan</div>
        <div class="kpi-value">{stats['years_covered']} yrs</div>
        <div class="kpi-subtitle">{stats['year_range']}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-title">Avg Temp</div>
        <div class="kpi-value">{stats['avg_temperature']}°C</div>
        <div class="kpi-subtitle">Consolidated Mean</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Rain</div>
        <div class="kpi-value">{int(stats['total_rainfall']):,} mm</div>
        <div class="kpi-subtitle">Accumulated Precip</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="kpi-card cyan">
        <div class="kpi-title">Avg Humidity</div>
        <div class="kpi-value">{stats['avg_humidity']}%</div>
        <div class="kpi-subtitle">Wind: {stats['avg_wind_speed']} km/h</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Filters & Charts
col_filter, col_spacer = st.columns([2, 4])
with col_filter:
    station_options = ["All"] + sorted(df["Station_Name"].unique().tolist())
    selected_stn = st.selectbox("🎯 Filter Trajectory by Weather Station:", station_options, index=0)

# Section: Climate Trajectory & Precipitation
col_chart1, col_chart2 = st.columns([3, 2])

with col_chart1:
    fig_temp = plot_temperature_trend(df, selected_stn)
    st.plotly_chart(fig_temp, use_container_width=True)

with col_chart2:
    filtered_for_annual = df if selected_stn == "All" else df[df["Station_Name"] == selected_stn]
    annual_df = compute_annual_summary(filtered_for_annual)
    fig_rain = plot_annual_rainfall(annual_df)
    st.plotly_chart(fig_rain, use_container_width=True)

# Section: Cross-Station Benchmarking and Analytics Insights
col_comp, col_insights = st.columns([3, 2])

with col_comp:
    station_summary = compute_station_comparison(df)
    fig_stn = plot_station_comparison_bar(station_summary)
    st.plotly_chart(fig_stn, use_container_width=True)

with col_insights:
    trend_metrics = compute_climate_trend_metrics(filtered_for_annual)
    
    st.markdown("""
    <div class="content-box">
        <div class="box-title">🧠 Climatological Analytics Insights</div>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Decadal ordinary least squares regressions computed across consolidated meteorological archives:
        </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    - **Estimated Warming Trend**: `<span style="color:#10b981; font-weight:700;">+{trend_metrics['temp_trend_per_decade']}°C / decade</span>`
    - **Rainfall Trend Drift**: `<span style="color:#06b6d4; font-weight:700;">{trend_metrics['rain_trend_per_decade']} mm / decade</span>`
    - **Peak Thermal Year**: `{trend_metrics['hottest_year']}`
    - **Peak Precipitation Year**: `{trend_metrics['wettest_year']}`
    - **Driest Year on Record**: `{trend_metrics['driest_year']}`
    """, unsafe_allow_html=True)

    st.markdown("""
        <hr style="border-color: rgba(255,255,255,0.08); margin: 12px 0;">
        <span class="status-pill success">Star Schema Synced</span>
        <span class="status-pill info">Time-Series Validated</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Use the left sidebar navigation to explore Data Upload, Data Exploration, Detailed Trends, Machine Learning Predictions, and Architecture details.")
