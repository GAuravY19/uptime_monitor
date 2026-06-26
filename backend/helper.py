import time
import requests

from .database import get_connection


def generate_web_id():
    """
    Generates a new WebID in the format:
    WEB_01, WEB_02, WEB_03, ...
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT web_id
            FROM website_listing
            ORDER BY CAST(SUBSTRING(web_id FROM '[0-9]+') AS INTEGER) DESC
            LIMIT 1;
        """)

        result = cursor.fetchone()

        if result is None:
            return "WEB_01"

        last_web_id = result["web_id"]      # Example: WEB_07
        last_number = int(last_web_id.split("_")[1])

        new_number = last_number + 1

        return f"WEB_{new_number:02d}"

    finally:
        cursor.close()
        conn.close()


def hit_website(url: str):
    """
    Hits the given URL and returns

    Returns:
        (
            status,
            response_time_ms
        )
    """

    try:

        start = time.perf_counter()

        response = requests.get(
            url,
            timeout=10
        )

        end = time.perf_counter()

        response_time = round((end - start) * 1000)

        if response.status_code < 400:
            status = "UP"
        else:
            status = "DOWN"

    except requests.exceptions.RequestException:

        status = "DOWN"
        response_time = None

    return (
        status,
        response_time
    )
