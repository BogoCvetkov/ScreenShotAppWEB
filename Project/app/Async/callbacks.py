from dotenv import load_dotenv
from rq import Worker

load_dotenv("Project/.env")

from Project.model.DB import Session
from Project.errors.custom_errors import AppServiceError
from Project.model.all_models import AccountModel
from Project.service.bots import CaptureBot, EmailBot
from Project.app.Async.queues import schedule_Q
from Project.service.scraper.web_driver import BuildWebDriver
import traceback


def on_failed_job(job, connection, type, value, tracebackinfo):
    # Create a Session
    db_sess = Session()

    try:

        # Log failed operation
        account = AccountModel.get_by_id(db_sess, job.id)

        if isinstance(value, AppServiceError):
            if hasattr(value, "origin") and value.origin == "capture":
                CaptureBot(db_sess, "").update_and_log(account, str(value.message), value.details, failed=True)
            message = f"Sheduled email failed for {account.email}. Reason: {value.message}"
            EmailBot(db_sess).update_and_log(account, message, value.details, failed=True)

        else:
            EmailBot(db_sess).update_and_log(account,
                                             f"Sheduled email failed for account {account.email}. Reason: Unexpected server error",
                                             traceback.format_exception(value), failed=True)

        db_sess.commit()
    except Exception as e:
        db_sess.rollback()

        raise e
    finally:

        # Return session to DB pool
        Session.remove()