import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            score INTEGER,
            xcount INTEGER,
            class TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_student(first_name, last_name, score, xcount, class_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (first_name, last_name, score, xcount, class)
        VALUES (%s, %s, %s, %s, %s)
    """, (first_name, last_name, score, xcount, class_name))
    conn.commit()
    conn.close()

def get_student(first_name, last_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT first_name, last_name, score, xcount, class
        FROM students
        WHERE first_name=%s AND last_name=%s
        ORDER BY id DESC LIMIT 1
    """, (first_name, last_name))
    result = cur.fetchone()
    conn.close()
    return result
