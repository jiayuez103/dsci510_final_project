# include your tests here
from load import get_weather_data, get_trends_data
from process import process_weather_data, process_airbnb_data
import pandas as pd
from config import DATA_DIR


def test_weather_data():
    print("Testing get_weather_data()...")
    try:
        df = get_weather_data()

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
        print(f"FAILED: {e}")

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


if __name__ == "__main__":
    test_weather_data()
    test_trends_data()
    test_process_weather_data()
    test_process_airbnb_data()
# for example for your Progress report you should be able to load data from at least one API source.
