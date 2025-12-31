import pika
from pika.exchange_type import ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="_routing",
    exchange_type=ExchangeType.direct,
    durable=True,
)

message = "This is a routed message."

channel.basic_publish(
    exchange="_routing",
    routing_key="payments",
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
    ),
    body=message,
)

print(f"Sent message: {message}")

connection.close()
