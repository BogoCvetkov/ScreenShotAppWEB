import time

from rq import Queue
from Project.app.Async.redis_conn import redis_conn
from Project.errors.custom_errors import AppServiceError

screenshot_Q = Queue("screenshots", connection=redis_conn)
email_Q = Queue("emails", connection=redis_conn)
schedule_Q = Queue("schedules", connection=redis_conn)
clean_up_Q = Queue("clean_up", connection=redis_conn)


# Used for email and client queue
def filter_accounts_from_queue(queue, initial_list, max_entries=None):
    # Check user input
    if not isinstance(initial_list, list):
        raise AppServiceError("/id_list/ field must be a list", 400)

    # Check if the number of id's is greater than the allowed
    if max_entries and len(initial_list) > max_entries:
        raise AppServiceError(f"Max list size exceeded = {max_entries} ")

    # remove duplicates with a set
    acc_list = list(set(initial_list))

    # Skip accounts that have already been queued for execution
    for id_list in queue.job_ids:
        # faster lookup for sets - O(n)
        id_list = set(id_list.split(","))
        acc_list = list(filter(lambda n: str(n) not in id_list, acc_list))

    # Skip accounts that are currently being executed
    for id_list in queue.started_job_registry.get_job_ids():
        id_list = set(id_list.split(","))
        acc_list = list(filter(lambda n: str(n) not in id_list, acc_list))

    return acc_list


# Jobs in schedules queue are structured differently - single id per job and retry on fail.
# This calls for a separate function for filtering
def filter_accounts_from_schedule_queue(acc_list):
    # Skip accounts that have been queued for execution by by workers of the schedule queue
    acc_list = list(filter(lambda n: str(n) not in schedule_Q.job_ids, acc_list))

    # Skip accounts that are currently being executed by workers of the schedule queue
    acc_list = list(filter(lambda n: str(n) not in schedule_Q.started_job_registry.get_job_ids(), acc_list))

    # Skip accounts that are scheduled for retry
    acc_list = list(filter(lambda n: str(n) not in schedule_Q.scheduled_job_registry.get_job_ids(), acc_list))

    return acc_list