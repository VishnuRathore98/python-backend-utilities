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

user_payments_message = "An european user paid for something."

business_order_message = "An asian business ordered something."

channel.basic_publish(
    exchange="topic_exchange",
    routing_key="user.europe.payments",
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
    ),
    body=user_payments_message,
)

print(f"Sent message: {user_payments_message}")

channel.basic_publish(
    exchange="topic_exchange",
    routing_key="business.asia.order",
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
    ),
    body=business_order_message,
)

print(f"Sent message: {business_order_message}")

connection.close()
