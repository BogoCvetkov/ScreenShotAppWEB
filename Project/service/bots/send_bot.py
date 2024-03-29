from Project.service.utils.email_sender import EmailSender
from Project.service.bots.base import BaseBot


class EmailBot( BaseBot ):
	bot_type = "email"

	def __init__( self, db_sess, user=None ):
		super().__init__( db_sess, user )

	def send_all( self ):
		accounts = self._get_all_ad_accounts()
		for account in accounts:
			self._run_for_many(account, self._send_email)
		self._retry_on_failed( self._send_email )
		return self.status

	# Runs for multiple accounts - exception on single account must not affect the others
	def send_from_list( self, id_list ):
		for id in id_list:
			account = self._get_ad_account_by_id( id )
			if account:
				self._run_for_many(account, self._send_email)
		self._retry_on_failed( self._send_email )
		return self.status

	# Runs for single account - Exceptions are not being handled
	def send_single(self,id):
		account = self._get_ad_account_by_id(id)
		if account:
			self._run_for_one(account,self._send_email)


	def _send_email( self, account ):
		email = EmailSender()
		email.build_mail( recipient=account.email, attachment=account.screenshot.file_dir,
		                  body=account.email_body )
		email.send_mail()
		return