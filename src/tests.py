import pandas as pd
from config import DATA_DIR, FEATURE_COLS, SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ALT
from load import get_weather_data, get_trends_data
from process import process_weather_data, process_airbnb_data, merge_all
from analyze import get_feature_importance


def test_weather_data():
    print("Testing get_weather_data()...")
    try:
        df = get_weather_data(SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ALT)

        if df is None or len(df) == 0:
            print("FAILED: No data returned")
            return

        if "date" not in df.columns:
            print("FAILED: Missing date column")
            return

        if "tavg" not in df.columns:
            print("FAILED: Missing tavg column")
            return

        print(f"PASSED: {len(df)} records, columns: {list(df.columns)}")

    except Exception as e:
        print(f"FAILED: {e}")


def test_trends_data():
    print("Testing get_trends_data()...")
    try:
        df = get_trends_data()

        if df is None or len(df) == 0:
            print("FAILED: No data returned")
            return

        if "date" not in df.columns:
            print("FAILED: Missing date column")
            return

        if "interest" not in df.columns:
            print("FAILED: Missing interest column")
            return

        print(f"PASSED: {len(df)} records, columns: {list(df.columns)}")

    except Exception as e:
        print(f"FAILED: {e},  Google Trends may block frequent requests")

def test_process_weather_data():
    print("Testing process_weather_data...")
    try:
        df = pd.read_csv(f"{DATA_DIR}/weather.csv")

        processed = process_weather_data(df)

        if "is_snowy" not in processed.columns:
            print("FAILED: Missing is_snowy column")
            return

        if "is_cold" not in processed.columns:
            print("FAILED: Missing is_cold column")
            return

        print(f"PASSED: {len(processed)} records, is_snowy and is_cold columns present")

    except Exception as e:
        print(f"FAILED: {e}")


def test_process_airbnb_data():
    print("Testing process_airbnb_data...")
    try:
        df = pd.read_csv(f"{DATA_DIR}/airbnb.csv")

        processed = process_airbnb_data(df)

        if processed["price_usd"].isna().sum() > 0:
            print("FAILED: Null prices still present")
            return

        if (processed["price_usd"] == 0).sum() > 0:
            print("FAILED: Zero prices still present")
            return

        print(f"PASSED: {len(processed)} records, no null or zero prices")

    except Exception as e:
        print(f"FAILED: {e}")


def test_merge():
    print("Testing merge_all()...")

    try:
        weather_df = pd.read_csv(f"{DATA_DIR}/weather.csv")
        trends_df = pd.read_csv(f"{DATA_DIR}/trends.csv")
        airbnb_df = pd.read_csv(f"{DATA_DIR}/airbnb.csv")

        merged = merge_all(weather_df, trends_df, airbnb_df)

        if len(merged) == 0:
            print("FAILED: Empty merged dataframe")
            return

        if "price_usd" not in merged.columns:
            print("FAILED: Missing price_usd column")
            return

        if "tavg" not in merged.columns:
            print("FAILED: Missing tavg column")
            return

        print(f"PASSED: {len(merged)} records merged successfully")

    except Exception as e:
        print(f"FAILED: {e}")


def test_get_feature_importance():
    print("Testing get_feature_importance()...")

    try:
        merged = pd.read_csv(f"{DATA_DIR}/merged_skaneateles.csv")

        for listing_id in merged["airbnb_id"].unique():

            listing_df = merged[merged["airbnb_id"] == listing_id]

            if listing_df["price_usd"].std() > 0:
                result = get_feature_importance(merged, listing_id, feature_cols=FEATURE_COLS)

                if result is None:
                    print("FAILED: No result returned")
                    return

                if "r2" not in result:
                    print("FAILED: Missing r2 in result")
                    return

                print(f"PASSED: listing {listing_id}, R²={result['r2']:.3f}, MAE=${result['mae']:.2f}")
                break

    except Exception as e:
        print(f"FAILED: {e}")


if __name__ == "__main__":
    test_weather_data()
    test_trends_data()
    test_process_weather_data()
    test_process_airbnb_data()
    test_merge()
    test_get_feature_importance()