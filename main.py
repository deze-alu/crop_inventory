import mysql.connector

import database as db


def main():
    conn = None
    try:
        conn = db.get_connection()
        print(f"Connected to {db.DB_NAME} on {db.SERVER_CONFIG['host']}.")
        db.create_tables(conn)
        print("Tables ready: crops, sales.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
