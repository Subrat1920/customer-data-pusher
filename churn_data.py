# import os
# import random
# import numpy as np
# import pandas as pd
# from datetime import datetime
# from faker import Faker
# from sqlalchemy import create_engine
# from dotenv import load_dotenv

# load_dotenv()
# fake = Faker()
# np.random.seed(42)
# random.seed(42)

# NUM_CUSTOMERS = 5000
# PLANS = ["Basic", "Pro", "Enterprise"]



# def get_db_url():
#     return os.getenv("CONNECTION_URL")

# def generate_and_append_data():
#     today = datetime.today().date()
#     rows_to_generate = random.randint(3, 5)
#     new_rows = []

#     for _ in range(rows_to_generate):
#         customer_id = random.randint(1, NUM_CUSTOMERS)
#         usage_score = np.clip(np.random.normal(loc=70, scale=20), 0, 100)
#         login_frequency = np.random.randint(1, 30)
#         active_days = np.random.randint(5, 28)
#         feature_adoption_score = np.clip(np.random.normal(usage_score * 0.8, 10), 0, 100)
#         support_tickets = np.random.poisson(0.8)
#         payment_issue = int(np.random.rand() < 0.05)
#         marketing_engaged = int(np.random.rand() < 0.2)
#         plan = random.choices(PLANS, weights=[0.5, 0.3, 0.2])[0]
#         downgraded = int(np.random.rand() < 0.05)
#         discount_applied = int(np.random.rand() < 0.1)
#         last_engaged_day = np.random.randint(1, 31)
#         avg_session_duration = round(np.random.normal(15, 5), 2)

#         churn_prob = (
#             0.05
#             + 0.2 * (usage_score < 40)
#             + 0.1 * (support_tickets > 2)
#             + 0.1 * payment_issue
#             + 0.05 * (login_frequency < 5)
#         )
#         churn = int(np.random.rand() < churn_prob)

#         new_rows.append([
#             customer_id, today, usage_score, login_frequency, active_days,
#             feature_adoption_score, support_tickets, payment_issue,
#             marketing_engaged, plan, downgraded, discount_applied,
#             last_engaged_day, avg_session_duration, churn
#         ])

#     df = pd.DataFrame(new_rows, columns=[
#         "customer_id", "date", "usage_score", "login_frequency", "active_days",
#         "feature_adoption_score", "support_tickets", "payment_issue",
#         "marketing_engaged", "plan", "downgraded", "discount_applied",
#         "last_engaged_day", "avg_session_duration", "churn"
#     ])

#     engine = create_engine(get_db_url())
#     df.to_sql('churn_data', con=engine, if_exists='append', index=False)
#     print(f"✅ {len(df)} churn rows inserted for {today}.")

# if __name__ == "__main__":
#     generate_and_append_data()



import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env variables and setup Faker
load_dotenv()
fake = Faker()
random.seed(42)
np.random.seed(42)

# Number of customers to generate
N_CUSTOMERS = 1000

# DB connection
def get_db_url():
    return os.getenv("CONNECTION_URL")

def append_churn_rows():
    # Base attributes
    customer_ids = [f"CUST{1000+i}" for i in range(N_CUSTOMERS)]
    tenure_months = np.random.randint(1, 60, N_CUSTOMERS)
    ages = np.random.randint(18, 70, N_CUSTOMERS)
    genders = np.random.choice(['Male', 'Female'], N_CUSTOMERS)
    locations = np.random.choice(['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai'], N_CUSTOMERS)
    segments = np.random.choice(['Basic', 'Premium', 'Enterprise'], N_CUSTOMERS, p=[0.6, 0.3, 0.1])
    subscription_types = np.random.choice(['Monthly', 'Yearly', 'Freemium'], N_CUSTOMERS, p=[0.5, 0.4, 0.1])
    contract_types = np.random.choice(['Month-to-Month', 'Annual'], N_CUSTOMERS)
    payment_methods = np.random.choice(['Credit Card', 'Debit Card', 'UPI', 'Net Banking'], N_CUSTOMERS)
    auto_renew = np.random.choice([True, False], N_CUSTOMERS)

    # Generate rows
    records = []
    for i in range(N_CUSTOMERS):
        seg = segments[i]
        tenure = tenure_months[i]
        sub_type = subscription_types[i]
        renew = auto_renew[i]

        logins = min(30, np.random.poisson(tenure / 3))
        max_days_ago = max(1, 30 - logins)
        last_login = datetime.today() - timedelta(days=random.randint(0, max_days_ago))

        session_time = max(1, round(np.random.normal(15 + 5*(seg == 'Premium') + 10*(seg == 'Enterprise'), 5), 2))
        feature_use = np.random.poisson(5 + (seg == 'Premium')*2 + (seg == 'Enterprise')*3)
        support_tickets = np.random.poisson(2 if seg == 'Basic' else 1)
        spend = max(100, round(np.random.normal(500 + 300*(seg == 'Premium') + 700*(seg == 'Enterprise'), 100), 2))
        payment_fails = np.random.binomial(2, 0.1 if renew else 0.3)
        refunds = np.random.binomial(1, 0.05 if seg != 'Basic' else 0.15)
        ltv = round(spend * tenure, 2)
        discount_used = int(np.random.rand() < (0.3 if seg == 'Basic' else 0.1))

        churn_score = (
            (tenure < 12) * 2 +
            (logins < 5) * 2 +
            (payment_fails > 0) * 2 +
            (session_time < 10) +
            (feature_use < 3) +
            (support_tickets > 3)
        )
        churn = 1 if churn_score >= 4 else 0

        records.append([
            customer_ids[i], tenure, ages[i], genders[i], locations[i], segments[i], subscription_types[i],
            contract_types[i], payment_methods[i], renew, logins, last_login.date(), session_time,
            feature_use, support_tickets, spend, payment_fails, refunds, ltv, discount_used, churn
        ])

    # Column names
    cols = [
        "customer_id", "tenure_months", "age", "gender", "location", "segment", "subscription_type",
        "contract_type", "payment_method", "auto_renew", "login_days_last_30", "last_login_date",
        "avg_session_duration", "feature_usage_count", "support_tickets_last_3mo",
        "monthly_spend", "payment_failures", "refund_requests", "lifetime_value",
        "used_discount_recently", "churn"
    ]

    # Create DataFrame
    df_churn = pd.DataFrame(records, columns=cols)
    df_churn["churn"] = df_churn["churn"].astype(int)

    # Push to DB
    engine = create_engine(get_db_url())
    df_churn.to_sql('customer_churn_data', con=engine, if_exists='append', index=False)
    print(f"✅ {len(df_churn)} churn rows inserted into 'customer_churn_data' table.")

if __name__ == "__main__":
    append_churn_rows()
