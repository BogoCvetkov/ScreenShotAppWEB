from flask.views import MethodView
from Project.app.controller import auth_controller


class LoginRouter( MethodView ):

	def post( self ):
		return auth_controller.login()


class ForgetPassRouter( MethodView ):

	def post( self ):
		return auth_controller.forget_pass()


class ResetPassRouter( MethodView ):

	def post( self, token ):
		return auth_controller.reset_pass(token)