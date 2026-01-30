from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    # total players
    total_players = r.zcard(LEADERBOARD_KEY)

    # get all scores
    scores = r.zrange(LEADERBOARD_KEY, 0, -1, withscores=True)

    # total score
    total_score = sum(score for _, score in scores)

    # top player
    top = r.zrevrange(LEADERBOARD_KEY, 0, 1, withscores=True)
    top_player = None
    if top:
        top_player = {
            "player": top[0][0],
            "score": top[0][1]
        }

    return {
        "total_players": total_players,
        "total_score": total_score,
        "top_player": top_player
    }

