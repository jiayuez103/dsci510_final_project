# include your tests here
from load import get_weather_data, get_trends_data


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


if __name__ == "__main__":
    test_weather_data()
    test_trends_data()
# for example for your Progress report you should be able to load data from at least one API source.
