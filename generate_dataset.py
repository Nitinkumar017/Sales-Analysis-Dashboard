"""
generate_dataset.py
-------------------
Generates a realistic, comprehensive sales dataset (sales_data.csv)
designed specifically for data analytics and visualization projects.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sales_data(filepath="sales_data.csv", num_records=850):
    # Set seed for reproducible results
    np.random.seed(42)
    random.seed(42)

    categories_products = {
        "Electronics": [
            ("Laptop Pro 15", 950.0),
            ("Smartphone X", 680.0),
            ("Wireless Earbuds", 89.0),
            ("4K Smart Monitor", 340.0),
            ("Gaming Mouse", 49.0),
            ("Smart Fitness Watch", 179.0)
        ],
        "Clothing": [
            ("Denim Jeans", 55.0),
            ("Cotton Crew T-Shirt", 24.0),
            ("Winter Hooded Jacket", 120.0),
            ("Formal Oxford Shirt", 48.0),
            ("Athletic Running Shoes", 85.0)
        ],
        "Furniture": [
            ("Ergonomic Office Chair", 230.0),
            ("Adjustable Standing Desk", 350.0),
            ("Wooden Bookshelf", 140.0),
            ("Modular 2-Seat Sofa", 520.0)
        ],
        "Food & Beverages": [
            ("Organic Coffee Roast 1kg", 26.0),
            ("Green Tea Herbal Box", 18.0),
            ("Gourmet Snack Basket", 38.0),
            ("Premium Dark Chocolate", 22.0)
        ],
        "Accessories": [
            ("Leather Travel Wallet", 42.0),
            ("Waterproof Laptop Backpack", 68.0),
            ("Insulated Thermal Flask", 28.0),
            ("Polarized Sunglasses", 64.0)
        ]
    }

    regions = ["North", "South", "East", "West"]
    segments = ["Consumer", "Corporate", "Home Office"]

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days

    records = []

    # Flatten products with categories
    catalog = []
    for cat, prod_list in categories_products.items():
        for prod_name, base_price in prod_list:
            catalog.append((cat, prod_name, base_price))

    # Monthly weights to simulate realistic sales seasonality (Q4 boost, summer boost)
    month_weights = [0.7, 0.75, 0.85, 0.9, 0.95, 1.05, 1.15, 1.0, 1.05, 1.25, 1.45, 1.6]

    for _ in range(num_records):
        # Pick random day weighted slightly towards end of year
        day_offset = random.randint(0, total_days)
        record_date = start_date + timedelta(days=day_offset)
        month_idx = record_date.month - 1
        
        # Decide if this day gets sampled based on monthly seasonality
        if random.random() > (month_weights[month_idx] / 1.8):
            # Pick another day in higher volume months occasionally
            if random.random() < 0.4:
                record_date = datetime(2024, random.choice([10, 11, 12]), random.randint(1, 28))

        cat, prod_name, base_price = random.choice(catalog)
        region = random.choice(regions)
        segment = random.choice(segments)

        # Quantity between 1 and 12, weighted towards 1-4
        quantity = int(np.random.choice([1, 2, 3, 4, 5, 6, 8, 10, 12], p=[0.35, 0.25, 0.15, 0.10, 0.05, 0.04, 0.03, 0.02, 0.01]))

        # Slight price fluctuation (+/- 5%) to simulate realistic discounts/taxes
        price_variation = np.round(base_price * (1.0 + np.random.uniform(-0.05, 0.05)), 2)
        sales_revenue = np.round(quantity * price_variation, 2)

        records.append({
            "Date": record_date.strftime("%Y-%m-%d"),
            "Product": prod_name,
            "Product Category": cat,
            "Region": region,
            "Quantity": quantity,
            "Unit Price": price_variation,
            "Sales Revenue": sales_revenue,
            "Customer Segment": segment
        })

    df = pd.DataFrame(records)

    # Sort chronologically
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date").reset_index(drop=True)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    # Inject a few intentional "dirty" records to demonstrate data cleaning during viva
    # 1. Duplicate rows (3 rows)
    duplicates = df.iloc[10:13].copy()
    
    # 2. Rows with missing/NaN values
    dirty_row_1 = {
        "Date": "2024-06-15",
        "Product": "Laptop Pro 15",
        "Product Category": "Electronics",
        "Region": np.nan,  # Missing region
        "Quantity": 2,
        "Unit Price": 950.0,
        "Sales Revenue": 1900.0,
        "Customer Segment": "Consumer"
    }
    
    dirty_row_2 = {
        "Date": "2024-07-20",
        "Product": "Cotton Crew T-Shirt",
        "Product Category": "  Clothing  ",  # Extra whitespace
        "Region": "South",
        "Quantity": np.nan,  # Missing quantity
        "Unit Price": 24.0,
        "Sales Revenue": np.nan,
        "Customer Segment": "Consumer"
    }

    # Append dirty data
    df = pd.concat([df, duplicates, pd.DataFrame([dirty_row_1, dirty_row_2])], ignore_index=True)

    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"Generated realistic sales dataset with {len(df)} records at '{filepath}'.")
    return df

if __name__ == "__main__":
    generate_sales_data()
