from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn
from rq.decorators import job
from Project.model.DB import Session
from Project.service.bots import EmailBot
from Project.app.Async.callbacks import on_failed_job


@job("client", connection=redis_conn, timeout="4m", failure_ttl="168h")
def send_result(json_body, user=None):
    # Create a DB Session
    db_sess = Session()

    try:
        # Instantiate an email bot
        bot = EmailBot(db_sess, user)

        # Execute operation for the ids
        status = bot.send_from_list(json_body)

        # Commit DB Session
        db_sess.commit()

        return status
    except Exception as e:
        db_sess.rollback()
        raise e
    finally:
        # Return session to pool
        Session.remove()