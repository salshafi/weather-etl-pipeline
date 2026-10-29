import sqlite3
from pathlib import Path

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
DB_PATH = Path(__file__).parent / "weather.db"


def extract():
    params = {
        "latitude": 45.42,
        "longitude": -75.70,
        "hourly": "temperature_2m",
        "timezone": "America/Toronto",
        "forecast_days": 1,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def transform(data):
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    rows = []
    for time, temp in zip(times, temps):
        rows.append(("Ottawa", time, temp))
    return rows


def load(rows):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hourly_temperature (
            city TEXT,
            time TEXT,
            temperature_c REAL,
            PRIMARY KEY (city, time)
        )
    """)
    cur.executemany(
        "INSERT OR REPLACE INTO hourly_temperature (city, time, temperature_c) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM hourly_temperature")
    total = cur.fetchone()[0]
    conn.close()
    return total


def main():
    data = extract()
    rows = transform(data)
    total = load(rows)
    print(f"Loaded {len(rows)} rows. Table now has {total} rows.")


if __name__ == "__main__":
    main()