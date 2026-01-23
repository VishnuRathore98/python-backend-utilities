from celery import Celery

app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@app.task
def add(x, y):
    return x + y


result = add.delay(4, 5)
print(result.get())  # Blocks until task completes

# run every 30 seconds
app.conf.beat_schedule = {
    "add-every-30-seconds": {"task": "tasks.add", "schedule": 30.0, "args": (10, 10)}
}
