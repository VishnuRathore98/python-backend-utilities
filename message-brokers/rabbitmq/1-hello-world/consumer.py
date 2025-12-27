import pika

RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
#params = pika.ConnectionParameters(host="localhost")
params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.queue_declare(queue="hello")


def callback(ch, method, properties, body):
    print(f"Received: {body}")


channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

print("Waiting for messages...")

channel.start_consuming()
