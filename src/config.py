from pathlib import Path
from dotenv import load_dotenv
import os

# project configuration from .env (secret part)
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

METEOSTAT_URL = "https://meteostat.p.rapidapi.com/point/daily"
AIRBNB_LISTINGS_URL = "https://airbnb-listings.p.rapidapi.com/v2/listingsByZipcode"
AIRBNB_LISTING_DETAILS_URL = "https://airbnb-listings.p.rapidapi.com/v2/listing"
AIRBNB_LISTING_PRICES_URL = "https://airbnb-listings.p.rapidapi.com/v2/listingPrices"

# project configuration
DATA_DIR = "../data"
RESULTS_DIR = "../results"

# data sources configuration - Meteostat
SKANEATELES_LAT = 42.9476
SKANEATELES_LON = -76.4296
SKANEATELES_ALT = 268

# data sources configuration - Airbnb
SKANEATELES_ZIP = "13152"
AIRBNB_COUNTRY = "us"

# Canandaigua Lake, NY
CANANDAIGUA_LAT = 42.8870
CANANDAIGUA_LON = -77.2858
CANANDAIGUA_ALT = 207
CANANDAIGUA_ZIP = "14424"

# data sources configuration - Google Trends
TRENDS_GEO = "US"

TRENDS_KEYWORDS = [
    "Dickens Christmas",
    "Syracuse basketball",
    "Finger Lakes",
]

TRENDS_KEYWORDS_CANANDAIGUA = [
    "Fire Ice Festival",
    "Canandaigua Lake",
    "Finger Lakes",
    "Syracuse basketball",
    "Bristol Mountain",
]


WINTER_SEASONS = [
    ("2022-11-01", "2023-03-31"),
    ("2023-11-01", "2024-03-31"),
    ("2024-11-01", "2025-03-31"),
]

AIRBNB_WINTER_MONTHS = [
    (2022, 11), (2022, 12),
    (2023, 1), (2023, 2), (2023, 3),
    (2023, 11), (2023, 12),
    (2024, 1), (2024, 2), (2024, 3),
    (2024, 11), (2024, 12),
    (2025, 1), (2025, 2), (2025, 3),
]

WINTER_HOLIDAYS = [
    "2022-11-24", "2022-12-25", "2022-12-26",
    "2023-01-01", "2023-01-16", "2023-02-20",
    "2023-11-23", "2023-12-25",
    "2024-01-01", "2024-01-15", "2024-02-19",
    "2024-11-28", "2024-12-25",
    "2025-01-01", "2025-01-20", "2025-02-17",
]

SINGLE_LISTING_FEATURE_COLS = [
    "tavg",
    "is_snowy",
    "is_cold",
    "is_weekend",
    "year",
    "month",
    "trend_dickens_christmas",
    "trend_syracuse_basketball",
    "trend_finger_lakes",
]

FEATURE_COLS = SINGLE_LISTING_FEATURE_COLS

FEATURE_COLS_CANANDAIGUA = [
    "year",
    "month",
    "tavg",
    "is_snowy",
    "is_cold",
    "is_weekend",
    "trend_bristol_mountain",
    "trend_canandaigua_lake",
    "trend_fire_ice_festival",
    "trend_finger_lakes",
    "trend_syracuse_basketball",
]

PLOT_SIZE = (10, 6) # use in the analyze.py (better coding practice)