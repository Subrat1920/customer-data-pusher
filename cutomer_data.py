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

industries = ["Tech", "Finance", "Retail", "Healthcare", "Education"]
regions = ["North America", "Europe", "Asia", "LATAM"]
sizes = ["Small", "Mid", "Large"]
review_templates = [
    "The platform has helped our team stay organized and productive.",
    "We're facing some bugs and missing features we expected.",
    "Great interface, but support can be slow.",
    "We love the reporting tools and automation options!",
    "It's overpriced for the feature set we use.",
    "Easy onboarding and helpful documentation.",
    "Product is not intuitive for non-technical users.",
    "Outstanding customer service and integrations.",
    "We rarely use all the features, considering alternatives.",
    "Reliable and user-friendly. Works well for our business size."
]

NUM_CUSTOMERS = 5000

def get_db_url():
    return f"postgresql://{os.getenv('NEON_DATABASE_USERNAME')}:{os.getenv('NEON_DATABASE_PASSWORD')}" \
           f"@{os.getenv('NEON_DATABASE_HOST')}:{os.getenv('NEON_DATABASE_PORT')}/" \
           f"{os.getenv('NEON_DATABASE_DATABASE_NAME')}?sslmode=require"

def append_metadata_rows():
    today = datetime.today().date()
    rows_to_generate = random.randint(3, 5)
    records = []

    for _ in range(rows_to_generate):
        customer_id = random.randint(1, NUM_CUSTOMERS)
        company = fake.company()
        email = fake.email()
        industry = random.choice(industries)
        region = random.choice(regions)
        company_size = random.choices(sizes, weights=[0.6, 0.3, 0.1])[0]
        join_date = fake.date_between(start_date='-2y', end_date='today')
        review = random.choice(review_templates)

        records.append([
            customer_id, email, company, industry, region,
            company_size, join_date, review
        ])

    df = pd.DataFrame(records, columns=[
        "customer_id", "company_email", "company", "industry", "region",
        "company_size", "join_date", "review_text"
    ])

    engine = create_engine(get_db_url())
    df.to_sql('customer_data', con=engine, if_exists='append', index=False)
    print(f"✅ {len(df)} metadata rows inserted.")

if __name__ == "__main__":
    append_metadata_rows()
