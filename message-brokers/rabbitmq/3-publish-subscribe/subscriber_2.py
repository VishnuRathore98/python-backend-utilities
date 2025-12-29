# Subscriber 2

import pika
from pika.exchange_type import ExchangeType

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.exchange_declare(
    exchange="pubsub",
    exchange_type=ExchangeType.fanout,
)
"""
Firstly, whenever we connect to Rabbit we need a fresh, empty queue. 
To do it we could create a queue with a random name, or, 
even better - let the server choose a random queue name for us. 
We can do this by supplying empty queue parameter to queue_declare.
"""
"""
Secondly, once the consumer connection is closed, the queue should be deleted. 
There's an exclusive flag for that.
"""
result = channel.queue_declare(
    queue="",
    exclusive=True,
)

queue_name = result.method.queue

"""
We've already created a fanout exchange and a queue. Now we need to 
tell the exchange to send messages to our queue. 
That relationship between exchange and a queue is called a binding.

From now on the "pubsub" exchange will append messages to our queue.
"""
channel.queue_bind(
    queue=queue_name,
    exchange="pubsub",
)


def callback(ch, method, properties, body):
    print(f"Subscriber 2 received: {body.decode()}")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

print("Subscriber 2 started consuming...")

channel.start_consuming()
