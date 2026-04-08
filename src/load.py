import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from config import (
    SKANEATELES_ALT, SKANEATELES_LAT, SKANEATELES_LON,
    WINTER_SEASONS, RAPIDAPI_KEY, METEOSTAT_URL,
    TRENDS_KEYWORDS, TRENDS_GEO,
    AIRBNB_SEARCH_URL
)


def get_weather_data():
    print("Loading weather data from Meteostat API:")

    headers = {
        "x-rapidapi-host": "meteostat.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    all_weather_data = []
    for start_str, end_str in WINTER_SEASONS:
        print(f"Fetching weather data from {start_str} to {end_str}...")

        parameters = {
            "lat": SKANEATELES_LAT,
            "lon": SKANEATELES_LON,
            "alt": SKANEATELES_ALT,
            "start": start_str,
            "end": end_str
        }
        response = requests.get(METEOSTAT_URL, headers=headers, params=parameters)
        data = response.json()
        weather_data = pd.DataFrame(data["data"])
        all_weather_data.append(weather_data)

    combined = pd.concat(all_weather_data, ignore_index=True)
    print(f"{len(combined)} weather data collected.")
    return combined


def get_trends_data():
    print("Loading Google Trends data:")
    pytrends = TrendReq(hl="en-US", tz=360)
    all_trend_data = []
    for start_str, end_str in WINTER_SEASONS:
        timeframe = f'{start_str} {end_str}'

        for keyword in TRENDS_KEYWORDS:
            print(f"Fetching '{keyword}' data from {start_str} to {end_str}...")

            pytrends.build_payload([keyword], timeframe=timeframe, geo=TRENDS_GEO)
            df = pytrends.interest_over_time()

            if df.empty:
                print(f"No data found for '{keyword}'.")
                continue

            df = df.reset_index()[["date", keyword]]
            df = df.rename(columns={keyword: "interest"})
            df["keyword"] = keyword
            all_trend_data.append(df)

            time.sleep(1)

    if not all_trend_data:
        print("No trends data collected.")
        return None

    combined = pd.concat(all_trend_data, ignore_index=True)
    print(f"{len(combined)} trend data collected.")
    return combined


def get_airbnb_data(checkin="2025-01-10", checkout="2025-01-17"):
    print("Loading Airbnb listing data:")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    params = {
        "checkin": checkin,
        "checkout": checkout,
    }

    response = requests.get(AIRBNB_SEARCH_URL, headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    script = soup.find("script", {"id": "__NEXT_DATA__"})


    if not script:
        print("Could not find data.")
        return None

    data = json.loads(script.string)
    print("Successfully fetched Airbnb page!")
    return data


if __name__ == "__main__":
    df = get_weather_data()
    print(df.head())

    df = get_trends_data()
    print(df.head())

    data = get_airbnb_data()
    print(data)

