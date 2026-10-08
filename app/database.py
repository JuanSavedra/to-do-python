import sqlite3

def get_db_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

def get_endpoint_connection():
    con = get_db_connection()

    try:
        yield con
    finally:
        con.close()

def init_db():
    con = get_db_connection()
    cur = con.cursor()

    try:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS Task
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    status INTEGER NOT NULL DEFAULT 0
                )
            '''
        )

        con.commit()
    finally:
        con.close()