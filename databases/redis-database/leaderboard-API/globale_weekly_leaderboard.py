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

