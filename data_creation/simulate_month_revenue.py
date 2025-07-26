import pandas as pd
import random
import os



# Load monthly churn data
df = pd.read_csv("Datasets/customer_churn_data.csv", parse_dates=["month"])

# Simulate daily date for each row (random day in that month)
df["date"] = df["month"].apply(lambda m: pd.to_datetime(
    f"{m.year}-{m.month}-{random.randint(1, 28)}"))

# Revenue per plan
revenue_map = {"Basic": 1000, "Pro": 3000, "Enterprise": 10000}
df["revenue"] = df["plan"].map(revenue_map)

# Mark first activity month for new signups
df["signup_month"] = df.groupby("customer_id")["month"].transform("min")
df["is_new_signup"] = df["month"] == df["signup_month"]

# Group by day and plan
daily_revenue = df.groupby(["date", "plan"]).agg(
    active_customers=("customer_id", "nunique"),
    churn_count=("churn", "sum"),
    new_signups=("is_new_signup", "sum"),
    daily_revenue=("revenue", "sum"),
    avg_usage_score=("usage_score", "mean")
).reset_index()

# Create full date range (365 days)
daily_dates = pd.date_range("2023-07-01", "2024-06-30")
plans = df["plan"].unique()

# Fill missing date-plan pairs with zeros
full_index = pd.MultiIndex.from_product([daily_dates, plans], names=["date", "plan"])
daily_revenue = daily_revenue.set_index(["date", "plan"]).reindex(full_index, fill_value=0).reset_index()

# Save
daily_revenue.to_csv("Datasets/daily_revenue_data.csv", index=False)
print("✅ daily_revenue_data.csv created.")
