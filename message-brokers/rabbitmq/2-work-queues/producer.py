# Producer

import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

"""
Our tasks will be lost if RabbitMQ server stops.

When RabbitMQ quits or crashes it will forget the queues and messages 
unless you tell it not to. 
Two things are required to make sure that messages aren't lost: 
we need to mark both the queue and messages as durable.

First, we need to make sure that the queue will survive 
a RabbitMQ node restart. 
In order to do so, we need to declare it as durable:
"""
channel.queue_declare(queue="workqueue", durable=True)

count = 1

while True:
    message = f"message {count}"

    """
    We mark our messages as persistent - by supplying a 
    delivery_mode property with the value of 
    pika.DeliveryMode.Persistent
    It tells RabbitMQ to save the message to disk.
    There is still a short time window when RabbitMQ has accepted 
    a message and hasn't saved it yet.
    RabbitMQ doesn't do fsync(2) for every message -- it may be 
    just saved to cache and not really written to the disk. 
    The persistence guarantees aren't strong.
    """
    channel.basic_publish(
        exchange="",
        routing_key="workqueue",
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )

    print(f"Sent message: {count}")

    count += 1

connection.close()
