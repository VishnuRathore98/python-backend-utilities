# leaderboard for a game
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Clear old leaderboard
r.delete("game_leaderboard")

# Add players
r.zadd("game_leaderboard", {
    "Alice": 50,
    "Bob": 80,
    "Carol": 65
})

# Increase Alice's score
r.zincrby("game_leaderboard", 20, "Alice")

# Show top 3
print("Top players:")
for name, score in r.zrevrange("game_leaderboard", 0, 2, withscores=True):
    print(name, score)

# Show Alice rank
rank = r.zrevrank("game_leaderboard", "Alice")
print("Alice rank:", rank + 1)

