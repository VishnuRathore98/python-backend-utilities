import pika
from pika.exchange_type import ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="topic_exchange",
    exchange_type=ExchangeType.topic,
    durable=True,
)

queue = channel.queue_declare(
    queue="",
    exclusive=True,
    durable=True,
)

queue_name = queue.method.queue

channel.queue_bind(
    queue=queue_name,
    exchange="topic_exchange",
    routing_key="#.payments",  # Every routing key ending with payments
)


def message_callback(ch, method, properties, body):
    print(f"Payments service received: {body}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=message_callback,
)

print("Payments service started consuming...")

channel.start_consuming()

