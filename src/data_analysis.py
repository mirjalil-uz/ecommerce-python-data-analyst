"""
E-Commerce Sales & Customer Analysis
Data Analyst portfolio project — see README.md for the full write-up.

Run this from anywhere (VS Code "Run" button, a terminal at the repo root,
or `cd src && python data_analysis.py`) — paths are resolved relative to
this file's own location, not the current working directory.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Paths -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ecommerce_sales.csv"
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)  # matplotlib won't create this for us

# --- Load ---------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df["order_date"] = pd.to_datetime(df["order_date"])

# --- Cleaning -------------------------------------------------------------
before = len(df)
df = df.drop_duplicates().copy()
duplicates_removed = before - len(df)

df["region"] = df["region"].fillna(df["region"].mode()[0])
df["discount"] = df["discount"].fillna(df["discount"].median())

# Orders with no customer_id can't be tied to a real customer. We keep them
# in revenue/profit totals (the sale still happened) but exclude them from
# customer-level rankings — otherwise every anonymous order gets lumped into
# one fake "UNKNOWN" customer who then looks like your #1 account.
df["customer_id"] = df["customer_id"].fillna("UNKNOWN")
known_customers = df[df["customer_id"] != "UNKNOWN"].copy()
missing_customer_orders = int((df["customer_id"] == "UNKNOWN").sum())

print(f"Duplicate rows removed: {duplicates_removed}")
print(f"Orders with missing customer_id (kept in totals, excluded from "
      f"customer ranking): {missing_customer_orders}")

# --- Feature engineering -------------------------------------------------
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["profit_margin"] = np.where(df["revenue"] != 0, df["profit"] / df["revenue"], 0)

# --- KPI summary -------------------------------------------------------
kpis = pd.Series({
    "Revenue": df["revenue"].sum(),
    "Profit": df["profit"].sum(),
    "Profit Margin": df["profit"].sum() / df["revenue"].sum(),
    "Orders": df["order_id"].nunique(),
    "Known Customers": known_customers["customer_id"].nunique(),
    "Average Order Value": df["revenue"].sum() / df["order_id"].nunique(),
})
print("\nKPI Summary:\n", kpis)

# --- Monthly performance -------------------------------------------------
monthly = df.groupby("month", as_index=False).agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
)

# --- Category performance -------------------------------------------------
category = df.groupby("category", as_index=False).agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    units=("quantity", "sum"),
)
category["profit_margin"] = category["profit"] / category["revenue"]
category = category.sort_values("revenue", ascending=False)

# --- Regional performance -------------------------------------------------
regional = df.groupby("region", as_index=False).agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
)
regional["profit_margin"] = regional["profit"] / regional["revenue"]
regional = regional.sort_values("profit", ascending=False)

# --- Customer value (known customers only) --------------------------------
customers = (
    known_customers.groupby("customer_id", as_index=False)
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
    .sort_values("revenue", ascending=False)
)

# --- Discount vs. profitability -------------------------------------------
discount_bins = pd.cut(
    df["discount"],
    bins=[-0.001, 0.05, 0.10, 0.15, 0.20, 0.35],
    labels=["0-5%", "5-10%", "10-15%", "15-20%", "20%+"],
)
discount_analysis = (
    df.assign(discount_band=discount_bins)
    .groupby("discount_band", observed=False)
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    .reset_index()
)
discount_analysis["profit_margin"] = discount_analysis["profit"] / discount_analysis["revenue"]

# --- Product-level margin review -------------------------------------------
product = df.groupby(["category", "product"], as_index=False).agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    units=("quantity", "sum"),
)
product["profit_margin"] = product["profit"] / product["revenue"]
lowest_margin_products = product.sort_values("profit_margin").head(5)

print("\nCategory performance:\n", category)
print("\nTop 10 customers (known customers only):\n", customers.head(10))
print("\nProfit margin by discount band:\n", discount_analysis)
print("\nLowest-margin products (candidates for pricing/cost review):\n", lowest_margin_products)

# --- Visuals -------------------------------------------------------------
sns.set_theme(style="whitegrid")

plt.figure(figsize=(11, 5))
sns.lineplot(data=monthly, x="month", y="revenue", marker="o")
plt.xticks(rotation=60)
plt.title("Monthly Revenue Trend")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "monthly_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
sns.barplot(data=category, x="revenue", y="category")
plt.title("Revenue by Product Category")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "category_revenue.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
sns.barplot(data=regional, x="profit", y="region")
plt.title("Profit by Region")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "regional_profit.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
sns.barplot(data=discount_analysis, x="discount_band", y="profit_margin")
plt.title("Profit Margin by Discount Band")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "discount_profit_margin.png", dpi=160)
plt.close()

print(f"\nCharts saved to: {IMAGES_DIR}")
