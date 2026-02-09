from fastapi import FastAPI, HTTPException, Request
from redis.asyncio import Redis
import time

app = FastAPI(title="Redis Rate Limited API")

redis = Redis(host="localhost", port=6379, decode_responses=True)

RATE_LIMIT = 5  # requests
WINDOW_SECONDS = 60  # per minute

# -----------------------------
# Rate Limiter Dependency
# -----------------------------


async def rate_limiter(request: Request):
    user_id = request.headers.get("X-User", "anonymous")
    current_window = int(time.time() // WINDOW_SECONDS)

    key = f"rate_limit:{user_id}:{current_window}"

    count = await redis.incr(key)

    if count == 1:
        await redis.expire(key, WINDOW_SECONDS)

    if count > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


# -----------------------------
# Protected API
# -----------------------------


@app.get("/protected")
async def protected_api(_: None = rate_limiter):
    return {"message": "You passed the rate limit!"}
