from Project.app.service.utils.email_sender import EmailSender
from Project.app.model.all_models import AccountModel
from Project.app.service.bots.base import BaseBot


class EmailBot( BaseBot ):

	def __init__( self, db_sess, user=None ):
		super().__init__( db_sess, user )

	def send_all( self ):
		accounts = self._get_all_ad_accounts()
		for account in accounts:
			self._run_with_status( account, self._send_email )
		self._retry_on_failed( self._send_email )
		return self.status

	def send_from_list( self, id_list ):
		for id in id_list:
			account = self._get_ad_account_by_id( id )
			if account:
				self._run_with_status( account, self._send_email )
		self._retry_on_failed( self._send_email )
		return self.status

	def _send_email( self, account ):
		email = EmailSender()
		email.build_mail( recipient=account.email, attachment=account.screenshot.file_dir,
		                  body=account.email_body )
		email.send_mail()
		return