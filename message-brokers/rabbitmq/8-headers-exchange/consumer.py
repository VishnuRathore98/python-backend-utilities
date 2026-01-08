import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()


def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")


channel.exchange_declare(exchange="headersexchange", exchange_type=ExchangeType.headers)

channel.queue_declare(queue="letterbox")

bind_args = {"x-match": "all", "name": "jinny", "age": "34"}

channel.queue_bind(queue="letterbox", exchange="headersexchange", arguments=bind_args)

channel.basic_consume(
    queue="letterbox", auto_ack=True, on_message_callback=on_message_received
)

print("Starting consuming")

channel.start_consuming()
