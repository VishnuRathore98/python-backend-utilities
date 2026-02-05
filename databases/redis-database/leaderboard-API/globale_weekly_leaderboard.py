from datetime import datetime

def weekly_key():
    year, week, _ = datetime.utcnow().isocalendar()
    return f"game:leaderboard:weekly:{year}-W{week}"

GLOBAL_KEY = "game:leaderboard:global"

@app.post("/score/increment")
async def increment_score(player: str, points: int = 1):
    week_key = weekly_key()

    # update both leaderboards
    global_score = await redis.zincrby(GLOBAL_KEY, points, player)
    weekly_score = await redis.zincrby(week_key, points, player)

    return {
        "player": player,
        "points_added": points,
        "global_score": global_score,
        "weekly_score": weekly_score
    }


@app.get("/leaderboard/global")
async def global_leaderboard(limit: int = 10):
    players = await redis.zrevrange(
        GLOBAL_KEY, 0, limit - 1, withscores=True
    )

    return [
        {"rank": i + 1, "player": name, "score": score}
        for i, (name, score) in enumerate(players)
    ]


@app.get("/leaderboard/weekly")
async def weekly_leaderboard(limit: int = 10):
    key = weekly_key()

    players = await redis.zrevrange(
        key, 0, limit - 1, withscores=True
    )

    return [
        {"rank": i + 1, "player": name, "score": score}
        for i, (name, score) in enumerate(players)
    ]

@app.get("/rank/{scope}/{player}")
async def get_rank(scope: str, player: str):
    if scope == "global":
        key = GLOBAL_KEY
    elif scope == "weekly":
        key = weekly_key()
    else:
        raise HTTPException(status_code=400, detail="Invalid scope")

    rank = await redis.zrevrank(key, player)
    score = await redis.zscore(key, player)

    if rank is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "scope": scope,
        "player": player,
        "rank": rank + 1,
        "score": score
    }

FOUR_WEEKS = 60 * 60 * 24 * 28

@app.on_event("startup")
async def expire_weekly():
    await redis.expire(weekly_key(), FOUR_WEEKS)

