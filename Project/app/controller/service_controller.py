from Project.service.bots import CaptureBot, EmailBot
from Project.model.DB import Session
from flask import request, jsonify
from flask_jwt_extended import current_user
from Project.app.Async.jobs.make_screenshot import capture_pages
from Project.app.Async.jobs.send_emails import send_email
from Project.app.Async.queues import screenshot_Q, email_Q
from Project.errors.custom_errors import AppServiceError

''''
Services logic:
    - screenshots - taking screenshots opens a browser, which is an expensive operation. So to optimize this, 
                    accounts are screenshootet in bulk in a single browser session - multiple id's [up to 5] 
                    are allowed per request.
    - emails - only a single email is processed at a time (more robust and reliable). Single id per request is
                allowed. We want to be sure that the recipient doesn't get an email two times.
    * accounts in queue for the first service always check if they are being processed in the second one and vice versa.
      Both services are operating on the same file, so this way they should sync with one another.
                    
'''


# Helper Func
def filter_accounts(queue, initial_list, max_entries):
    # Check user input
    if not isinstance(initial_list, list):
        raise AppServiceError("/id_list/ field must be a list", 400)

    # Check if the number of id's is greater than the allowed
    if len(initial_list) > max_entries:
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


# Controllers

# /service/?type=scrape
def capture_accounts():
    acc_list = filter_accounts(queue=email_Q, initial_list=request.json["id_list"], max_entries=5)
    email_queued = set(request.json["id_list"]).difference(set(acc_list))
    if email_queued:
        raise AppServiceError(f"Accounts with id's - {email_queued} are being emailed currently. "
                              f"Wait for them if you want to send them for screenshots.")

    acc_list = filter_accounts(queue=screenshot_Q, initial_list=request.json["id_list"], max_entries=5)

    # Send a job to the queue if there are any accounts after filtration
    if len(acc_list):
        job_id = ""
        for id in acc_list: job_id += f"{id},"
        user = { "id": current_user.id, "email": current_user.email }
        job_proxy = capture_pages.delay(acc_list=acc_list, user=user, job_id=job_id)

    # Send the response that the job was send to the queue
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": screenshot_Q.job_ids,
                      "executing": screenshot_Q.started_job_registry.get_job_ids() } }), 200


# /service/?type=email
def send_emails():
    acc_list = filter_accounts(queue=email_Q, initial_list=request.json["id_list"], max_entries=1)
    if not acc_list:
        raise AppServiceError("This account is currently being emailed to.")
    acc_list = filter_accounts(queue=screenshot_Q, initial_list=acc_list, max_entries=1)
    if not acc_list:
        raise AppServiceError("This account is currently in queue for a screenshot. Wait a bit and try again.")

    # Send a job to the queue if there are any accounts after filtration
    if len(acc_list):
        job_id = ""
        for id in acc_list: job_id += f"{id},"
        user = { "id": current_user.id, "email": current_user.email }
        job_proxy = send_email.delay(acc_list=acc_list, user=user, job_id=job_id)

    # Send the status of the operation
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": email_Q.job_ids, "executing": email_Q.started_job_registry.get_job_ids() } }), 200

# def send_emails():
# 	# Create a DB Session
# 	db_sess = Session()
#
# 	# Instantiate a email bot
# 	bot = EmailBot( db_sess, current_user )
#
# 	# Check for list of account id's in the body
# 	if isinstance( request.json["id_list"], list ):
# 		status = bot.send_from_list( request.json["id_list"] )
#
# 	# Or send to all accounts
# 	if request.json["id_list"] == "all":
# 		status = bot.send_all()
#
# 	# Commit DB Session
# 	db_sess.commit()
#
# 	# Send the status of the operation
# 	return jsonify(
# 		{ "status": "success", "msg": "Emailing Completed", "result": status } ), 200