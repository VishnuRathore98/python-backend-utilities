import pika
from pika.exchange_type import ExchangeType


def dead_letter_message_callback(ch, method, properties, body):
    print(f"DLEx: received message: {body}")


params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="dead-letter-exchange",
    exchange_type=ExchangeType.fanout,
)

channel.exchange_declare(
    exchange="main-exchange",
    exchange_type=ExchangeType.direct,
    arguments={"x-dead-letter-exchange": "dead-letter-exchange", "x-message-ttl": 1000},
)

channel.queue_declare(queue="dead-letter-exchange-queue")
channel.queue_bind(
    queue="dead-letter-exchange-queue",
    exchange="dead-letter-exchange",
)

channel.queue_declare(queue="main-exchange-queue")
channel.queue_bind(
    queue="main-exchange-queue",
    exchange="main-exchange",
)

channel.basic_consume(
    queue="dead-letter-exchange-queue",
    on_message_callback=dead_letter_message_callback,
    auto_ack=True,
)

channel.start_consuming()
