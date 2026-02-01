from datetime import datetime


def current_week_key():
    now = datetime.utcnow()
    year, week, _ = now.isocalendar()
    return f"game:leaderboard:{year}-W{week}"


def leaderboard_key():
    return current_week_key()


@app.post("/score/increment")
async def increment_score(player: str, points: int = 1):
    key = leaderboard_key()

    new_score = await redis.zincrby(key, points, player)

    return {"week": key, "player": player, "new_score": new_score}


@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    key = leaderboard_key()

    players = await redis.zrevrange(key, 0, limit - 1, withscores=True)

    return [
        {"rank": i + 1, "player": name, "score": score}
        for i, (name, score) in enumerate(players)
    ]


@app.get("/rank/{player}")
async def get_rank(player: str):
    key = leaderboard_key()

    rank = await redis.zrevrank(key, player)
    score = await redis.zscore(key, player)

    if rank is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return {"week": key, "player": player, "rank": rank + 1, "score": score}


SECONDS_IN_4_WEEKS = 60 * 60 * 24 * 28


@app.on_event("startup")
async def setup_expiry():
    key = leaderboard_key()
    await redis.expire(key, SECONDS_IN_4_WEEKS)
