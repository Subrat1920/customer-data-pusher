import pandas as pd
import numpy as np
import random
from faker import Faker
import os

# Ensure output directory exists
os.makedirs("Datasets", exist_ok=True)

fake = Faker()
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000
DATES = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")  # 2 years daily
PLANS = ["Basic", "Pro", "Enterprise"]

def generate_churn_data():
    churn_data = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):
        plan = random.choices(PLANS, weights=[0.5, 0.3, 0.2])[0]
        join_date = random.choice(DATES[:-180])  # Joined at least ~6 months before end
        customer_dates = [d for d in DATES if d >= join_date]
        churn_occurred = False

        for date in customer_dates:
            if churn_occurred:
                break  # stop generating after churn

            usage_score = np.clip(np.random.normal(loc=70, scale=20), 0, 100)
            login_frequency = np.random.randint(1, 30)
            active_days = np.random.randint(5, 28)
            feature_adoption_score = np.clip(np.random.normal(usage_score * 0.8, 10), 0, 100)
            support_tickets = np.random.poisson(0.8)
            payment_issue = int(np.random.rand() < 0.05)
            marketing_engaged = int(np.random.rand() < 0.2)
            downgraded = int(np.random.rand() < 0.05)
            discount_applied = int(np.random.rand() < 0.1)
            last_engaged_day = np.random.randint(1, 31)
            avg_session_duration = round(np.random.normal(15, 5), 2)

            churn_prob = (
                0.05
                + 0.2 * (usage_score < 40)
                + 0.1 * (support_tickets > 2)
                + 0.1 * payment_issue
                + 0.05 * (login_frequency < 5)
            )
            churn = int(np.random.rand() < churn_prob)
            if churn:
                churn_occurred = True

            churn_data.append([
                customer_id, date, usage_score, login_frequency, active_days,
                feature_adoption_score, support_tickets, payment_issue,
                marketing_engaged, plan, downgraded, discount_applied,
                last_engaged_day, avg_session_duration, churn
            ])

    df = pd.DataFrame(churn_data, columns=[
        "customer_id", "date", "usage_score", "login_frequency", "active_days",
        "feature_adoption_score", "support_tickets", "payment_issue",
        "marketing_engaged", "plan", "downgraded", "discount_applied",
        "last_engaged_day", "avg_session_duration", "churn"
    ])

    df.to_csv("Datasets/customer_churn_data.csv", index=False)
    print("✅ customer_churn_data.csv created.")
    return df

# Run the generation
df = generate_churn_data()
