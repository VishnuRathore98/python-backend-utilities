from celery import Celery
from celery.schedules import crontab

app = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.autodiscover_tasks()

# tasks


@app.task
def cleanup_old_records():
    print("Cleaning up old records...")


app.conf.beat_schedule = {
    "cleanup-every-night": {
        "task": "tasks.cleanup_old_records",
        "schedule": crontab(hour=2, minute=0),  # every day at 2 AM
    },
}

crontab(minute="*/5")  # every 5 minutes
crontab(hour=0, minute=0)  # daily at midnight
crontab(day_of_week="mon")  # every Monday
