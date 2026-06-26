import os

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_connection():
    """
    Creates and returns a PostgreSQL database connection.
    """

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )

    return connection


# def test_connection():
#     """
#     Tests the database connection.
#     """

#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute("SELECT version();")
#         version = cursor.fetchone()

#         print("Connected to PostgreSQL")

#         cursor.close()
#         conn.close()

#     except Exception as e:
#         print("Database Connection Failed")
#         print(e)

# if __name__ == "__main__":
#     test_connection()
