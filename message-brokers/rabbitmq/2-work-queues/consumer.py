# Consumer

import pika
import time
import random

RABBITMQ_URL="amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

"""
The durability options let the tasks survive even if 
RabbitMQ is restarted.
"""
channel.queue_declare(queue="workqueue", durable=True,)

print("Waiting for messages...")

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")
    # Mocking delay in processing
    time.sleep(random.randint(1,6))
    print("Done processing.")
    """
    In order to make sure a message is never lost, RabbitMQ supports message acknowledgments. 
    An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message 
    had been received, processed and that RabbitMQ is free to delete it.

    If a consumer dies (its channel is closed, connection is closed, or TCP connection is lost) 
    without sending an ack, RabbitMQ will understand that a message wasn't processed fully and 
    will re-queue it. 
    If there are other consumers online at the same time, it will then quickly redeliver it 
    to another consumer. That way you can be sure that no message is lost, even if the workers occasionally die.

    A timeout (30 minutes by default) is enforced on consumer delivery acknowledgement. 
    This helps detect buggy (stuck) consumers that never acknowledge deliveries. 
    We can increase this timeout.
    """
    ch.basic_ack(delivery_tag=method.delivery_tag)

"""
This uses the basic.qos protocol method to tell RabbitMQ not to give 
more than one message to a worker at a time. 
Or, in other words, don't dispatch a new message to a worker until 
it has processed and acknowledged the previous one. 
Instead, it will dispatch it to the next worker that is not still busy.
"""
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="workqueue", on_message_callback=callback,)

print("Waiting for messages...")

channel.start_consuming()
