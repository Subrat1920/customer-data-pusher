import os
import random
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

revenue_map = {"Basic": 1000, "Pro": 3000, "Enterprise": 10000}
plans = ["Basic", "Pro", "Enterprise"]



def get_db_url():
    return os.getenv("CONNECTION_URL")

def append_daily_revenue_rows():
    today = datetime.today().date()
    rows_to_generate = random.randint(3, 5)
    new_rows = []

    for _ in range(rows_to_generate):
        plan = random.choice(plans)
        active_customers = random.randint(50, 300)
        churn_count = random.randint(0, 10)
        new_signups = random.randint(0, 20)
        daily_revenue = active_customers * revenue_map[plan]
        avg_usage_score = round(np.clip(np.random.normal(loc=70, scale=15), 0, 100), 2)

        new_rows.append([
            today, plan, active_customers, churn_count,
            new_signups, daily_revenue, avg_usage_score
        ])

    df = pd.DataFrame(new_rows, columns=[
        "date", "plan", "active_customers", "churn_count",
        "new_signups", "daily_revenue", "avg_usage_score"
    ])

    engine = create_engine(get_db_url())
    df.to_sql('daily_revenue', con=engine, if_exists='append', index=False)
    print(f"✅ {len(df)} revenue rows inserted for {today}.")

if __name__ == "__main__":
    append_daily_revenue_rows()
