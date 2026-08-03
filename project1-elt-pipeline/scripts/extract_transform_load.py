import os
import requests
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def extract_exchange_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"Extracted data for base currency: {data['base_code']}")
    return data


def transform_exchange_rates(raw_data):
    rates = raw_data["rates"]
    df = pd.DataFrame(list(rates.items()), columns=[
                      "currency_code", "exchange_rate"])
    df["base_currency"] = raw_data["base_code"]
    df["fetched_at"] = datetime.now()
    print(f"Transformed {len(df)} currency rates")
    return df


def load_to_postgres(df):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id SERIAL PRIMARY KEY,
            currency_code VARCHAR(10),
            exchange_rate NUMERIC,
            base_currency VARCHAR(10),
            fetched_at TIMESTAMP
        );
    """)

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO exchange_rates (currency_code, exchange_rate, base_currency, fetched_at)
            VALUES (%s, %s, %s, %s);
            """,
            (row["currency_code"], row["exchange_rate"],
             row["base_currency"], row["fetched_at"]),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Loaded {len(df)} rows into PostgreSQL")


if __name__ == "__main__":
    raw = extract_exchange_rates()
    transformed = transform_exchange_rates(raw)
    load_to_postgres(transformed)
    print("ELT pipeline completed successfully")
