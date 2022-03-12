from Project.app.service.bots import CaptureBot, EmailBot
from Project.app.model import Session
from flask import request, jsonify
from Project.app.service.scraper.web_driver import BuildWebDriver

from Project.app.model.all_models import UserModel




# /
def capture_accounts():
	# Create a Session
	db_sess = Session()

	# Create the driver
	driver = BuildWebDriver( headless=False ).build_driver()

	test_user = UserModel.get_by_id( db_sess, 19 )

	# Instantiate a capture bot
	bot = CaptureBot( test_user, driver, db_sess )

	# Check for list of account id's in the body
	if isinstance( request.json["id_list"], list ):
		status = bot.capture_from_list( request.json["id_list"] )

	# Or capture all accounts
	if request.json["id_list"] == "all":
		status = bot.capture_all()

	# Close Browser Session
	bot.close_driver()

	# Commit DB Session
	db_sess.commit()

	# Send the status of the operation
	return jsonify(
		{ "status": "success", "msg": "Scraping Completed", "result": status } ), 200


def send_emails():
	# Create a DB Session
	db_sess = Session()

	test_user = UserModel.get_by_id( db_sess, 19 )

	# Instantiate a email bot
	bot = EmailBot( db_sess, test_user )

	# Check for list of account id's in the body
	if isinstance( request.json["id_list"], list ):
		status = bot.send_from_list( request.json["id_list"] )

	# Or send to all accounts
	if request.json["id_list"] == "all":
		status = bot.send_all()

	# Commit DB Session
	db_sess.commit()

	# Send the status of the operation
	return jsonify(
		{ "status": "success", "msg": "Emailing Completed", "result": status } ), 200