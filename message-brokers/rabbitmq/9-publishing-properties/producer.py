import pika
from pika.exchange_type import ExchangeType


connection_params = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# Enable publish confirm
channel.confirm_delivery()

# Enable transaction
channel.tx_select()

channel.exchange_declare(exchange="pubsub", exchange_type=ExchangeType.fanout)

# Create a durable queue that survives restart
channel.queue_declare("Test", durable=True)

message = "This is a brodcast message!"

channel.basic_publish(
    exchange="pubsub",
    routing_key="",
    # Set properties including custom (headers), delivery_mode (message persistance), expiration
    properties=pika.BasicProperties(
        headers={"name": "Ram"},
        delivery_mode=1,
        expiration=13434341,
        content_type="application/json",
    ),
    body=message,
    # Set the publish to be mandatory - i.e. recieve a notification of failure
    mandatory=True,
)

# Commit a transaction
channel.tx_commit()

# Rollback a transaction
channel.tx_rollback()

print(f"Sent message: {message}")

connection.close()
