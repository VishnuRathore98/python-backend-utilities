from redis import Redis

r = Redis(host="localhost", port=6379, decode_responses=True)

import uuid


def create_user(name, age, email):
    user_id = str(uuid.uuid4())

    r.hset(
        f"user:{user_id}",
        mapping={"id": user_id, "name": name, "age": age, "email": email},
    )

    r.sadd("users", user_id)
    return user_id


def get_all_users():
    ids = r.smembers("users")
    return [r.hgetall(f"user:{uid}") for uid in ids]


def get_user(user_id):
    return r.hgetall(f"user:{user_id}")


uid = create_user("John", 25, "john@test.com")
print(get_user(uid))
