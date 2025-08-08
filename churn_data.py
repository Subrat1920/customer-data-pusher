import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv

# config / seeding
load_dotenv()
fake = Faker()
random.seed(42)
np.random.seed(42)

# DB helper
def get_db_url():
    url = os.getenv("CONNECTION_URL")
    if not url:
        raise ValueError("CONNECTION_URL not set in environment (.env).")
    return url

def generate_single_customer():
    """Generate one synthetic customer row using the same logic as your original script."""
    # sample base attributes
    tenure = int(np.random.randint(1, 60))                 # months
    age = int(np.random.randint(18, 70))
    gender = random.choice(['Male', 'Female'])
    location = random.choice(['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai'])
    segment = np.random.choice(['Basic', 'Premium', 'Enterprise'], p=[0.6, 0.3, 0.1])
    subscription_type = np.random.choice(['Monthly', 'Yearly', 'Freemium'], p=[0.5, 0.4, 0.1])
    contract_type = random.choice(['Month-to-Month', 'Annual'])
    payment_method = random.choice(['Credit Card', 'Debit Card', 'UPI', 'Net Banking'])
    auto_renew = bool(np.random.choice([True, False]))

    # engagement metrics
    logins = int(min(30, np.random.poisson(tenure / 3)))
    max_days_ago = max(0, 30 - logins)
    days_ago = random.randint(0, max_days_ago)
    last_login = (datetime.today() - timedelta(days=days_ago)).date()

    session_time = float(max(1, round(np.random.normal(15 + 5*(segment == 'Premium') + 10*(segment == 'Enterprise'), 5), 2)))
    feature_use = int(np.random.poisson(5 + int(segment == 'Premium')*2 + int(segment == 'Enterprise')*3))
    support_tickets = int(np.random.poisson(2 if segment == 'Basic' else 1))
    monthly_spend = float(max(100, round(np.random.normal(500 + 300*(segment == 'Premium') + 700*(segment == 'Enterprise'), 100), 2)))
    payment_fails = int(np.random.binomial(2, 0.1 if auto_renew else 0.3))
    refunds = int(np.random.binomial(1, 0.05 if segment != 'Basic' else 0.15))
    lifetime_value = round(monthly_spend * tenure, 2)
    used_discount_recently = int(np.random.rand() < (0.3 if segment == 'Basic' else 0.1))

    # churn logic (same as original)
    churn_score = (
        (tenure < 12) * 2 +
        (logins < 5) * 2 +
        (payment_fails > 0) * 2 +
        (session_time < 10) +
        (feature_use < 3) +
        (support_tickets > 3)
    )
    churn = 1 if churn_score >= 4 else 0

    # create reasonably-unique customer_id for daily inserts
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")  # high-res timestamp
    customer_id = f"CUST{random.randint(100,9999)}"

    return [
        customer_id, tenure, age, gender, location, segment, subscription_type,
        contract_type, payment_method, auto_renew, logins, last_login, session_time,
        feature_use, support_tickets, monthly_spend, payment_fails, refunds,
        lifetime_value, used_discount_recently, churn
    ]

def append_daily_churn_rows():
    rows_to_generate = random.randint(3, 4)  # 3-4 rows per run
    records = [generate_single_customer() for _ in range(rows_to_generate)]

    cols = [
        "customer_id", "tenure_months", "age", "gender", "location", "segment", "subscription_type",
        "contract_type", "payment_method", "auto_renew", "login_days_last_30", "last_login_date",
        "avg_session_duration", "feature_usage_count", "support_tickets_last_3mo",
        "monthly_spend", "payment_failures", "refund_requests", "lifetime_value",
        "used_discount_recently", "churn"
    ]

    df = pd.DataFrame(records, columns=cols)
    df["churn"] = df["churn"].astype(int)

    engine = create_engine(get_db_url())
    df.to_sql('customer_churn_data', con=engine, if_exists='append', index=False)
    print(f"{len(df)} rows appended to 'customer_churn_data'.")

if __name__ == "__main__":
    append_daily_churn_rows()



## subratmishra1sep@gmail.com, 2subratmishra1sep@gmail.com, subuking001@gmail.com, 22mca053.subratmishra@giet.edu, 22mca053.subratmishra@gmail.com, subu2459@gmail.com, prjctreview@gmail.com, sumu12321@gmail.com, photosubratmishra@gmail.com