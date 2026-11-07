"""
ClimateTrend AI - Configuration Module
Consolidates decades of weather station data for trend dashboards.
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_PATH = DATA_DIR / "sample_weather_data.csv"

DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "warehouse.db"
DB_URL = f"sqlite:///{DB_PATH}"

MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "climate_model.pkl"

ASSETS_DIR = BASE_DIR / "assets"
CSS_PATH = ASSETS_DIR / "style.css"

# Ensure all primary runtime directories exist
for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_DIR, MODELS_DIR, ASSETS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Application Meta
APP_NAME = "ClimateTrend AI"
APP_SUBTITLE = "An Intelligent System to Consolidate Decades of Station Data for Trend Dashboards"
VERSION = "1.0.0"

# Target Stations (Synthetic & Demo Benchmark Stations)
STATION_METADATA = {
    "STN_HYD_01": {"name": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "elevation_m": 542},
    "STN_VJA_02": {"name": "Vijayawada", "state": "Andhra Pradesh", "lat": 16.5062, "lon": 80.6480, "elevation_m": 11},
    "STN_MAA_03": {"name": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "elevation_m": 6},
    "STN_BLR_04": {"name": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "elevation_m": 920},
    "STN_VTZ_05": {"name": "Visakhapatnam", "state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185, "elevation_m": 45},
}

# Required columns for validation
EXPECTED_COLUMNS = [
    "Station_ID",
    "Station_Name",
    "Date",
    "Temperature_Max",
    "Temperature_Min",
    "Rainfall",
    "Humidity",
    "Wind_Speed"
]

# Color Palette (Modern Dark Navy & Climate Green Theme)
THEME_COLORS = {
    "primary": "#10b981",       # Emerald Green
    "secondary": "#06b6d4",     # Cyan
    "accent": "#f59e0b",        # Amber
    "danger": "#ef4444",        # Red
    "background": "#0b1329",    # Deep Navy
    "card_bg": "#132144",       # Navy Card
    "text": "#e2e8f0",          # Light Slate
    "text_muted": "#94a3b8"     # Slate Muted
}
