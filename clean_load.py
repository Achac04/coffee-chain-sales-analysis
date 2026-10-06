import sqlite3
import pandas as pd

sales = pd.read_csv("data/sales_raw.csv", parse_dates=["order_date"])
stores = pd.read_csv("data/stores.csv")
products = pd.read_csv("data/products.csv")

# 1. Inspect
print(sales.info())
print(sales.isna().sum())          # how many nulls per column
print(sales.duplicated().sum())    # how many duplicate rows

# 2. Clean
sales = sales.drop_duplicates()
sales = sales.dropna(subset=["quantity"])
sales["quantity"] = sales["quantity"].astype(int)
print("Clean rows:", len(sales))   # expect about 19,960

# 3. Quick exploration
merged = sales.merge(products, on="product_id").merge(stores, on="store_id")
merged["revenue"] = merged["quantity"] * merged["price"] * (1 - merged["discount"])
print(merged["revenue"].describe())
print(merged.groupby("category")["revenue"].sum().sort_values(ascending=False))

# 4. Chart
import matplotlib.pyplot as plt
merged.groupby(merged["order_date"].dt.month)["revenue"].sum().plot(kind="bar", title="Revenue by month")
plt.savefig("revenue_by_month.png")

# 5. Load into SQLite for the SQL part
conn = sqlite3.connect("coffee.db")
sales.to_sql("sales", conn, if_exists="replace", index=False)
stores.to_sql("stores", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
conn.close()