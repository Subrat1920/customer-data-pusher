import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
pgsql_password = os.getenv('POSTGRESQL_PASSWORD')

# Connect to the default 'postgres' database
conn = psycopg2.connect(
    dbname='postgres',       # connect to default database first
    user='postgres',
    password=pgsql_password,
    host='localhost',
    port=5432
)
conn.autocommit = True  # Required for CREATE DATABASE to work
cur = conn.cursor()

# Database name to be created
new_db_name = "customers"

# Create the new database (if not exists)
cur.execute(sql.SQL("CREATE DATABASE {}").format(
    sql.Identifier(new_db_name)
))


print(f"Database '{new_db_name}' created successfully.")

cur.close()
conn.close()
