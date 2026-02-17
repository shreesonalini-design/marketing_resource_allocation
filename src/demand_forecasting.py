import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# -----------------------------
# Path handling
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# -----------------------------
# Load and preprocess data
# -----------------------------
def load_processed_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "sales_history.csv"))
    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(by=["product_id", "date"])

    df["rolling_avg_demand"] = (
        df.groupby("product_id")["units_sold"]
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["lag_1_demand"] = (
        df.groupby("product_id")["units_sold"]
        .shift(1)
        .fillna(0)
    )

    return df

# -----------------------------
# Train demand forecasting model
# -----------------------------
def train_demand_model(df):
    features = ["rolling_avg_demand", "lag_1_demand", "promotion"]
    X = df[features]
    y = df["units_sold"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    return model, mae, rmse

# -----------------------------
# Generate demand predictions
# -----------------------------
def generate_demand_predictions(df, model):
    features = ["rolling_avg_demand", "lag_1_demand", "promotion"]

    df["predicted_demand"] = model.predict(df[features])

    latest_predictions = (
        df.sort_values("date")
        .groupby("product_id")
        .tail(1)[["product_id", "predicted_demand"]]
    )

    output_path = os.path.join(DATA_DIR, "demand_predictions.csv")
    latest_predictions.to_csv(output_path, index=False)

    print("Demand predictions saved to data/demand_predictions.csv")

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    data = load_processed_data()

    model, mae, rmse = train_demand_model(data)

    print("Demand Forecasting Model Performance:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

    generate_demand_predictions(data, model)
