from Project.model.all_models import AccountModel, LogModel
from Project.errors.custom_errors import AppServiceError
from datetime import datetime
import time, traceback


class BaseBot():
	bot_type="base"

	def __init__( self, db_sess, user=None ):
		self.db_sess = db_sess
		self.user = user
		self.status = { "fail_count": 0, "success": [], "failed": [],"skipped":[] }
		self.retry_list = []

	def _get_all_ad_accounts( self ):
		data = AccountModel.get_all( self.db_sess )
		return data

	def _get_ad_account_by_id( self, id ):
		data = AccountModel.get_by_id( self.db_sess, id )
		return data

	# Errors are not being handled
	def _run_for_one(self,account,method_to_call):
		try:
			info = method_to_call(account)
			message = f"Operation {method_to_call.__name__} for - {account.name} -  successful."
			self._update_status_and_log(account, message, info)
		except Exception as e:
			raise AppServiceError(e,origin=self.bot_type)

	# this private method consumes errors when processing accounts,
	# so that one fail doesn't affect the other accounts
	def _run_for_many(self, account, method_to_call):
		try:
			info = method_to_call( account )
			message = f"Operation {method_to_call.__name__} for - {account.name} -  successful."
			self._update_status_and_log(account, message, info)
		except:
			self.retry_list.append( account )

	# Using the already mapped objects from the DB - to save on querying again
	def _retry_on_failed( self, method_to_call ):
		if len( self.retry_list ) < 1: return

		# Wait before retrying
		time.sleep( 15 )
		for obj in self.retry_list:
			try:
				info = method_to_call( obj )
				message = f"Operation {method_to_call.__name__} for - {obj.name} -  successful."
				self._update_status_and_log(obj, message, info)
			except Exception as e:
				if isinstance( e, AppServiceError ):
					self._update_status_and_log(obj, e.message, e.details, failed=True)
				else:
					self._update_status_and_log(obj, "Unexpected Server Error",
												traceback.format_exc(), failed=True)

		self.retry_list = []

	# Logging the result of the operation to the Logs Table in DB
	def _log_operation_result( self, account, message, details, failed=False ):
		params = { "account_name": account.name, "log_msg": message, "log_details": details,
		           "date": datetime.now() }
		# Optional
		if failed: params["fail"] = True
		if self.user:
			params["user_id"] = self.user["id"]
			params["started_by"] = self.user["email"]

		new_log = LogModel( **params )
		account.logs.append( new_log )

	# Updating account info
	def _update_acc_info(self,account,failed=False):
		if (self.bot_type == "capture"):
			if failed:
				account.last_scrape_fail = True
			else:
				account.last_scraped = datetime.now()
				account.last_scrape_fail = False
		if (self.bot_type == "email"):
			if failed:
				account.last_email_fail = True
			else:
				account.last_emailed = datetime.now()
				account.last_email_fail = False

	# Updating the final status that the bot will return
	def _update_status_and_log(self, account, message, details, failed=False):
		if failed:
			self.status["failed"].append( { "account": account.name, "info": message } )
			self._log_operation_result( account, message, details, failed=True )
			self._update_acc_info(account,failed=True)
		else:
			self.status["success"].append( { "account": account.name, "info": message } )
			self._log_operation_result( account, message, details )
			self._update_acc_info(account)

		self.status["fail_count"] = len( self.status["failed"] )

	def update_and_log(self,account,message,details,failed=False):
		self._update_status_and_log(account,message,details,failed)