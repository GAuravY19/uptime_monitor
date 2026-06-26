import threading
import time

from .crud import get_all_websites, get_previous_response, insert_tracking

from backend.helper import hit_website

def monitor_websites():
    """
    Background job that continuously monitors
    all tracked websites every 60 seconds.
    """

    while True:

        print("Checking websites...")

        websites = get_all_websites()

        for website in websites:

            web_id = website["web_id"]
            url = website["web_url"]

            status, current_response = hit_website(url)

            previous_response = get_previous_response(web_id)

            # First time tracking
            if (
                previous_response is None or
                current_response is None
            ):
                response_difference = None

            else:
                response_difference = (
                    current_response -
                    previous_response
                )

            insert_tracking(
                web_id=web_id,
                url=url,
                status=status,
                response_time=current_response,
                response_difference=response_difference
            )

        print("Cycle Completed")

        # Wait for 1 minute
        time.sleep(60)


def start_scheduler():
    """
    Starts the scheduler in a background thread.
    """

    scheduler_thread = threading.Thread(
        target=monitor_websites,
        daemon=True
    )

    scheduler_thread.start()

    print("Website Monitoring Scheduler Started.")
