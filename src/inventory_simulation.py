import pandas as pd
import time
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

inventory_df = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))

# 🔥 CRITICAL FIX: Ensure stock column exists
if "current_stock" not in inventory_df.columns:
    inventory_df["current_stock"] = random.choices(
        range(50, 200), k=len(inventory_df)
    )

LOW_STOCK_THRESHOLD = 30

print("Starting Inventory Simulation (IoT-like updates)\n")

for cycle in range(1, 6):
    print(f"--- Update Cycle {cycle} ---")

    inventory_df["current_stock"] = inventory_df["current_stock"] - inventory_df["current_stock"].apply(
        lambda x: random.randint(0, 5)
    )

    inventory_df["current_stock"] = inventory_df["current_stock"].clip(lower=0)

    for _, row in inventory_df.iterrows():
        if row["current_stock"] <= LOW_STOCK_THRESHOLD:
            print(f"⚠️ Low Stock Alert: Product {row['product_id']} | Stock = {row['current_stock']}")

    print(inventory_df[["product_id", "current_stock"]])

    inventory_df[["product_id", "current_stock"]].to_csv(
        os.path.join(DATA_DIR, "inventory_status.csv"),
        index=False
    )

    time.sleep(1)
