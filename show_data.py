"""Print what is stored in weather.db (handy for checking a run)."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "weather.db"

conn = sqlite3.connect(DB_PATH)
count, first, last, low, high = conn.execute(
    "SELECT COUNT(*), MIN(time), MAX(time), MIN(temperature_c), MAX(temperature_c) "
    "FROM hourly_temperature"
).fetchone()
print(f"Rows: {count}  |  {first} to {last}  |  low {low} C, high {high} C\n")
for city, time, temp in conn.execute(
    "SELECT city, time, temperature_c FROM hourly_temperature ORDER BY time LIMIT 8"
):
    print(f"{city:8} {time}  {temp:5.1f} C")
conn.close()
