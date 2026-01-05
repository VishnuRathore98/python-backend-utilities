import pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

params = pika.URLParameters(url=RABBITMQ_URL)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

queue_name = "request-queue"

channel.queue_declare(queue=queue_name)


def message_callback(ch, method, proprties, body):
    print(f"Request id: {proprties.correlation_id}")
    print(f"Server received: {body}")
    channel.basic_publish(
        exchange="",
        routing_key=proprties.reply_to,
        body=f"This is a reply to {proprties.correlation_id}",
    )


channel.basic_consume(
    queue=queue_name,
    on_message_callback=message_callback,
    auto_ack=True,
)

print("Server starting...")

channel.start_consuming()
