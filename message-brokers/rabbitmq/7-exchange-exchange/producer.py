import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(exchange="firstexchange", exchange_type=ExchangeType.direct)

channel.exchange_declare(exchange="secondexchange", exchange_type=ExchangeType.fanout)

channel.exchange_bind(destination="secondexchange", source="firstexchange")

message = "This message has gone through multiple exchanges."

channel.basic_publish(exchange="firstexchange", routing_key="", body=message)

print(f"Message sent: {message}")

connection.close()
