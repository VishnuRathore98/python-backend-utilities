from celery_app import app
import csv
import time
import redis

r = redis.Redis(host="localhost", port=6379, db=1)


@app.task(bind=True)
def process_csv(self, file_path):
    with open(file_path, newline="") as csvfile:
        reader = list(csv.reader(csvfile))
        total = len(reader)

        for i, row in enumerate(reader):
            time.sleep(0.2)  # simulate work
            percent = int((i + 1) / total * 100)
            r.set(f"csv_progress:{file_path}", percent)

    return "CSV processed"
