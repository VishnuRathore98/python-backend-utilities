import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(exchange="headersexchange", exchange_type=ExchangeType.headers)

message = "This message will be sent with headers."

channel.basic_publish(
    exchange="headersexchange",
    routing_key="",
    body=message,
    properties=pika.BasicProperties(headers={"name": "jinny"}),
)

print(f"Message sent: {message}")

connection.close()
