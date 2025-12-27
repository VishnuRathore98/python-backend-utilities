import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
# params = pika.ConnectionParameters(host="localhost")
params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(
    exchange="", routing_key="hello", body="Hello, message from producer!"
)

print("Sent hello message! Closing connection...")

connection.close()
