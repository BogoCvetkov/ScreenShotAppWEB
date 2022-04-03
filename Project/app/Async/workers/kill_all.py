from redis import Redis
from rq.command import send_shutdown_command
from Project.app.Async.queues import screenshot_Q,email_Q

from rq.worker import Worker

redis = Redis()

workers = Worker.all(redis)

email_Q.empty()
screenshot_Q.empty()
for worker in workers:
    send_shutdown_command(redis, worker.name)  # Tells worker to shutdown