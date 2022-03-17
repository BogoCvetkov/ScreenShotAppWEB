from flask.views import MethodView
from Project.app.controller import auth_controller


class AuthRouter( MethodView ):

	def post( self ):
		return auth_controller.login()