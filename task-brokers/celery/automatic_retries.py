from celery import Celery
import requests

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


# Celery retries automatically when an exception happens.
@app.task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
)
def fetch_data(url):
    response = requests.get(url, timeout=2)
    response.raise_for_status()
    return response.text
