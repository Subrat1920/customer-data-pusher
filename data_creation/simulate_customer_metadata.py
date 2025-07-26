import pandas as pd
import numpy as np
import random
from faker import Faker
import os

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

fake = Faker()
np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 5000

industries = ["Tech", "Finance", "Retail", "Healthcare", "Education"]
regions = ["North America", "Europe", "Asia", "LATAM"]
sizes = ["Small", "Mid", "Large"]

# Simulated customer review samples
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

def simulate_customer_metadata(num_customers=NUM_CUSTOMERS):
    data = []
    for cid in range(1, num_customers + 1):
        company = fake.company()
        email = fake.email()
        industry = random.choice(industries)
        region = random.choice(regions)
        company_size = random.choices(sizes, weights=[0.6, 0.3, 0.1])[0]
        join_date = fake.date_between(start_date='-2y', end_date='today')
        review = random.choice(review_templates)
        data.append([
            cid, email, company, industry, region, company_size, join_date, review
        ])

    df = pd.DataFrame(data, columns=[
        "customer_id", "company_email", "company", "industry", "region",
        "company_size", "join_date", "review_text"
    ])
    df.to_csv("Datasets/customer_metadata.csv", index=False)
    print("✅ customer_metadata.csv created.")
    return df

# Generate the file
simulate_customer_metadata()
