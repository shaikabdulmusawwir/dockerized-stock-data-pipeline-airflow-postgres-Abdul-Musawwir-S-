import os
import logging
from datetime import datetime

import requests
import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

DB_HOST = os.getenv("STOCK_DB_HOST", "postgres")
DB_PORT = os.getenv("STOCK_DB_PORT", "5432")
DB_NAME = os.getenv("STOCK_DB_NAME", "stocksdb")
DB_USER = os.getenv("STOCK_DB_USER", "stockuser")
DB_PASSWORD = os.getenv("STOCK_DB_PASSWORD", "stockpass")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def fetch_stock_data(symbol: str = "AAPL"):
    if not API_KEY:
        raise ValueError("ALPHAVANTAGE_API_KEY not set")
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Unexpected API response: {data.keys()}")

    ts_data = data["Time Series (Daily)"]
    rows = []
    for date_str, metrics in ts_data.items():
        ts = datetime.fromisoformat(date_str)
        price = float(metrics["4. close"])
        volume = int(metrics["5. volume"])
        rows.append((symbol, price, volume, ts))
    return rows

def load_to_db(rows):
    if not rows:
        logger.info("No rows to insert")
        return

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        insert_sql = """
            INSERT INTO stock_prices (symbol, price, volume, ts)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """
        execute_values(cur, insert_sql, rows)
        conn.commit()
        cur.close()
        logger.info("Inserted %d rows into stock_prices", len(rows))
    except Exception as e:
        logger.exception("Error inserting into DB: %s", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def main(symbol: str = "AAPL"):
    try:
        rows = fetch_stock_data(symbol)
        load_to_db(rows)
    except Exception as e:
        logger.exception("Pipeline failed for symbol %s: %s", symbol, e)
        # let Airflow mark task as failed
        raise

if __name__ == "__main__":
    main()
