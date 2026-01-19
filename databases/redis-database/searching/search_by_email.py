import redis
import uuid


def create_user(name, age, email):
    email_key = f"email:{email}"

    # prevent duplicate email
    if r.exists(email_key):
        raise ValueError("Email already exists")

    user_id = str(uuid.uuid4())

    r.hset(
        f"user:{user_id}",
        mapping={"id": user_id, "name": name, "age": age, "email": email},
    )

    r.sadd("users", user_id)
    r.set(email_key, user_id)

    return user_id


def get_user_by_email(email):
    user_id = r.get(f"email:{email}")
    if not user_id:
        return None
    return r.hgetall(f"user:{user_id}")


def update_user(user_id, **fields):
    user_key = f"user:{user_id}"

    if "email" in fields:
        old_email = r.hget(user_key, "email")
        new_email = fields["email"]

        if old_email != new_email:
            if r.exists(f"email:{new_email}"):
                raise ValueError("Email already exists")

            r.delete(f"email:{old_email}")
            r.set(f"email:{new_email}", user_id)

    r.hset(user_key, mapping=fields)


def delete_user(user_id):
    user_key = f"user:{user_id}"
    email = r.hget(user_key, "email")

    r.delete(user_key)
    r.srem("users", user_id)

    if email:
        r.delete(f"email:{email}")


uid = create_user("Alice", 28, "alice@test.com")

print(get_user_by_email("alice@test.com"))
print(get_user_by_email("missing@test.com"))  # None
