import pandas as pd
import numpy as np
import random
from faker import Faker
import os
import time
import psycopg2
from dotenv import load_dotenv
load_dotenv()
pgsql_password = os.getenv('POSTGRESQL_PASSWORD')

fake = Faker()
np.random.seed(42)
random.seed(42)

## establish connection
conn = psycopg2.connect(
    dbname = 'prac',
    user = 'postgres',
    password = pgsql_password,
    host = 'localhost',
    port =5432
)

cur = conn.cursor()


## creating a database
cur.execute("""
CREATE TABLE IF NOT EXISTS testing_table_connection(
            sl_no SERIAL PRIMARY KEY,
            name varchar(50),
            email varchar(100),
            address varchar(200),
            phone varchar(30)
            )
""")

conn.commit()

for i in range(20):
    name = fake.name()
    email = fake.email()
    address = fake.address()
    number = fake.phone_number()
    cur.execute("""
    insert into testing_table_connection(name, email, address, phone)    
                values (%s, %s, %s, %s);
""", (name, email, address, number))
    time.sleep(2)
    print(f'Logged {i} row')

    conn.commit()

cur.close()
conn.close()
