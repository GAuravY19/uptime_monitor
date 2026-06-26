from .database import get_connection


def get_all_websites():
    """
    Returns all websites that are currently under tracking.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                web_id,
                web_name,
                web_url
            FROM website_listing
            WHERE under_track = TRUE
            ORDER BY web_id;
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()


def get_previous_response(web_id):
    """
    Returns the latest response time recorded for a website.

    Returns:
        Integer response time
        OR
        None if no previous record exists.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT response_time_ms

            FROM website_tracking

            WHERE web_id = %s

            ORDER BY hit_timestamp DESC

            LIMIT 1;
        """, (web_id,))

        result = cursor.fetchone()

        if result is None:
            return None

        return result["response_time_ms"]

    finally:

        cursor.close()
        conn.close()


def insert_tracking(
        web_id,
        url,
        status,
        response_time,
        response_difference
):
    """
    Inserts one tracking record.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO website_tracking
            (
                web_id,
                url,
                status,
                response_time_ms,
                response_difference
            )

            VALUES
            (%s,%s,%s,%s,%s)
            """,
            (
                web_id,
                url,
                status,
                response_time,
                response_difference
            )
        )

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


from backend.database import get_connection


def get_recent_tracking(web_id=None, limit=30):
    """
    Returns the latest tracking records.

    Args:
        web_id : Filter records for a specific website.
                 If None, returns records for all websites.

        limit : Number of latest records.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        if web_id is None:

            cursor.execute(
                """
                SELECT

                    wl.web_id,
                    wl.web_name,

                    wt.url,
                    wt.status,
                    wt.response_time_ms,
                    wt.hit_timestamp,
                    wt.response_difference

                FROM website_tracking wt

                INNER JOIN website_listing wl

                ON wt.web_id = wl.web_id

                ORDER BY wt.hit_timestamp DESC

                LIMIT %s;
                """,
                (limit,)
            )

        else:

            cursor.execute(
                """
                SELECT

                    wl.web_id,
                    wl.web_name,

                    wt.url,
                    wt.status,
                    wt.response_time_ms,
                    wt.hit_timestamp,
                    wt.response_difference

                FROM website_tracking wt

                INNER JOIN website_listing wl

                ON wt.web_id = wl.web_id

                WHERE wl.web_id = %s

                ORDER BY wt.hit_timestamp DESC

                LIMIT %s;
                """,
                (
                    web_id,
                    limit
                )
            )

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

def get_all_websites():
    """
    Returns all registered websites.
    Used to populate the filter dropdown.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                web_id,
                web_name,
                web_url
            FROM website_listing
            ORDER BY web_name;
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()
