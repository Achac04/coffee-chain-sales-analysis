import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed = same data every run

# --- Stores (20 stores in 6 cities) ---
cities = ["Calgary", "Edmonton", "Vancouver", "Toronto", "Winnipeg", "Montreal"]
stores = pd.DataFrame({
    "store_id": range(1, 21),
    "city": rng.choice(cities, 20),
})
stores["store_name"] = "Store " + stores["store_id"].astype(str)

# --- Products (12 items) ---
products = pd.DataFrame({
    "product_id": range(1, 13),
    "product_name": ["Latte", "Cappuccino", "Americano", "Cold Brew", "Frappuccino",
                     "Green Tea", "Chai Latte", "Croissant", "Muffin", "Bagel",
                     "Cookie", "Sandwich"],
    "category": ["Coffee"]*5 + ["Tea"]*2 + ["Food"]*5,
    "price": [5.25, 4.95, 3.75, 4.95, 6.25, 3.95, 5.45, 3.95, 3.50, 3.25, 2.95, 7.50],
})

# --- Sales (20,000 rows over 2025) ---
n = 20000
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
sales = pd.DataFrame({
    "order_id": range(1, n + 1),
    "order_date": dates,
    "store_id": rng.integers(1, 21, n),
    "product_id": rng.choice(range(1, 13), n, p=[.18,.12,.10,.10,.10,.05,.07,.08,.06,.05,.05,.04]),
    "quantity": rng.integers(1, 4, n),
    "discount": rng.choice([0, 0.1, 0.2], n, p=[.7, .2, .1]),
})

# --- Make the data messy on purpose (so you can practice cleaning) ---
sales.loc[rng.choice(n, 40, replace=False), "quantity"] = np.nan          # missing values
sales = pd.concat([sales, sales.sample(60, random_state=1)])                # duplicate rows

stores.to_csv("data/stores.csv", index=False)
products.to_csv("data/products.csv", index=False)
sales.to_csv("data/sales_raw.csv", index=False)
print("Done:", len(sales), "raw sales rows")