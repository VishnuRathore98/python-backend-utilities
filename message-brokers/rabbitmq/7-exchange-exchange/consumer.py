import pika
from pika.exchange_type import ExchangeType


RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()


def on_message_received(ch, method, properties, body):
    print(f"Received new message: {body}")


channel.exchange_declare(exchange="secondexchange", exchange_type=ExchangeType.fanout)

channel.queue_declare(queue="letterbox")

channel.queue_bind(queue="letterbox", exchange="secondexchange")

channel.basic_consume(
    queue="letterbox", auto_ack=True, on_message_callback=on_message_received
)

print("Starting consuming")

channel.start_consuming()
