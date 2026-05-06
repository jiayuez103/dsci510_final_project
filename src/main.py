import os
import argparse
import joblib
import pandas as pd
import time
from config import DATA_DIR, RESULTS_DIR, FEATURE_COLS, FEATURE_COLS_CANANDAIGUA
from load import get_weather_data, get_trends_data, get_airbnb_data
from config import (
    SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ALT, SKANEATELES_ZIP,
    CANANDAIGUA_LAT, CANANDAIGUA_LON, CANANDAIGUA_ALT, CANANDAIGUA_ZIP,
    TRENDS_KEYWORDS, TRENDS_KEYWORDS_CANANDAIGUA
    )
from process import merge_all
from analyze import get_feature_importance, run_full_model, normalize_prices
from sklearn.metrics import mean_absolute_error, r2_score


def train(data_link_skaneateles=None, data_link_canandaigua=None):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if data_link_skaneateles and data_link_canandaigua:
        import urllib.request
        print("Downloading pre-collected data from Google Drive")
        urllib.request.urlretrieve(data_link_skaneateles, f"{DATA_DIR}/merged_skaneateles.csv")
        urllib.request.urlretrieve(data_link_canandaigua, f"{DATA_DIR}/merged_canandaigua.csv")
        print("Data downloaded successfully!")

    else:
        print("\nCollecting Skaneateles data from original sources")
        weather_df = get_weather_data(SKANEATELES_LAT, SKANEATELES_LON, SKANEATELES_ALT)
        weather_df.to_csv(f"{DATA_DIR}/weather.csv", index=False)

        trends_df = get_trends_data(keywords=TRENDS_KEYWORDS)
        trends_df.to_csv(f"{DATA_DIR}/trends.csv", index=False)

        all_dfs = []
        for offset in [0, 50, 100]:
            print(f"\nFetching Skaneateles listings offset={offset}")
            df = get_airbnb_data(zipcode=SKANEATELES_ZIP, offset=offset, max_listings=50)
            if df is not None and len(df) > 0:
                all_dfs.append(df)
            time.sleep(2)  # AI generated: avoid rate limiting

        airbnb_df = pd.concat(all_dfs, ignore_index=True)
        airbnb_df.to_csv(f"{DATA_DIR}/airbnb.csv", index=False)

        print("\nCollecting Canandaigua data from original sources")
        weather_canandaigua_df = get_weather_data(CANANDAIGUA_LAT, CANANDAIGUA_LON, CANANDAIGUA_ALT)
        weather_canandaigua_df.to_csv(f"{DATA_DIR}/weather_canandaigua.csv", index=False)

        trends_canandaigua_df = get_trends_data(keywords=TRENDS_KEYWORDS_CANANDAIGUA)
        trends_canandaigua_df.to_csv(f"{DATA_DIR}/trends_canandaigua.csv", index=False)

        all_dfs = []
        for offset in [0, 50, 100, 150, 200, 250]:
            df = get_airbnb_data(zipcode=CANANDAIGUA_ZIP, offset=offset, max_listings=50)
            if df is not None and len(df) > 0:
                all_dfs.append(df)
            time.sleep(2)
        airbnb_canandaigua_df = pd.concat(all_dfs, ignore_index=True)
        airbnb_canandaigua_df.to_csv(f"{DATA_DIR}/airbnb_canandaigua.csv", index=False)

        merged_df = merge_all(weather_df, trends_df, airbnb_df)
        merged_df.to_csv(f"{DATA_DIR}/merged_skaneateles.csv", index=False)

        merged_canandaigua_df = merge_all(weather_canandaigua_df, trends_canandaigua_df, airbnb_canandaigua_df)
        merged_canandaigua_df.to_csv(f"{DATA_DIR}/merged_canandaigua.csv", index=False)

    # Skaneateles Lake
    print("\nTraining Model for Skaneateles Lake listings")
    merged_df = pd.read_csv(f"{DATA_DIR}/merged_skaneateles.csv")
    print(f"Merged {len(merged_df)} records")

    #single listing
    rf_results = []
    for listing_id in merged_df["airbnb_id"].unique():
        result = get_feature_importance(merged_df, listing_id)
        if result is not None:
            rf_results.append(result)

    rf_summary = pd.DataFrame(rf_results)[["listing_id", "mae", "r2"]]
    rf_summary.to_csv(f"{RESULTS_DIR}/rf_results_skaneateles.csv", index=False)
    print(f"Skaneateles Mean R²: {rf_summary['r2'].mean():.3f}")
    print(f"Skaneateles Median R²: {rf_summary['r2'].median():.3f}")

    # full model with normalized price
    rf_model_sk, importance_sk, r2_sk = run_full_model(merged_df, feature_cols=FEATURE_COLS)
    importance_sk.to_csv(f"{RESULTS_DIR}/full_model_importance_skaneateles.csv", index=False)
    joblib.dump(rf_model_sk, f"{RESULTS_DIR}/rf_model_skaneateles.pkl")

    # Canandaigua Lake
    print("\nTraining Model for Canandaigua Lake listings")
    merged_canandaigua_df = pd.read_csv(f"{DATA_DIR}/merged_canandaigua.csv")
    print(f"Merged {len(merged_canandaigua_df)} records")

    #single listing
    rf_results_canandaigua = []
    for listing_id in merged_canandaigua_df["airbnb_id"].unique():
        result = get_feature_importance(merged_canandaigua_df, listing_id, feature_cols=FEATURE_COLS_CANANDAIGUA)
        if result is not None:
            rf_results_canandaigua.append(result)

    rf_summary_canandaigua = pd.DataFrame(rf_results_canandaigua)[["listing_id", "mae", "r2"]]
    rf_summary_canandaigua.to_csv(f"{RESULTS_DIR}/rf_results_canandaigua.csv", index=False)
    print(f"Canandaigua Mean R²: {rf_summary_canandaigua['r2'].mean():.3f}")
    print(f"Canandaigua Median R²: {rf_summary_canandaigua['r2'].median():.3f}")

    #full model with normalized price
    rf_model_ca, importance_ca, r2_ca = run_full_model(merged_canandaigua_df, feature_cols=FEATURE_COLS_CANANDAIGUA)
    importance_ca.to_csv(f"{RESULTS_DIR}/full_model_importance_canandaigua.csv", index=False)
    joblib.dump(rf_model_ca, f"{RESULTS_DIR}/rf_model_canandaigua.pkl")

    print("\nModel Training Done.")


