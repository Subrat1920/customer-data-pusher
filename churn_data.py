import os
import random
import numpy as np
import pandas as pd
from datetime import datetime
from faker import Faker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 5000
PLANS = ["Basic", "Pro", "Enterprise"]



def get_db_url():
    return os.getenv("CONNECTION_URL")

def generate_and_append_data():
    today = datetime.today().date()
    rows_to_generate = random.randint(3, 5)
    new_rows = []

    for _ in range(rows_to_generate):
        customer_id = random.randint(1, NUM_CUSTOMERS)
        usage_score = np.clip(np.random.normal(loc=70, scale=20), 0, 100)
        login_frequency = np.random.randint(1, 30)
        active_days = np.random.randint(5, 28)
        feature_adoption_score = np.clip(np.random.normal(usage_score * 0.8, 10), 0, 100)
        support_tickets = np.random.poisson(0.8)
        payment_issue = int(np.random.rand() < 0.05)
        marketing_engaged = int(np.random.rand() < 0.2)
        plan = random.choices(PLANS, weights=[0.5, 0.3, 0.2])[0]
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

        new_rows.append([
            customer_id, today, usage_score, login_frequency, active_days,
            feature_adoption_score, support_tickets, payment_issue,
            marketing_engaged, plan, downgraded, discount_applied,
            last_engaged_day, avg_session_duration, churn
        ])

    df = pd.DataFrame(new_rows, columns=[
        "customer_id", "date", "usage_score", "login_frequency", "active_days",
        "feature_adoption_score", "support_tickets", "payment_issue",
        "marketing_engaged", "plan", "downgraded", "discount_applied",
        "last_engaged_day", "avg_session_duration", "churn"
    ])

    engine = create_engine(get_db_url())
    df.to_sql('churn_data', con=engine, if_exists='append', index=False)
    print(f"✅ {len(df)} churn rows inserted for {today}.")

if __name__ == "__main__":
    generate_and_append_data()
