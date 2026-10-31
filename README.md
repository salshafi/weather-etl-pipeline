# Ottawa Weather ETL

A small Python ETL pipeline. It pulls hourly temperature data for Ottawa from the Open-Meteo API, stores it in a SQLite database, and can run once a day with cron on Linux.

## How it works

Extract, transform, load, each as its own function in `extract.py`:

- `extract()` calls the Open-Meteo API with `requests` and returns the JSON response.
- `transform()` pairs each hour with its temperature and builds one row per hour, skipping hours with no reading.
- `load()` writes the rows into a SQLite table. The primary key is (city, time) and rows are inserted with `INSERT OR REPLACE`, so running the script twice does not create duplicates.

If the API call fails or returns nothing usable, the script logs the error and exits with a non-zero code, so a failed scheduled run is easy to spot in the log.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python extract.py
python show_data.py          # print what was stored
```

## Scheduling

On Linux, a cron entry can run the script every day at 6:00 a.m. It uses full paths, because cron does not activate the virtual environment, and appends output to a log file:

```
0 6 * * * /path/to/.venv/bin/python /path/to/extract.py >> /path/to/pipeline.log 2>&1
```

Cron only runs while the machine is on.

## Limits

- One city (Ottawa) and one day of forecast per run.
- Hourly temperature only.

## Tools

Python, requests, SQLite, cron, Git. Tested on Windows and on an Ubuntu virtual machine.

## Possible next steps

- Add more cities
- Add a report query or chart
