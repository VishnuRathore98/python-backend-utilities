"""
Publisher - Subscriber Architecture
-------------------------------------
The assumption behind a work queue is that each task is delivered to exactly one worker. 
In this part we'll do something completely different -- we'll deliver a message to 
multiple consumers. 
This pattern is known as "publish/subscribe".
"""
"""
Listing exchanges:
-------------------
To list the exchanges on the server you can run the ever useful rabbitmqctl:

>> sudo rabbitmqctl list_exchanges
"""
"""
Listing bindings:
-----------------
You can list existing bindings using

>> rabbitmqctl list_bindings
"""
