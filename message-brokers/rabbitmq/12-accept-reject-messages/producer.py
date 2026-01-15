import pika
from pika.exchange_type import ExchangeType

params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="except-reject-exchange",
    exchange_type=ExchangeType.fanout,
)

message = "Hello!"

while True:
    channel.basic_publish(
        exchange="except-reject-exchange",
        routing_key="test",
        body=message,
    )
    print(f"sent message: {message}")
    input("Press any key to continue...")
