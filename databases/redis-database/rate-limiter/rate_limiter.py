# Fixed Window Rate Limiting
# Max 5 requests per 60 seconds per IP

from fastapi import FastAPI, Request, HTTPException, Depends
import redis

app = FastAPI()

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# Rate Limiter Logic

def rate_limiter(request: Request, limit=5, window=60):
    ip = request.client.host
    key = f"rate:{ip}"

    current = r.incr(key)

    if current == 1:
        r.expire(key, window)

    if current > limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

#Use as FastAPI Dependency

@app.get("/protected", dependencies=[Depends(rate_limiter)])
def protected():
    return {"message": "You are within the rate limit"}

# Custom Limits per Endpoint

def strict_limiter(request: Request):
    return rate_limiter(request, limit=2, window=10)

@app.get("/strict", dependencies=[Depends(strict_limiter)])
def strict():
    return {"message": "Strict limit"}

