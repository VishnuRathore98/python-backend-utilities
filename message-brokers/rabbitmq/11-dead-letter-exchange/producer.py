import pika
from pika.exchange_type import ExchangeType

params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="main-exchange",
    exchange_type=ExchangeType.direct,
)

message = "Hello! this message will expire!"

channel.basic_publish(
    exchange="main-exchange",
    routing_key="test",
    body=message,
)

print(f"sent message: {message}")

connection.close()
