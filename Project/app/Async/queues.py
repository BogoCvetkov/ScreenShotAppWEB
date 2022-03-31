from rq import Queue
from Project.app.Async.redis_conn import redis_conn

screenshot_Q = Queue("screenshots", connection=redis_conn)
email_Q = Queue("emails", connection=redis_conn)
schedule_Q = Queue("schedules", connection=redis_conn)