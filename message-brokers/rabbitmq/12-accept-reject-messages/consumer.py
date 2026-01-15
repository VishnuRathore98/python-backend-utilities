import pika
from pika import delivery_mode
from pika.exchange_type import ExchangeType


def on_message_callback(ch, method, properties, body):
    # Automatically acknowledging messages.
    ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

    # Only acknowledging when we receive the 5th message
    if method.delivery_tag % 5 == 0:
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)

    # When we receive the 5th message auto unackowledge all back and put them back in queue
    if method.delivery_tag % 5 == 0:
        ch.basic_nack(delivery_mode=method.delivery_tag, requeue=True, multiple=True)

    print(f"received message: {body}")


params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="except-reject-exchange",
    exchange_type=ExchangeType.fanout,
)


channel.queue_declare(queue="letter-queue")
channel.queue_bind(
    queue="letter-queue",
    exchange="except-reject-exchange",
    routing_key="test",
)

channel.basic_consume(
    queue="letter-queue",
    on_message_callback=on_message_callback,
)

channel.start_consuming()
