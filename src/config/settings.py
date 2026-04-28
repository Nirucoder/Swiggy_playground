import os

# API Keys
WEATHER_API_KEY = "745266e7a2224532b54174149262504"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# Data Files
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
FINAL_TRAINING_DATA = os.path.join(PROCESSED_DATA_DIR, "final_training_data.csv")
HOURLY_TRAINING_DATA = os.path.join(PROCESSED_DATA_DIR, "final_training_data_hourly.csv")
FORECAST_SUMMARY = os.path.join(PROCESSED_DATA_DIR, "forecast_summary.csv")
LIVE_DATA_PATH = os.path.join(DATA_DIR, "live", "swiggy_live.json")

# Scraper Config
SCRAPER_SCRIPT = os.path.join(SCRIPTS_DIR, "scraper", "live_scraper.py")
DEFAULT_RESTAURANT_URL = "https://www.swiggy.com/restaurants/meghana-foods-residency-road-lavelle-road-bangalore-5182"

# UI Config
SWIGGY_ORANGE = "#fc8019"
SWIGGY_DARK = "#282c3f"
BACKGROUND_COLOR = "#f5f5f5"
