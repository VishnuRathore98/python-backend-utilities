"""
Alternate Exchange (AE)
------------------------
Alternate Exchange is a backup exchange that receives messages which cannot be routed to any queue 
by the main exchange.

In short:
If RabbitMQ can’t find a queue for a message → it sends the message to the Alternate Exchange 
instead of dropping it.

This provides lossless handling of unroutable messages.
"""
