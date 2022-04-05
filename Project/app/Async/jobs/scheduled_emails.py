import time

from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn, redis_conn_d
from rq import Retry, Worker
from rq.decorators import job
from rq.command import send_command
from Project.model.DB import Session
from Project.service.bots import CaptureBot, EmailBot
from Project.service.scraper.web_driver import BuildWebDriver
from Project.app.Async.callbacks import on_failed_job
from Project.app.Async.queues import screenshot_Q, schedule_Q, email_Q
from Project.app.Async.jobs.clean_up import close_browser_sessions


@job("schedules", connection=redis_conn, timeout="5m", failure_ttl="168h", on_failure=on_failed_job,
     retry=Retry(max=3, interval=[10, 20]))
def send_scheduled_emails(acc_id, sess_name):
    # Create a Session
    db_sess = Session()

    # If account is being processed by workers of the email queue - command them to cancel it
    if str(acc_id) in extract_active_jobs(email_Q):
        return
        # cancel_email_job(acc_id) not on Windows, IMPLEMENT IT WHEN DEPLOYING on SERVER

    # If account is being processed by workers of the screenshot queue - wait for them
    while str(acc_id) in extract_active_jobs(screenshot_Q):
        time.sleep(1)
        redis_conn.hset("stat", "wait", "YES")
    redis_conn.hset("stat", "wait", "NO")

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
        # If no more accounts in the queues, schedule a clean_up job for closing the sessions
        if len(schedule_Q.job_ids) < 1 and len(schedule_Q.scheduled_job_registry.get_job_ids()) < 1:
            close_browser_sessions.delay()

        # Return session to pool
        Session.remove()


# helper function
def extract_active_jobs(queue):
    id_list = []
    started_job_ids = queue.started_job_registry.get_job_ids()

    for job_ids in started_job_ids:
        id_list.extend(job_ids.split(","))

    return id_list


# Not working on windows - NOT yet implemented
def cancel_email_job(job_id):
    email_job_id = str(job_id) + ","
    job = email_Q.fetch_job(email_job_id)
    send_command(redis_conn, job.worker_name, "stop-job", job_id=email_job_id)