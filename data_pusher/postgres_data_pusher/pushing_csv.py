import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import urllib.parse

# Load environment variables
load_dotenv()

# PostgreSQL connection details
user = 'postgres'
raw_password = os.getenv("POSTGRESQL_PASSWORD")
password = urllib.parse.quote_plus(raw_password)  # safely encode special characters
host = 'localhost'
port = 5432
database = 'customers'

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
print('Engine created')

# Load CSV file
df = pd.read_csv(r"D:\Data Science Projects\Personal_Project\Datasets\customer_churn_data.csv")

# Write to database
try:
    df.to_sql('customer_churn_data', engine, if_exists='append', index=False)
    print("Table created and data inserted successfully.")
except Exception as e:
    print("An error occurred:", e)
