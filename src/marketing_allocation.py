import pandas as pd
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load data
inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory_status.csv"))
demand = pd.read_csv(os.path.join(DATA_DIR, "demand_predictions.csv"))

# Merge inventory and demand
df = pd.merge(inventory, demand, on="product_id")

LOW_STOCK_THRESHOLD = 30

# ---------------- PROMOTION PERCENTAGE ----------------
def calculate_promotion_percentage(row):
    demand = row["predicted_demand"]
    stock = row["current_stock"]

    if stock <= LOW_STOCK_THRESHOLD:
        return 0
    elif demand >= 60 and stock >= 100:
        return 70
    elif demand >= 60 and stock < 100:
        return 40
    elif demand < 60 and stock >= 100:
        return 50
    else:
        return 20

# ---------------- MANPOWER ALLOCATION ----------------
def recommend_manpower(promo_percent):
    if promo_percent == 0:
        return 0
    elif promo_percent <= 25:
        return 1
    elif promo_percent <= 50:
        return 2
    elif promo_percent <= 70:
        return 3
    else:
        return 4

# ---------------- MARKETING CHANNELS ----------------
def recommend_channels(promo_percent):
    if promo_percent == 0:
        return "NO PROMOTION"
    elif promo_percent <= 25:
        return "Email"
    elif promo_percent <= 50:
        return "Email, Social Media"
    elif promo_percent <= 70:
        return "Social Media, Online Ads"
    else:
        return "Online Ads, Field Marketing"

# Apply logic
df["promotion_percentage"] = df.apply(calculate_promotion_percentage, axis=1)
df["manpower_required"] = df["promotion_percentage"].apply(recommend_manpower)
df["marketing_channels"] = df["promotion_percentage"].apply(recommend_channels)

# Final output
print("\nEnhanced Marketing Resource Allocation:")
print(df)

# Save output
output_path = os.path.join(DATA_DIR, "marketing_allocation_output.csv")
df.to_csv(output_path, index=False)

print("\nMarketing allocation saved to data/marketing_allocation_output.csv")

