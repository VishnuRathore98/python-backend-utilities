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
    queue="",
    exclusive=True,
    durable=True,
)

queue_name = queue.method.queue

channel.queue_bind(
    queue=queue_name,
    exchange="_routing",
    routing_key="analytics",
)


def message_callback(ch, method, properties, body):
    print(f"Analytics service received: {body}")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=message_callback,
    auto_ack=True,
)

print("Analytics service stated consuming...")

channel.start_consuming()
