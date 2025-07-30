# database/export_to_csv.py
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    host=os.getenv("HOST", "localhost"),
)

query = "SELECT * FROM raw_listings;"
df = pd.read_sql(query, conn)
df.to_csv("data/raw/raw_listings.csv", index=False)

conn.close()
print("Data exported to data/raw/raw_listings.csv")