def evaluate(model_link=None, feature_cols=FEATURE_COLS, region="skaneateles"):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # AI generated: download model from Google Drive if link provided
    if model_link:
        import urllib.request
        urllib.request.urlretrieve(model_link, f"{RESULTS_DIR}/rf_model_{region}.pkl")
        print(f"Model downloaded from {model_link}")
    # AI generated end

    rf_model = joblib.load(f"{RESULTS_DIR}/rf_model_{region}.pkl")

    merged_df = pd.read_csv(f"{DATA_DIR}/merged_{region}.csv")


    print(f"\n--- Per-Listing Evaluation ({region}) ---")
    rf_results = []
    for listing_id in merged_df["airbnb_id"].unique():
        result = get_feature_importance(merged_df, listing_id, feature_cols=feature_cols)
        if result is not None:
            rf_results.append(result)

    rf_summary = pd.DataFrame(rf_results)[["listing_id", "mae", "r2"]]
    print(f"Mean R²: {rf_summary['r2'].mean():.3f}")
    print(f"Median R²: {rf_summary['r2'].median():.3f}")
    rf_summary.to_csv(f"{RESULTS_DIR}/eval_results_{region}.csv", index=False)
    print(f"Results saved to results/eval_results_{region}.csv")


    df = normalize_prices(merged_df)
    available_features = [f for f in feature_cols if f in df.columns]
    df = df[available_features + ["price_normalized"]].dropna()

    X = df[available_features]
    y = df["price_normalized"]

    predictions = rf_model.predict(X)
    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)
    print(f"\nEvaluation Results:")
    print(f"MAE: {mae:.4f}")
    print(f"R2: {r2:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluation", action="store_true")
    parser.add_argument("--model_link", type=str, default=None)
    parser.add_argument("--region", type=str, default="skaneateles")
    parser.add_argument("--data_link_skaneateles", type=str, default=None)
    parser.add_argument("--data_link_canandaigua", type=str, default=None)

    args = parser.parse_args()

    if args.train:
        train(
            data_link_skaneateles=args.data_link_skaneateles,
            data_link_canandaigua=args.data_link_canandaigua
        )
    elif args.evaluation:
        if args.region == "canandaigua":
            evaluate(model_link=args.model_link, region=args.region,
                     feature_cols=FEATURE_COLS_CANANDAIGUA)
        else:
            evaluate(model_link=args.model_link, region=args.region)
    else:
        print("Please specify --train or --evaluation")
