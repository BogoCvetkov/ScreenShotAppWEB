from rq import Worker
from redis import Redis
from rq import SimpleWorker
from rq.timeouts import TimerDeathPenalty

class WindowsSimpleWorker(SimpleWorker):
    death_penalty_class = TimerDeathPenalty

redis_conn=Redis(host="localhost")

worker = WindowsSimpleWorker(["client"], connection=redis_conn)

if __name__ == "__main__":
    worker.work()