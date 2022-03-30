from Project.service.bots import CaptureBot, EmailBot
from Project.model.DB import Session
from flask import request, jsonify
from flask_jwt_extended import current_user
from Project.app.Async.jobs.make_screenshot import capture_pages
from Project.app.Async.jobs.send_emails import send_result
from Project.app.Async.queues import client_Q
from Project.errors.custom_errors import AppServiceError


# /service/?type=scrape
def capture_accounts():
    # Check user input
    if not isinstance(request.json["id_list"], list):
        raise AppServiceError("/id_list/ field must be a list", 400)

    # remove duplicates with a set
    acc_list = list(set(request.json["id_list"]))

    # Skip accounts that have already been queued for execution
    for id_list in client_Q.job_ids:
        id_list = id_list.split(",")
        acc_list = list(filter(lambda n: str(n) not in id_list, acc_list))

    # Skip accounts that are currently being executed
    for id_list in client_Q.started_job_registry.get_job_ids():
        id_list = id_list.split(",")
        acc_list = list(filter(lambda n: str(n) not in id_list, acc_list))

    # Send a job to the queue if there are any accounts after filtration
    if len(acc_list):
        job_id = ""
        for id in acc_list: job_id += f"{id},"
        job = capture_pages.delay(acc_list=acc_list, job_id=job_id)

    # Send the response that the job was send to the queue
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.",
          "result": { "waiting": client_Q.job_ids, "executing": client_Q.started_job_registry.get_job_ids() } }), 200


# /service/?type=email
def send_emails():
    # Send a job to the queue
    job_id = f"email_{current_user.id}"
    job = send_result.delay(json_body=request.json["id_list"], job_id=job_id)

    # Send the status of the operation
    return jsonify(
        { "status": "success", "msg": "Job registered. The bot will be on it soon.", "result": job.id }), 200

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