from email.message import EmailMessage
from Project.app.errors import AppServiceError
from smtplib import SMTP_SSL
import ssl,os


class EmailSender:
	"""
	This class is used for attaching the screenshots of the pages and sending them to an email
	"""

	# Storing email agent credentials as class properties
	sender = os.environ["MAIL_USER"]
	password = os.environ["MAIL_PASS"]
	subject = os.environ["MAIL_SUBJECT"]

	def __init__( self ):
		self.message = EmailMessage()

	# First we construct the mail and then we send it
	def build_mail( self, recipient, attachment, body="" ):
		self.message["From"] = self.sender
		self.message["To"] = recipient
		self.message['Subject'] = self.subject
		self.message.set_content( body )
		self._attach_file( attachment )

	def send_mail( self ):
			context = ssl.create_default_context()
			mail_server = SMTP_SSL( 'smtp.gmail.com', 465, context=context )
			try:
				mail_server.login( self.sender, self.password )
				mail_server.send_message( self.message )
			except Exception as e:
				message = f"Failed to send email to: {self.message['To']}."
				raise AppServiceError( message=message )
			finally:
				mail_server.quit()

	# Private method used only by the build_mail method for attaching of a file
	def _attach_file( self, attachment ):
		with open( attachment, "rb" ) as file:
			self.message.add_attachment( file.read(),
			                             maintype="application",
			                             subtype="pdf",
			                             filename="Competitor_Analysis.pdf" )


if __name__ == "__main__":
	# Used for testing during development

	email_sender = EmailSender
	email_sender.build_mail( recipient="bogomil@xplora.bg",
	                         attachment="D:\\Programming\\Work_Projects\\ScrenshotAppWEB\\Ad_library_screens/Bogo/Happy/Ads_Preview_09_03.pdf",
	                         )
	email_sender.send_mail()