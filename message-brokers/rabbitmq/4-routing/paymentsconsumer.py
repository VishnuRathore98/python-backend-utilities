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

queue = channel.queue_declare(
    queue="payments_queue",
    #    exclusive=True,
    durable=True,
)

queue_name = "payments_queue"  # queue.method.queue

channel.queue_bind(
    queue=queue_name,
    exchange="_routing",
    routing_key="payments",
)


def message_callback(ch, method, properties, body):
    print(f"Payments service received: {body}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=message_callback,
)

print("Payments service stated consuming...")

channel.start_consuming()
