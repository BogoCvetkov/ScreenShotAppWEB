from Project.app.model.all_models import AccountModel, LogModel
from Project.app.errors import AppServiceError
from datetime import datetime
import time, traceback


class BaseBot():

	def __init__( self, db_sess, user ):
		self.db_sess = db_sess
		self.user = user
		self.status = { "fail_count": 0, "success": [], "failed": [] }
		self.retry_list = []

	def _get_all_ad_accounts( self ):
		data = AccountModel.get_all( self.db_sess )
		return data

	def _get_ad_account_by_id( self, id ):
		data = AccountModel.get_by_id( self.db_sess, id )
		return data

	def _run_with_status( self, account, method_to_call ):
		try:
			info = method_to_call( account )
			message = f"Operation {method_to_call.__name__} for - {account.name} -  successful."
			self._update_and_log_status( account, message, info )
		except:
			self.retry_list.append( account )
		finally:
			self._retry_on_failed( method_to_call )

	# Using the already mapped objects from the DB - to save on querying again
	def _retry_on_failed( self, method_to_call ):
		if len( self.retry_list ) < 1: return

		# Wait before retrying
		time.sleep( 15 )
		for obj in self.retry_list:
			try:
				info = method_to_call( obj )
				message = f"Operation {method_to_call.__name__} for - {obj.name} -  successful."
				self._update_and_log_status( obj, message, info )
			except Exception as e:
				if isinstance( e, AppServiceError ):
					self._update_and_log_status( obj, e.message, e.details, failed=True )
				else:
					self._update_and_log_status( obj, "Unexpected Server Error",
					                             traceback.format_exc(), failed=True )

		self.retry_list = []

	# Logging the result of the operation to the Logs Table in DB
	def _log_operation_result( self, account, message, details, failed=False ):
		params = { "started_by": self.user.username, "account_name": account.name,
		           "log_msg": message, "log_details": details,"date":datetime.now() }
		# Optional
		if failed: params["fail"] = True
		if hasattr( self.user, "id" ): params["user_id"] = self.user.id

		new_log = LogModel( **params )
		account.logs.append( new_log )

	def _update_and_log_status( self, account, message, details, failed=False ):
		if failed:
			self.status["failed"].append( { "account": account.name, "info": message } )
			self._log_operation_result( account, message, details, failed=True )
		else:
			self.status["success"].append( { "account": account.name, "info": message } )
			self._log_operation_result( account, message, details )

		self.status["fail_count"] = len( self.status["failed"] )