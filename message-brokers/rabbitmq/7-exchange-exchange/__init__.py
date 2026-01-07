"""
Exchange to Exchange routing
-----------------------------
Exchange-to-exchange routing means exchanges can be bound to other exchanges, not just to queues.
So messages can flow through multiple routing stages before reaching queues.

Producer → Exchange A → Exchange B → Queue → Consumer
"""
"""
What exchanges do
---------------------
An exchange is only a router.
It does not store messages — it decides where copies of a message go next based on bindings.

With exchange-to-exchange, the “next hop” can be another exchange.
"""

