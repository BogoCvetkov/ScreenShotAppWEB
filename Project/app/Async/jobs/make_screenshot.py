from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn
from Project.service.scraper.web_driver import BuildWebDriver
from rq.decorators import job
from Project.model.DB import Session
from Project.service.bots import CaptureBot
from Project.app.Async.callbacks import on_failed_job
from dotenv import load_dotenv


@job("client", connection=redis_conn, timeout="10m", failure_ttl="168h")
def capture_pages(acc_list, user=None):
    # Create a Session
    db_sess = Session()

    try:
        # Create the driver
        driver = BuildWebDriver(headless=True)
        driver.add_options("--no-sandbox")
        driver = driver.build_driver()

        # Instantiate a capture bot
        bot = CaptureBot(driver, db_sess, user)

        # Check for list of account id's in the request body
        if acc_list[0] == "all":
            status = bot.capture_all()
        else:
            status = bot.capture_from_list(acc_list)

        # Commit DB Session
        db_sess.commit()

        return status
    except Exception as e:
        db_sess.rollback()
        raise e
    finally:
        # Close Browser Session
        bot.close_driver()

        # Return session to pool
        Session.remove()