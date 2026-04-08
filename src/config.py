from pathlib import Path
from dotenv import load_dotenv
import os

# project configuration from .env (secret part)
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)  # loads into os.environ

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
METEOSTAT_URL = "https://meteostat.p.rapidapi.com/point/daily"

# project configuration
DATA_DIR = "../data"
RESULTS_DIR = "../results"

# data sources configuration
SKANEATELES_LAT = 42.9476
SKANEATELES_LON = -76.4296
SKANEATELES_ALT = 268  # 海拔，单位：米

# Google Trends
TRENDS_KEYWORDS = [
    "Skaneateles Lake",
    "Dickens Christmas",
    "Finger Lakes winter",
    "Finger Lakes ski",
    "Skaneateles Airbnb",
]
TRENDS_GEO = "US"


WINTER_SEASONS = [
    #("2022-11-01", "2023-03-31"),
    #("2023-11-01", "2024-03-31"),
    ("2024-11-01", "2025-03-31"),
]

AIRBNB_SEARCH_URL = "https://www.airbnb.com/s/Skaneateles-Lake--NY--United-States/homes"