import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="learn_pg",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost",
        port="5432"
    )

def create_user(name, email, age):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name, email, age)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (name, email, age))

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_all_users():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def get_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row

