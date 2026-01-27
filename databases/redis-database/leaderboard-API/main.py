from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

LEADERBOARD_KEY = "game:leaderboard"

@app.post("/score")
def add_score(player: str, score: int):
    r.zadd(LEADERBOARD_KEY, {player: score})
    return {
        "message": "Score updated",
        "player": player,
        "score": score
    }

@app.get("/leaderboard")
def get_leaderboard(limit: int = 10):
    players = r.zrevrange(
        LEADERBOARD_KEY,
        0,
        limit - 1,
        withscores=True
    )

    return [
        {"rank": i + 1, "player": name, "score": score}
        for i, (name, score) in enumerate(players)
    ]

@app.get("/rank/{player}")
def get_rank(player: str):
    rank = r.zrevrank(LEADERBOARD_KEY, player)
    score = r.zscore(LEADERBOARD_KEY, player)

    if rank is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "player": player,
        "rank": rank + 1,  # human-friendly
        "score": score
    }


