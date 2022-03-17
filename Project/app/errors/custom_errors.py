import traceback

class AppServiceError(Exception):
	'''
	Custom error class raised for errors coming from the service bots:
	- scraping
	- emailing
	- Pdf creation
	- etc.

	Formats the message to be shown to the client, so that it doesn't leak any
	sensitive data about the app, while keeping a record about the error details,
	that will be stored in the logs table in the DB.
	'''

	def __init__( self,message, status_code = 400 ):
		self.message = message
		self.details = traceback.format_exc()
		self.status_code = status_code

	def to_dict( self ):
		return { "status": "failed", "msg": self.message }