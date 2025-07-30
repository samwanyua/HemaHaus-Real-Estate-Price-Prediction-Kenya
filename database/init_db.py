import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("HOST", "localhost"),
            port=os.getenv("PORT", "5432")
        )
    except psycopg2.Error as e:
        print("❌ Database connection failed:", e)
        raise

def initialize_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        schema_path = os.path.join("database", "schema.sql")
        with open(schema_path, "r") as f:
            cur.execute(f.read())

        conn.commit()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print("❌ Error during initialization:", e)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    initialize_db()
