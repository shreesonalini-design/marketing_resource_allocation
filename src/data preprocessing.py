import pandas as pd
import os

# Get project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_sales_data():
    return pd.read_csv(os.path.join(DATA_DIR, "sales_history.csv"))

def preprocess_sales_data(df):
    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort by product and date (important for time series)
    df = df.sort_values(by=["product_id", "date"])

    # Create rolling demand feature (3-day moving average)
    df["rolling_avg_demand"] = (
        df.groupby("product_id")["units_sold"]
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Lag feature (previous day demand)
    df["lag_1_demand"] = (
        df.groupby("product_id")["units_sold"]
        .shift(1)
        .fillna(0)
    )

    return df

if __name__ == "__main__":
    sales_df = load_sales_data()
    processed_df = preprocess_sales_data(sales_df)

    print("Preprocessed Sales Data:")
    print(processed_df.head(10))
