import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

queue = channel.queue_declare(
    queue="",
    durable=True,
    exclusive=True,
)

queue_name = queue.method.queue

message = "test message"


def client_message_callback(ch, method, properties, body):
    print(f"Client message received: {body}")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=client_message_callback,
)

channel.basic_publish(exchange="", routing_key="", body=message)
