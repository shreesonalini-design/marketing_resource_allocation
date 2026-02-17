import pandas as pd
import os

# Get absolute path of current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

def load_products():
    return pd.read_csv(os.path.join(DATA_DIR, "products.csv"))

def load_inventory():
    return pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))

def load_sales():
    return pd.read_csv(os.path.join(DATA_DIR, "sales_history.csv"))

if __name__ == "__main__":
    products = load_products()
    inventory = load_inventory()
    sales = load_sales()

    print("Products Data:")
    print(products.head(), "\n")

    print("Inventory Data:")
    print(inventory.head(), "\n")

    print("Sales History Data:")
    print(sales.head())
