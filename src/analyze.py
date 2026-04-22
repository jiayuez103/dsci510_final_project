import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from config import FEATURE_COLS, RESULTS_DIR, PLOT_SIZE

TARGET = "price_usd"

def get_feature_importance(merged_df, listing_id, feature_cols=FEATURE_COLS):
    """
    Use Random Forest to identify the most important features
    for predicting price changes in a single listing.
    """
    print(f"\nFeature Importance (Random Forest): {listing_id}")

    listing_df = merged_df[merged_df["airbnb_id"] == listing_id].copy()
    available_features = [f for f in feature_cols if f in listing_df.columns]
    listing_df = listing_df[available_features + [TARGET]].dropna()

    if listing_df[TARGET].std() == 0:
        print("Price is constant - skipping")
        return None

    # 1. Prepare data
    X = listing_df[available_features]
    y = listing_df[TARGET]

    # 2. Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Initialize and train the model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # 4. Make predictions
    predictions = rf_model.predict(X_test)

    # 5. Evaluate
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    if r2 < -1:
        print(f"R2 too negative ({r2:.3f}) - skipping")
        return None

    print(f"MAE: ${mae:.2f}")
    print(f"R2: {r2:.3f}")

    # Feature importance
    importance_df = pd.DataFrame({
        "feature": available_features,
        "importance": rf_model.feature_importances_
    }).sort_values("importance", ascending=False)

    print("\nFeature Importance:")
    print(importance_df.to_string(index=False))

    return {
        "listing_id": listing_id,
        "mae": mae,
        "r2": r2,
        "importance": importance_df
    }

def run_single_listing_model(merged_df, listing_id):
    """
    Run Linear Regression on a single Airbnb listing to test
    whether weather and calendar features can predict price changes.
    """
    print(f"\n--- Single Listing Model: {listing_id} ---")

    listing_df = merged_df[merged_df["airbnb_id"] == listing_id].copy()

    available_features = [f for f in FEATURE_COLS if f in listing_df.columns]
    listing_df = listing_df[available_features + [TARGET]].dropna()

    if listing_df[TARGET].std() == 0:
        print("Price is constant - skipping")
        return None

    # 1. Prepare data
    X = listing_df[available_features]
    y = listing_df[TARGET]
    print(f"Features: {available_features}")
    print(f"Price range: ${y.min():.2f} - ${y.max():.2f}, std: ${y.std():.2f}")

    # 2. Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 4. Make predictions
    predictions = model.predict(X_test)

    # 5. Evaluate
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"MAE: ${mae:.2f}")
    print(f"R2: {r2:.3f}")

    return {"listing_id": listing_id, "mae": mae, "r2": r2}

def normalize_prices(merged_df):
    """Normalize price relative to each listing's average"""
    merged_df = merged_df.copy()
    avg_prices = merged_df.groupby("airbnb_id")["price_usd"].transform("mean")
    merged_df["price_normalized"] = merged_df["price_usd"] / avg_prices
    return merged_df


def run_full_model(merged_df, feature_cols=FEATURE_COLS):
    print("\n=== Full Model (Normalized Prices) ===")

    df = normalize_prices(merged_df)

    available_features = [f for f in feature_cols if f in df.columns]
    df = df[available_features + ["price_normalized"]].dropna()

    X = df[available_features]
    y = df["price_normalized"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    predictions = rf_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"MAE: {mae:.4f}")
    print(f"R2: {r2:.3f}")

    importance_df = pd.DataFrame({
        "feature": available_features,
        "importance": rf_model.feature_importances_
    }).sort_values("importance", ascending=False)

    print("\nFeature Importance:")
    print(importance_df.to_string(index=False))

    return rf_model, importance_df, r2