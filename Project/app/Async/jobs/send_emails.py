import time

from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn
from rq.decorators import job
from Project.model.DB import Session
from Project.service.bots import EmailBot
from Project.app.Async.callbacks import on_failed_job
from Project.app.Async.queues import filter_accounts_from_schedule_queue
from Project.app.Async.utils import send_event


@job("emails", connection=redis_conn, timeout="1m", failure_ttl="168h")
def send_email(initial_list, user=None):
    # Check again and filter accounts being handled by workers of the schedule queue
    filtered_list = filter_accounts_from_schedule_queue(initial_list)

    if len(filtered_list) < 1: return

    # Create a DB Session
    db_sess = Session()

    try:
        # Instantiate an email bot
        bot = EmailBot(db_sess, user)

        # Execute operation for the ids
        status = bot.send_from_list(filtered_list)

        # Commit DB Session
        db_sess.commit()

        return send_event(status)
    except Exception as e:
        db_sess.rollback()
        raise e
    finally:
        # Return session to pool
        Session.remove()