import pika
from pika.exchange_type import ExchangeType


def alt_message_callback(ch, method, properties, body):
    print(f"alt: received message: {body}")


def main_message_callback(ch, method, properties, body):
    print(f"main: received message: {body}")


params = pika.ConnectionParameters(host="localhost")

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="altexchange",
    exchange_type=ExchangeType.fanout,
)

channel.exchange_declare(
    exchange="mainexchange",
    exchange_type=ExchangeType.direct,
    arguments={"alternate-exchange": "altexchange"},
)

channel.queue_declare(queue="altexchangequeue")
channel.queue_bind(
    queue="altexchangequeue",
    exchange="altexchange",
)

channel.basic_consume(
    queue="altexchangequeue",
    on_message_callback=alt_message_callback,
    auto_ack=True,
)

channel.queue_declare(queue="mainexchangequeue")
channel.queue_bind(
    queue="mainexchangequeue",
    exchange="mainexchange",
)

channel.basic_consume(
    queue="mainexchangequeue",
    on_message_callback=main_message_callback,
    auto_ack=True,
)

channel.start_consuming()
