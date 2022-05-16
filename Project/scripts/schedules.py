from dotenv import load_dotenv

load_dotenv(".env")

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from Project.model.all_models import ScheduleModel
from Project.model.DB import Session
from Project.service.scraper.web_driver import BuildWebDriver
from Project.app.Async.redis_conn import redis_conn_d
from Project.app.Async.jobs.scheduled_emails import send_scheduled_emails

sched = BlockingScheduler()


# This runs as a daemon process on the server. It runs at every hour and checks
#  if there are scheduled jobs at that time, that should be enqueued for processing
@sched.scheduled_job("cron", hour="*")
def print_hour():
    # Get the day and hour
    week_day = datetime.now().weekday()
    hour = datetime.now().hour

    # print(datetime.now())
    # print(week_day, hour)

    try:
        # Create a Session
        db_sess = Session()

        # Get all Scheduled jobs
        scheduled_accounts = ScheduleModel.search_schedules(db_sess, hour=hour, weekday=week_day)

        if len(scheduled_accounts) > 0:
            # Get the id's of the accounts for those jobs
            id_list = [sched.account_id for sched in scheduled_accounts]

            # Instantiate two selenium browser instances
            driver_1 = BuildWebDriver(headless=True).build_remote_driver()
            driver_2 = BuildWebDriver(headless=True).build_remote_driver()

            # Save the session id's to be used later by the workers in Redis
            redis_conn_d.hset("selenium", "session_1", driver_1.session_id)
            redis_conn_d.hset("selenium", "session_2", driver_2.session_id)

            # Distribute the sessions evenly and send the jobs
            for i in range(len(id_list)):
                if i % 2 != 0:
                    send_scheduled_emails.delay(id_list[i], "session_2", job_id=str(id_list[i]))
                else:
                    send_scheduled_emails.delay(id_list[i], "session_1", job_id=str(id_list[i]))
    except Exception as e:
        db_sess.rollback()
        raise e
    finally:
        # Return session to pool
        Session.remove()


# Start the process
sched.start()