import requests
import pandas as pd
import time
from pytrends.request import TrendReq
from config import (
    SKANEATELES_ALT, SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ZIP,
    CANANDAIGUA_LAT, CANANDAIGUA_LON, CANANDAIGUA_ALT, CANANDAIGUA_ZIP, TRENDS_KEYWORDS_CANANDAIGUA,
    WINTER_SEASONS, AIRBNB_WINTER_MONTHS, RAPIDAPI_KEY, METEOSTAT_URL,
    TRENDS_KEYWORDS, TRENDS_GEO,
    AIRBNB_LISTINGS_URL, AIRBNB_LISTING_DETAILS_URL, AIRBNB_LISTING_PRICES_URL, AIRBNB_COUNTRY
)


def get_weather_data(lat, lon, alt):
    print(f"Loading weather data (lat={lat}, lon={lon}):")

    headers = {
        "x-rapidapi-host": "meteostat.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    all_weather_data = []
    for start_str, end_str in WINTER_SEASONS:
        print(f"Fetching weather data from {start_str} to {end_str}...")
        parameters = {
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "start": start_str,
            "end": end_str
        }
        response = requests.get(METEOSTAT_URL, headers=headers, params=parameters)
        data = response.json()
        weather_df = pd.DataFrame(data["data"])
        all_weather_data.append(weather_df)

    combined_weather = pd.concat(all_weather_data, ignore_index=True)
    print(f"{len(combined_weather)} weather records collected.")
    return combined_weather

def get_trends_data(keywords=TRENDS_KEYWORDS):
    print("Loading Google Trends data:")
    pytrends = TrendReq(hl="en-US", tz=360)
    all_trend_data = []
    for start_str, end_str in WINTER_SEASONS:
        timeframe = f'{start_str} {end_str}'

        for keyword in keywords:
            print(f"Fetching '{keyword}' data from {start_str} to {end_str}...")

            pytrends.build_payload([keyword], timeframe=timeframe, geo=TRENDS_GEO)
            trend_df = pytrends.interest_over_time()

            if trend_df.empty:
                print(f"No data found for '{keyword}'.")
                continue

            trend_df = trend_df.reset_index()[["date", keyword]]
            trend_df = trend_df.rename(columns={keyword: "interest"})
            trend_df["keyword"] = keyword
            all_trend_data.append(trend_df)
            time.sleep(1) # AI generated:avoid rate limiting

    if not all_trend_data:
        print("No trends data collected.")
        return None


    combined_trends = pd.concat(all_trend_data, ignore_index=True)
    print(f"{len(combined_trends)} trend data collected.")
    return combined_trends

def get_total_listings(zipcode):
    print(f"Testing total listings for zipcode {zipcode}...")

    headers = {
        "x-rapidapi-host": "airbnb-listings.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    total = 0
    for offset in [0, 50, 100, 150, 200, 250, 300]:
        response = requests.get(
            AIRBNB_LISTINGS_URL,
            headers=headers,
            params={"state": AIRBNB_COUNTRY, "zipcode": zipcode, "offset": offset}
        )
        results = response.json().get("results", [])
        count = len(results)
        print(f"  Offset {offset}: {count} listings")
        total += count
        time.sleep(0.5)

        if count < 50:
            print(f"  Last page reached at offset {offset}")
            break

    print(f"Total listings found: {total}")
    return total


def get_airbnb_data(zipcode=SKANEATELES_ZIP, max_listings=50, offset=0, country=AIRBNB_COUNTRY):
    print("Loading Airbnb listing data via RapidAPI:")

    headers = {
        "x-rapidapi-host": "airbnb-listings.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }

    response = requests.get(
        AIRBNB_LISTINGS_URL,
        headers=headers,
        params={"state": country, "zipcode": zipcode, "offset": offset}
    )

    results = response.json().get("results", [])
    listing_ids = [r["airbnb_id"] for r in results[:max_listings]]
    print(f"Got {len(listing_ids)} listing IDs")

    all_listings = []
    for listing_id in listing_ids:
        try:
            details_data = requests.get(
                AIRBNB_LISTING_DETAILS_URL,
                headers=headers,
                params={"id": listing_id},
                timeout=20
            ).json()
            detail = details_data.get("results", [{}])[0]
        except Exception as e:
            print(f"  Skipping listing {listing_id} details: {e}")
            continue

        prices_list = []
        for year, month in AIRBNB_WINTER_MONTHS:
            print(f"Fetching prices for listing {listing_id} - {year}/{month}...")
            try:
                prices_data = requests.get(
                    AIRBNB_LISTING_PRICES_URL,
                    headers=headers,
                    params={"id": listing_id, "year": year, "month": month},
                    timeout=20
                ).json()
                prices_list += prices_data.get("results", [])
            except Exception as e:
                print(f"  Skipping {listing_id} - {year}/{month}: {e}")
                continue
            time.sleep(0.5)

        for price_entry in prices_list:
            all_listings.append({
                "airbnb_id": listing_id,
                "date": price_entry["date"],
                "price_usd": price_entry["price_usd"],
                "bedrooms": detail.get("bedrooms"),
                "bathrooms": detail.get("bathrooms"),
                "star_rating": detail.get("starRating"),
                "review_count": detail.get("reviewCount"),
                "property_type": detail.get("propertyType"),
                "room_type": detail.get("roomType"),
                "is_superhost": detail.get("isSuperhost"),
            })

    airbnb_df = pd.DataFrame(all_listings)
    print(f"{len(airbnb_df)} listings collected with details and prices.")
    return airbnb_df


if __name__ == "__main__":
    RUN_REGION = "canandaigua"

    if RUN_REGION == "skaneateles":
        weather_df = get_weather_data(SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ALT)
        weather_df.to_csv("../data/weather.csv", index=False)

        trends_df = get_trends_data(keywords=TRENDS_KEYWORDS)
        trends_df.to_csv("../data/trends.csv", index=False)

        all_dfs = []
        for offset in [0, 50, 100]:
            print(f"\nFetching Skaneateles listings offset={offset}")
            df = get_airbnb_data(zipcode=SKANEATELES_ZIP, offset=offset, max_listings=50)
            if df is not None and len(df) > 0:
                all_dfs.append(df)
            time.sleep(2)
        airbnb_df = pd.concat(all_dfs, ignore_index=True)
        airbnb_df.to_csv("../data/airbnb.csv", index=False)
        print(f"Total saved: {len(airbnb_df)} records")
        print(f"Total listings: {airbnb_df['airbnb_id'].nunique()}")


    elif RUN_REGION == "canandaigua":
        headers = {
            "x-rapidapi-host": "airbnb-listings.p.rapidapi.com",
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        test = requests.get(
            AIRBNB_LISTING_PRICES_URL,
            headers=headers,
            params={"id": 650212222409106646, "year": 2022, "month": 11}
        ).json()
        print(test)
        # total = get_total_listings(zipcode=CANANDAIGUA_ZIP)
        # weather_canandaigua_df = get_weather_data(CANANDAIGUA_LAT, CANANDAIGUA_LON, CANANDAIGUA_ALT)
        # weather_canandaigua_df.to_csv("../data/weather_canandaigua.csv", index=False)

        #trends_canandaigua_df = get_trends_data(keywords=TRENDS_KEYWORDS_CANANDAIGUA)
        #trends_canandaigua_df.to_csv("../data/trends_canandaigua.csv", index=False)
        #print(trends_canandaigua_df.groupby("keyword")["interest"].describe())

        # all_dfs = []
        # for offset in [0, 50, 100, 150, 200, 250]:
        #     print(f"\nFetching Canandaigua listings offset={offset}")
        #     df = get_airbnb_data(zipcode=CANANDAIGUA_ZIP, offset=offset, max_listings=50)
        #     if df is not None and len(df) > 0:
        #         all_dfs.append(df)
        #         temp_df = pd.concat(all_dfs, ignore_index=True)
        #         temp_df.to_csv("../data/airbnb_canandaigua.csv", index=False)
        #         print(f"Saved so far: {len(temp_df)} records")
        #     time.sleep(2)

        #airbnb_canandaigua_df = pd.concat(all_dfs, ignore_index=True)
        #airbnb_canandaigua_df.to_csv("../data/airbnb_canandaigua.csv", index=False)
        #print(f"Total saved: {len(airbnb_canandaigua_df)} records")
        #print(f"Total listings: {airbnb_canandaigua_df['airbnb_id'].nunique()}")

