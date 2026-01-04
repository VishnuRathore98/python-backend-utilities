import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

queue = channel.queue_declare(queue="", exclusive=True)

queue_name = queue.method.queue


def message_callback(ch, method, proprties, body):
    print(f"Server received: {body}")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=message_callback,
)
