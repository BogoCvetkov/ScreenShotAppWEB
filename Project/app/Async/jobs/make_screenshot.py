import time

from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn
from Project.service.scraper.web_driver import BuildWebDriver
from rq.decorators import job
from Project.model.DB import Session
from Project.service.bots import CaptureBot
from Project.model.logs_model import LogModel
from Project.app.Async.queues import filter_accounts_from_schedule_queue


@job("screenshots", connection=redis_conn, timeout="10m", failure_ttl="168h")
def capture_pages(initial_list, user=None):
    # Check again and filter accounts being handled by workers of the schedule queue
    filtered_list = filter_accounts_from_schedule_queue(initial_list)

    if len(filtered_list) < 1: return

    # Create a Session
    db_sess = Session()

    # Create the driver
    driver = BuildWebDriver(headless=True)
    driver.add_options("--no-sandbox")

    try:
        # Open browser instance
        driver = driver.build_driver()

        # Instantiate a capture bot
        bot = CaptureBot(driver, db_sess, user)

        # Check for list of account id's in the request body
        if filtered_list[0] == "all":
            status = bot.capture_all()
        else:
            status = bot.capture_from_list(filtered_list)

        # Commit DB Session
        db_sess.commit()

        return status
    except Exception as e:
        db_sess.rollback()
        raise e
    finally:
        # Close Browser Session
        driver.quit()

        # Return session to pool
        Session.remove()