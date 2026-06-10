import os
import psycopg2

def get_connection():
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        cursor = conn.cursor()
        cursor.execute('''SELECT version();''')
        version = cursor.fetchone()

        print('Connected!')
        print(version)

    except psycopg2.Error as e:
        print(f'Database connection Error: {e}')

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()