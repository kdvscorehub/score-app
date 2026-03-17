import sqlite3

DB_FILE = 'score_app.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            score INTEGER,
            xcount INTEGER,
            class TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_student(first_name, last_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name, score, xcount, class FROM students WHERE first_name=? AND last_name=?',
                   (first_name, last_name))
    result = cursor.fetchone()
    conn.close()
    return result

def save_student(first_name, last_name, score, xcount, class_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Check if exists
    cursor.execute('SELECT id FROM students WHERE first_name=? AND last_name=?', (first_name, last_name))
    row = cursor.fetchone()
    if row:
        cursor.execute('''
            UPDATE students SET score=?, xcount=?, class=? WHERE id=?
        ''', (score, xcount, class_name, row[0]))
    else:
        cursor.execute('''
            INSERT INTO students (first_name, last_name, score, xcount, class)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, score, xcount, class_name))
    conn.commit()
    conn.close()
