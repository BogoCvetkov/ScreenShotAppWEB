from rq import Worker

from Project.service.bots import CaptureBot, EmailBot
from Project.service.scraper.web_driver import BuildWebDriver
from Project.model.DB import Session
from flask import request, jsonify
from flask_jwt_extended import current_user
from Project.app.Async.jobs.make_screenshot import capture_pages
from Project.app.Async.jobs.send_emails import send_email
from Project.app.Async.jobs.scheduled_emails import send_scheduled_emails
from Project.app.Async.queues import screenshot_Q, email_Q, schedule_Q, filter_accounts_from_queue, \
    filter_accounts_from_schedule_queue
from Project.app.Async.redis_conn import redis_conn_d
from Project.errors.custom_errors import AppServiceError

''''
Services logic:
    - The structure of the Async operations is based on hierarchy. Currently two types of Queues exist. The first are 
     handling client-side commands send from users - those are the /emails and screenshots/ queues. The second type is
     the queue that executes scheduled jobs - the /schedules/ queue:
        - Schedules queue has higher priority than the others
        - If the same job is queued for the 2 types of queues at the same time - those in the /schedules/ queue
        will be executed and the rest will be skipped
        -If execution of a job has already started in a lower priority queue(the first type) - the same job in the 
        /schedule/ queue will either wait for it/screenshots/ or cancel it/emails/.
    - screenshots - taking screenshots opens a browser, which is an expensive operation. So to optimize this, 
                    accounts are screenshootet in bulk in a single browser session - multiple id's [up to 5] 
                    are allowed per request.
    - emails - only a single email is processed at a time (more robust and reliable). Single id per request is
                allowed. We want to be sure that the recipient doesn't get an email two times.
    
    * accounts in queue for the first service always check if they are being processed in the second one and vice versa.
      Both services are operating on the same file, so this way they should sync with one another.
                    
'''


# /service/?type=scrape
def capture_accounts():
    # 1. Check if accounts are being queued for emailing
    acc_list = filter_accounts_from_queue(queue=email_Q, initial_list=request.json["id_list"], max_entries=5)
    queued_for_email = set(request.json["id_list"]).difference(set(acc_list))
    if queued_for_email:
        raise AppServiceError(f"Accounts with id's - {queued_for_email} are being emailed currently. "
                              f"Wait for them if you want to send them for screenshots.")

    # 2. Filter accounts already in the queue for screenshots
    acc_list = filter_accounts_from_queue(queue=screenshot_Q, initial_list=request.json["id_list"], max_entries=5)

    # 3. Filter accounts that are being handled currently by workers of the schedule queue
    acc_list = filter_accounts_from_schedule_queue(acc_list)

    # Send a job to the queue if there are any accounts after filtration
    if len(acc_list):
        job_id = ""
        for id in acc_list: job_id += f"{id},"
        user = { "id": current_user.id, "email": current_user.email }
        capture_pages.delay(initial_list=acc_list, user=user, job_id=job_id)

    # Send the response that the job was send to the queue
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": screenshot_Q.job_ids,
                      "executing": screenshot_Q.started_job_registry.get_job_ids() } }), 200


# /service/?type=email
def send_emails():
    acc_list = filter_accounts_from_queue(queue=email_Q, initial_list=request.json["id_list"], max_entries=1)
    if not acc_list:
        raise AppServiceError("This account is currently being emailed to.")
    acc_list = filter_accounts_from_queue(queue=screenshot_Q, initial_list=acc_list, max_entries=1)
    if not acc_list:
        raise AppServiceError("This account is currently in queue for a screenshot. Wait a bit and try again.")
    acc_list = filter_accounts_from_schedule_queue(acc_list)
    if not acc_list:
        raise AppServiceError("This account is currently or soon to be emailed by the schedule bot")

    # Send a job to the queue if there are any accounts after filtration
    if len(acc_list):
        job_id = ""
        for id in acc_list: job_id += f"{id},"
        user = { "id": current_user.id, "email": current_user.email }
        send_email.delay(initial_list=acc_list, user=user, job_id=job_id)

    # Send the status of the operation
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": email_Q.job_ids, "executing": email_Q.started_job_registry.get_job_ids() } }), 200


# /service/?type=test - for testing the schedule job functionality
def test_schedule():
    driver_1 = BuildWebDriver(headless=False).build_remote_driver()
    driver_2 = BuildWebDriver(headless=False).build_remote_driver()

    redis_conn_d.hset("selenium", "session_1", driver_1.session_id)
    redis_conn_d.hset("selenium", "session_2", driver_2.session_id)

    for i in range(len(request.json["id_list"])):
        if i % 2 != 0:
            send_scheduled_emails.delay(request.json["id_list"][i], "session_2", job_id=str(request.json["id_list"][i]))
        else:
            send_scheduled_emails.delay(request.json["id_list"][i], "session_1", job_id=str(request.json["id_list"][i]))

    # Send the status of the operation
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": schedule_Q.job_ids, "executing": schedule_Q.started_job_registry.get_job_ids() },
          "failed": schedule_Q.failed_job_registry.get_job_ids(),
          "scheduled": schedule_Q.scheduled_job_registry.get_job_ids() }, ), 200