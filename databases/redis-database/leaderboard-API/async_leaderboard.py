from fastapi import APIRouter, HTTPException
from redis.asyncio import Redis

router = APIRouter()

redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

LEADERBOARD_KEY = "game:leaderboard"

@router.post("/score/increment")
async def increment_score(player: str, points: int = 1):
    new_score = await redis.zincrby(
        LEADERBOARD_KEY,
        points,
        player
    )

    return {
        "player": player,
        "new_score": new_score
    }


@router.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    players = await redis.zrevrange(
        LEADERBOARD_KEY,
        0,
        limit - 1,
        withscores=True
    )

    return [
        {"rank": i + 1, "player": name, "score": score}
        for i, (name, score) in enumerate(players)
    ]

@router.get("/rank/{player}")
async def get_rank(player: str):
    rank = await redis.zrevrank(LEADERBOARD_KEY, player)
    score = await redis.zscore(LEADERBOARD_KEY, player)

    if rank is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "player": player,
        "rank": rank + 1,
        "score": score
    }

