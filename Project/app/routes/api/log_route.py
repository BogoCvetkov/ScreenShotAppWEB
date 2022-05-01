from flask.views import MethodView
from Project.app.controller import log_controller
from Project.app.auth.jwt import verify_jwt

class LogRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self ):
		return log_controller.get_all_logs()