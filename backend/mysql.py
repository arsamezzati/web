import pymysql.cursors
from pymysql.connections import Connection
from contextlib import contextmanager

# Database configuration
db_config = {
    "host": "mysql",
    "user": "gameuser",
    "password": "gamepassword",
    "database": "gametracker",
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor
}

# Create a connection pool
def get_connection():
    return pymysql.connect(**db_config)

@contextmanager
def get_db():
    conn = None
    try:
        conn = get_connection()
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()