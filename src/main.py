import os
import argparse
import joblib
import pandas as pd
from config import DATA_DIR, RESULTS_DIR, FEATURE_COLS, FEATURE_COLS_CANANDAIGUA
from process import merge_all
from analyze import get_feature_importance, run_full_model, normalize_prices
from sklearn.metrics import mean_absolute_error, r2_score


def train():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Skaneateles Lake
    print("\nTraining Model for Skaneateles Lake listings")
    weather_df = pd.read_csv(f"{DATA_DIR}/weather.csv")
    trends_df = pd.read_csv(f"{DATA_DIR}/trends.csv")
    airbnb_df = pd.read_csv(f"{DATA_DIR}/airbnb.csv")

    merged_df = merge_all(weather_df, trends_df, airbnb_df)
    merged_df.to_csv(f"{DATA_DIR}/merged_skaneateles.csv", index=False)
    print(f"Merged: {len(merged_df)} records")

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
    print("\n Training Model for Canandaigua Lake listings")
    weather_canandaigua_df = pd.read_csv(f"{DATA_DIR}/weather_canandaigua.csv")
    trends_canandaigua_df = pd.read_csv(f"{DATA_DIR}/trends_canandaigua.csv")
    airbnb_canandaigua_df = pd.read_csv(f"{DATA_DIR}/airbnb_canandaigua.csv")

    merged_canandaigua_df = merge_all(weather_canandaigua_df, trends_canandaigua_df, airbnb_canandaigua_df)
    merged_canandaigua_df.to_csv(f"{DATA_DIR}/merged_canandaigua.csv", index=False)
    print(f"Merged: {len(merged_canandaigua_df)} records")

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

    print("\nDone.")


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

    args = parser.parse_args()

    if args.train:
        train()
    elif args.evaluation:
        if args.region == "canandaigua":
            evaluate(model_link=args.model_link, region=args.region,
                     feature_cols=FEATURE_COLS_CANANDAIGUA)
        else:
            evaluate(model_link=args.model_link, region=args.region)
    else:
        print("Please specify --train or --evaluation")
