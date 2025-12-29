# Subscriber 1

import pika
from pika.exchange_type import ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="pubsub",
    exchange_type=ExchangeType.fanout,
)

queue = channel.queue_declare(
    queue="",
    exclusive=True,
)

queue_name = queue.method.queue

channel.queue_bind(
    queue=queue_name,
    exchange="pubsub",
)


def callback(ch, method, properties, body):
    print(f"Subscriber 1 received: {body.decode()}")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

print("Subscriber 1 started consuming...")

channel.start_consuming()
