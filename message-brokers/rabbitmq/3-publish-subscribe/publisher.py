# Publisher

import pika
from pika.exchange_type import ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

"""
The fanout exchange is very simple. 
As in the name itself, it just broadcasts all the messages 
it receives to all the queues it knows. 
"""
channel.exchange_declare(
    exchange="pubsub",
    exchange_type=ExchangeType.fanout,
)

message = "This is a broadcast message."

channel.basic_publish(
    exchange="pubsub",
    routing_key="",
    body=message,
)

connection.close()
