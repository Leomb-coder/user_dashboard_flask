from psycopg2.extras import RealDictCursor

from db import get_connection

def create_user(name, email, password):
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id''', (name, email, password))
        conn.commit()

        user_id = cursor.fetchone()[0]
        return user_id

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def get_user_by_id(user_id):
    cursor = None
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT id, name, email FROM users WHERE id = %s''', (user_id,))
        return cursor.fetchone()

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def get_user_by_email(email):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
        return cursor.fetchone()

    except Exception:
        raise

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()