"""
Different types of publishing properties
-----------------------------------------
"""

"""
Publisher Confirms
-------------------------
channel.confirm_delivery()

This enables publisher acknowledgements.

Without this:

You have no idea if RabbitMQ actually received your message.

With confirms:

RabbitMQ will ACK/NACK every publish.

This gives you network-level delivery guarantees.
"""

"""
Transactions
----------------------
channel.tx_select()
...
channel.tx_commit()
channel.tx_rollback()


This enables AMQP transactions.

Transactions guarantee all-or-nothing publishing:

Action          Effect
tx_select()     Start transaction mode
tx_commit()     Actually send messages
tx_rollback()   Cancel everything since last commit

If anything fails → nothing is published.

Transactions are very slow and rarely used in production. Confirms are preferred.
"""

"""
Durable Queue
---------------
channel.queue_declare("Test", durable=True)

Durable queue = survives broker restarts.

But durable queue ≠ durable message.

Both must be durable to survive crashes.
"""

"""
Message Properties
------------------------

properties=pika.BasicProperties(
    headers={"name": "Ram"},
    delivery_mode=1,
    expiration=13434341,
    content_type="application/json",
)

Property        Meaning
headers         Custom metadata
delivery_mode=1 Non-persistent message
expiration      TTL in milliseconds
content_type    Data type

If we used:

delivery_mode=2

the message would be written to disk.
"""

"""
Mandatory Flag
---------------
mandatory=True

This prevents silent message loss.

If no queue is bound → RabbitMQ returns the message to you instead of discarding it.

Without mandatory:

Message disappears if no queues are bound.
"""
