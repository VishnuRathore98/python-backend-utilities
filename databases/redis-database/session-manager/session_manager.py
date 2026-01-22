import uuid
import json
from redis_client import redis_client

SESSION_TTL = 3600  # 1 hour
SESSION_PREFIX = "session:"

def create_session(data: dict) -> str:
    session_id = str(uuid.uuid4())
    redis_client.setex(
        f"{SESSION_PREFIX}{session_id}",
        SESSION_TTL,
        json.dumps(data)
    )
    return session_id

def get_session(session_id: str):
    if not session_id:
        return None

    data = redis_client.get(f"{SESSION_PREFIX}{session_id}")
    if data:
        # refresh TTL (sliding expiration)
        redis_client.expire(f"{SESSION_PREFIX}{session_id}", SESSION_TTL)
        return json.loads(data)
    return None

def delete_session(session_id: str):
    redis_client.delete(f"{SESSION_PREFIX}{session_id}")

