from fastapi import FastAPI
import redis
import time
import json

app = FastAPI()

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# Simulated Slow Database Call
def slow_db_call(user_id: int):
    time.sleep(2)  # simulate slow DB
    return {
        "id": user_id,
        "name": "John",
        "email": "john@test.com"
    }

# GET API with Redis Cache (Cache-Aside Pattern)
@app.get("/users/{user_id}")
def get_user(user_id: int):
    cache_key = f"user:{user_id}"

    # Try cache
    cached = r.get(cache_key)
    if cached:
        return {
            "source": "cache",
            "data": json.loads(cached)
        }

    # Cache miss → slow DB
    data = slow_db_call(user_id)

    # Save to cache (30 seconds)
    r.setex(cache_key, 30, json.dumps(data))

    return {
        "source": "database",
        "data": data
    }

# Cache Invalidation (Update Endpoint)
@app.put("/users/{user_id}")
def update_user(user_id: int):
    # pretend we updated DB here

    # invalidate cache
    r.delete(f"user:{user_id}")

    return {"message": "User updated, cache cleared"}

