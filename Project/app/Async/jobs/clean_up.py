from dotenv import load_dotenv

load_dotenv("Project/.env")

from Project.app.Async.redis_conn import redis_conn
from rq.decorators import job
from Project.app.Async.queues import schedule_Q, clean_up_Q
from Project.service.scraper.web_driver import BuildWebDriver
from datetime import timedelta

@job("clean_up", connection=redis_conn, timeout="30s", failure_ttl="24h")
def close_browser_sessions():
    def inner():
        queued_jobs = schedule_Q.job_ids
        executing_jobs = schedule_Q.started_job_registry.get_job_ids()
        retry_jobs = schedule_Q.scheduled_job_registry.get_job_ids()

        # If all jobs have finished processing, close selenium sessions
        if len(queued_jobs) < 1 and len(executing_jobs) < 1 and len(retry_jobs) < 1:
            BuildWebDriver.close_all_sessions()

        # If not, requeue again in 10 seconds
        else:
            clean_up_Q.enqueue_in(timedelta(10),inner,timeout="30s",failure_ttl="24h")

    inner()


    # TEST CASE [69,57,55,44]

    # while True:
    #     time.sleep(2)
    #     print(f"In Queue: {schedule_Q.job_ids}")
    #     print(f"Executing: {schedule_Q.started_job_registry.get_job_ids()}")
    #     print(f"Retry: {schedule_Q.scheduled_job_registry.get_job_ids()}")
    #     print(f"Clean_up: {clean_up_Q.job_ids}")
    #     print(f"Clean_up executing: {clean_up_Q.started_job_registry.get_job_ids()}")
    #     print("-------------------")