from rq import Queue
from Project.app.Async.redis_conn import redis_conn

client_Q = Queue("client", connection=redis_conn )