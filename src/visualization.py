import pandas as pd
import matplotlib.pyplot as plt
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Load final allocation output
df = pd.read_csv(os.path.join(DATA_DIR, "marketing_allocation_output.csv"))

# ---------------- PROMOTION PERCENTAGE ----------------
plt.figure()
plt.bar(df["product_id"], df["promotion_percentage"])
plt.title("Promotion Percentage per Product")
plt.xlabel("Product ID")
plt.ylabel("Promotion Percentage (%)")
plt.tight_layout()
plt.show()

# ---------------- MANPOWER REQUIRED ----------------
plt.figure()
plt.bar(df["product_id"], df["manpower_required"])
plt.title("Manpower Allocation per Product")
plt.xlabel("Product ID")
plt.ylabel("Number of Staff")
plt.tight_layout()
plt.show()

# ---------------- MARKETING CHANNELS ----------------
channel_counts = df["marketing_channels"].value_counts()

plt.figure()
plt.bar(channel_counts.index, channel_counts.values)
plt.title("Marketing Channel Distribution")
plt.xlabel("Marketing Channel")
plt.ylabel("Number of Products")
plt.xticks(rotation=15)

plt.tight_layout()
plt.show()
