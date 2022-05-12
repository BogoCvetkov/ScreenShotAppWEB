from redis import Redis
from rq.command import send_shutdown_command
from Project.app.Async.queues import *
from rq.command import send_stop_job_command

from rq.worker import Worker

redis = Redis()

workers = Worker.all(redis)

email_Q.empty()
screenshot_Q.empty()
schedule_Q.empty()
clean_up_Q.empty()
send_stop_job_command(redis,"33")
for worker in workers:
    send_shutdown_command(redis, worker.name)  # Tells worker to shutdown