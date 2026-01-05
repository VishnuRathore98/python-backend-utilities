import pika
import uuid 
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

reply_queue = channel.queue_declare(
    queue="",
    durable=True,
    exclusive=True,
)

reply_queue_name = reply_queue.method.queue


def client_message_callback(ch, method, properties, body):
    print(f"Client message received: {body}")


channel.basic_consume(
    queue=reply_queue_name,
    on_message_callback=client_message_callback,
    auto_ack = True,
)

channel.queue_declare(queue="request-queue")

message = "can i request a reply?"

correlation_id = str(uuid.uuid4())

print(f"Sending request {correlation_id}")

channel.basic_publish(
    exchange="", 
    routing_key="request-queue",
    properties=pika.BasicProperties(
        reply_to=reply_queue_name,
        correlation_id=correlation_id,
    ),
    body=message,
)

channel.start_consuming()
