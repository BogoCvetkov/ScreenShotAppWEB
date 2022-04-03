from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn, redis_conn_d
from rq import Retry, Worker
from rq.decorators import job
from Project.model.DB import Session
from Project.service.bots import CaptureBot, EmailBot
from Project.service.scraper.web_driver import BuildWebDriver
from Project.app.Async.callbacks import on_failed_job
from Project.app.Async.queues import schedule_Q


@job("schedules", connection=redis_conn, timeout="5m", failure_ttl="168h", on_failure=on_failed_job,
     retry=Retry(max=3, interval=[10, 20]))
def send_scheduled_emails(acc_id, sess_name):
    # Create a Session
    db_sess = Session()

    # Connect to chrome session
    sess_id = redis_conn_d.hget("selenium", sess_name)
    web_driver = BuildWebDriver.reuse_session(sess_id)

    try:
        # Instantiate a capture bot
        c_bot = CaptureBot(web_driver, db_sess)

        # Capture account
        c_bot.capture_single(acc_id)

        # Commit DB Session - don't want to capture again in case of email fail
        db_sess.commit()

        # Instantiate an email bot
        e_bot = EmailBot(db_sess)

        # Send pdf to client
        e_bot.send_single(acc_id)

        # Commit DB Session
        db_sess.commit()

    except Exception as e:
        db_sess.rollback()

        raise e
    finally:
        # Close Browser Session if there are no more accounts in the queue
        if len(schedule_Q.job_ids) < 1 and len(schedule_Q.scheduled_job_registry.get_job_ids()) < 1:
            # Check for other active workers and the selenium session they use
            workers_sess = [w.get_current_job().args[1] for w in Worker.all(queue=schedule_Q) if w.get_current_job()]
            # If we have more than 1 active worker and the current session is not used in another worker - close it
            if len(workers_sess) > 1 and workers_sess.count(sess_name) < 2:
                web_driver.quit()

        # Return session to pool
        Session.remove()