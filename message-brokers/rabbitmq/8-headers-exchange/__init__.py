"""
Headers Exchange
------------------
A headers exchange routes messages based on message headers, not routing keys.

Routing decisions are made by matching key–value pairs in message headers.

x-match
------------------
    Mode                Meaning
-----------       --------------------------------
    all             ALL headers must match
    any             ANY one header must match

Trade-off
-----------
Headers exchanges are slower than topic/direct exchanges.
Use only when routing keys become unmanageable.
"""
