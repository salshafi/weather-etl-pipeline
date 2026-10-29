\# Ottawa Weather ETL



A small Python ETL pipeline. It pulls hourly temperature data for Ottawa from the Open-Meteo API, stores it in a SQLite database, and runs once a day with cron on Linux.



\## How it works



Extract, transform, load, each as its own function in `extract.py`:



\- `extract()` calls the Open-Meteo API with `requests` and returns the JSON response.

\- `transform()` pairs each hour with its temperature and builds one row per hour.

\- `load()` writes the rows into a SQLite table. The primary key is (city, time) and rows are inserted with `INSERT OR REPLACE`, so running the script twice does not create duplicates.



\## Setup



```

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python extract.py

```



On Windows, activate with `.venv\\Scripts\\activate` instead.



\## Scheduling



On Linux, a cron entry runs the script every day at 6:00 a.m. It uses full paths, because cron does not activate the virtual environment, and appends output to a log file:



```

0 6 \* \* \* /path/to/.venv/bin/python /path/to/extract.py >> /path/to/pipeline.log 2>\&1

```



Cron only runs while the machine is on.



\## Tools



Python, requests, SQLite, cron, Git. Tested on Windows and on an Ubuntu virtual machine.



\## Possible next steps



\- Add more cities

\- Add a report query or chart

\- Add logging and error handling

