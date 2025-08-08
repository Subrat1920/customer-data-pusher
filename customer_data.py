import os
import random
import pandas as pd
from datetime import datetime, date
from faker import Faker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
fake = Faker()
random.seed(42)

ALLOWED_EMAILS = [
    "subratmishra1sep@gmail.com", "2subratmishra1sep@gmail.com",
    "subuking001@gmail.com", "22mca053.subratmishra@giet.edu",
    "22mca053.subratmishra@gmail.com", "subu2459@gmail.com",
    "prjctreview@gmail.com", "sumu12321@gmail.com",
    "photosubratmishra@gmail.com"
]

def get_db_url():
    url = os.getenv("CONNECTION_URL")
    if not url:
        raise ValueError("CONNECTION_URL not set in .env")
    return url

def generate_customer_row():
    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    customer_id = f"CUST{ts}{random.randint(100,999)}"
    full_name = fake.name()
    email = random.choice(ALLOWED_EMAILS)
    phone_number = fake.phone_number()
    city = fake.city()
    state = fake.state()
    country = "India"
    signup_date = fake.date_between(start_date='-2y', end_date='today')
    review_text = random.choice([
        "The streaming quality is excellent.",
        "Too many ads on the basic plan.",
        "Loving the variety of genres available.",
        "Customer support resolved my issue quickly.",
        "The app is easy to use.",
        "The streaming quality is excellent.",
        "Too many ads on the basic plan.",
        "Loving the variety of genres available.",
        "Customer support resolved my issue quickly.",
        "The app is easy to use.",
        "The streaming quality is excellent.",
        "Too many ads on the basic plan.",
        "Loving the variety of genres available.",
        "Customer support resolved my issue quickly.",
        "The app is easy to use.",
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
    ])
    pushed_date = date.today()
    return [
        customer_id, full_name, email, phone_number,
        city, state, country, signup_date, review_text, pushed_date
    ]

def insert_single_customer():
    record = [generate_customer_row()]
    df = pd.DataFrame(record, columns=[
        "customer_id", "full_name", "email", "phone_number",
        "city", "state", "country", "signup_date", "review_text", "pushed_date"
    ])
    engine = create_engine(get_db_url())
    df.to_sql('customer_data', con=engine, if_exists='append', index=False)
    print(f"✅ 1 row inserted into customer_data.")

if __name__ == "__main__":
    insert_single_customer()
