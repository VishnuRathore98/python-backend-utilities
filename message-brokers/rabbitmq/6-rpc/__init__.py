"""
RPC Pattern
------------
If we need to run a function on a remote computer and wait for the result.
This pattern is commonly known as Remote Procedure Call or RPC.
"""
"""
Callback queue
----------------
The request-reply pattern in RabbitMQ involves a straightforward interaction between the server and the client.

A client sends a request message and a server replies with a response message.

In order to receive a response we need to send a 'callback' queue name with the request. 
Such a queue is often server-named but can also have a well-known name (be client-named).

The server will then use that name to respond using the default exchange.
"""
"""
Message properties
-------------------
The AMQP 0-9-1 protocol predefines a set of 14 properties that go with a message. 
Most of the properties are rarely used, with the exception of the following:

 - delivery_mode: Marks a message as persistent (with a value of 2) or transient (any other value).
   
 - content_type: Used to describe the mime-type of the encoding. 
   For example for the often used JSON encoding it is a good practice to set this property to: application/json.

 - reply_to: Commonly used to name a callback queue.

 - correlation_id: Useful to correlate RPC responses with requests.
"""
"""
Correlation id
----------------
Creating a callback queue for every RPC request is inefficient. A better way is creating a single callback queue per client.

That raises a new issue, having received a response in that queue it's not clear to which request the response belongs. 
That's when the correlation_id property is used. We're going to set it to a unique value for every request. 
Later, when we receive a message in the callback queue we'll look at this property, and based on that we'll be able to 
match a response with a request. 
If we see an unknown correlation_id value, we may safely discard the message - it doesn't belong to our requests.

You may ask, why should we ignore unknown messages in the callback queue, rather than failing with an error? 
It's due to a possibility of a race condition on the server side. 
Although unlikely, it is possible that the RPC server will die just after sending us the answer, but before sending 
an acknowledgment message for the request. 
If that happens, the restarted RPC server will process the request again. 
That's why on the client we must handle the duplicate responses gracefully, and the RPC should ideally be idempotent.
"""
"""
Our RPC will work like this:
-----------------------------
When the Client starts up, it creates an exclusive callback queue.

For an RPC request, the Client sends a message with two properties: 
 reply_to, which is set to the callback queue and 
 correlation_id, which is set to a unique value for every request.

The request is sent to an rpc_queue queue.

The RPC worker (aka: server) is waiting for requests on that queue. 

When a request appears, it does the job and sends a message with the result back to the Client, 
using the queue from the reply_to field.

The client waits for data on the callback queue. When a message appears, it checks the correlation_id property. 

If it matches the value from the request it returns the response to the application.
"""
