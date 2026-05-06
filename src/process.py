import pandas as pd
from config import WINTER_HOLIDAYS


def process_weather_data(weather_df):
    weather_df_processed = weather_df.copy()
    weather_df_processed["date"] = pd.to_datetime(weather_df_processed["date"]).dt.date
    weather_df_processed["is_snowy"] = (weather_df_processed["snow"] > 0).astype(int)
    weather_df_processed["is_cold"] = (weather_df_processed["tavg"] < -5).astype(int)
    return weather_df_processed


def add_calendar_features(df, date_col="date"):
    df_calendar = df.copy()
    df_calendar[date_col] = pd.to_datetime(df_calendar[date_col])
    df_calendar["year"] = df_calendar[date_col].dt.year
    df_calendar["month"] = df_calendar[date_col].dt.month
    df_calendar["is_weekend"] = df_calendar[date_col].dt.dayofweek.isin([5, 6]).astype(int)
    holidays = pd.to_datetime(WINTER_HOLIDAYS)
    df_calendar["is_holiday"] = df_calendar[date_col].isin(holidays).astype(int)
    return df_calendar


def process_trends_data(trends_df):
    trends_df_pivot = trends_df.pivot_table(
        index="date",
        columns="keyword",
        values="interest"
    )
    trends_df_pivot.columns = [f"trend_{c.lower().replace(' ', '_')}"
                                for c in trends_df_pivot.columns]
    trends_df_pivot = trends_df_pivot.reset_index()
    return trends_df_pivot


def process_airbnb_data(airbnb_df):
    airbnb_df_clean = airbnb_df.copy()
    airbnb_df_clean["date"] = pd.to_datetime(airbnb_df_clean["date"])
    airbnb_df_clean = airbnb_df_clean.dropna(subset=["price_usd"])
    airbnb_df_clean = airbnb_df_clean[airbnb_df_clean["price_usd"] > 0]
    holidays = pd.to_datetime(WINTER_HOLIDAYS)
    airbnb_df_clean = airbnb_df_clean[~airbnb_df_clean["date"].isin(holidays)]

    listing_counts = airbnb_df_clean.groupby("airbnb_id").size()
    valid_ids = listing_counts[listing_counts >= 30].index
    airbnb_df_clean = airbnb_df_clean[airbnb_df_clean["airbnb_id"].isin(valid_ids)]

    return airbnb_df_clean


def merge_all(weather_df, trends_df, airbnb_df):
    weather_df_processed = process_weather_data(weather_df)
    weather_df_processed = add_calendar_features(weather_df_processed)
    trends_df_pivot = process_trends_data(trends_df)
    airbnb_df_clean = process_airbnb_data(airbnb_df)

    weather_df_processed["date"] = pd.to_datetime(weather_df_processed["date"])
    trends_df_pivot["date"] = pd.to_datetime(trends_df_pivot["date"])
    airbnb_df_clean["date"] = pd.to_datetime(airbnb_df_clean["date"])


    weather_trends_df = pd.merge(weather_df_processed, trends_df_pivot, on="date", how="left")
    merged_df = pd.merge(airbnb_df_clean, weather_trends_df, on="date", how="left")

    return merged_df