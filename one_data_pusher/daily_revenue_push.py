import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

NEON_DATABASE_PASSWORD = os.getenv('NEON_DATABASE_PASSWORD')
NEON_DATABASE_USERNAME = os.getenv('NEON_DATABASE_USERNAME')
NEON_DATABASE_HOST = os.getenv('NEON_DATABASE_HOST')
NEON_DATABASE_PORT = 5432
NEON_DATABASE_DATABASE_NAME = os.getenv('NEON_DATABASE_DATABASE_NAME')

engine = create_engine(
    f"postgresql+psycopg2://{NEON_DATABASE_USERNAME}:{NEON_DATABASE_PASSWORD}@{NEON_DATABASE_HOST}:{NEON_DATABASE_PORT}/{NEON_DATABASE_DATABASE_NAME}?sslmode=require"
)

print("Engine created")
print('Reading the data from the csv')
df = pd.read_csv('datasets\daily_revenue_data.csv')
print(f"Data got read with shape {df.shape}")

df.to_sql('daily_revenue', con=engine, if_exists='replace', index=False)

print('Data got pushed')

