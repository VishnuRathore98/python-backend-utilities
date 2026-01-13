import pika
from pika.exchange_type import ExchangeType

params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="altexchange",
    exchange_type=ExchangeType.fanout,
)

channel.exchange_declare(
    exchange="mainexchange",
    exchange_type=ExchangeType.direct,
    arguments={"alternate-exchange": "altexchange"},
)

message = "Hello!"

channel.basic_publish(
    exchange="mainexchange",
    routing_key="test",
    body=message,
)

print(f"sent message: {message}")

connection.close()
