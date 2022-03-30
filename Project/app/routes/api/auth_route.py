from flask.views import MethodView
from Project.app.controller import auth_controller
from Project.app.auth.jwt import verify_jwt


class LoginRouter( MethodView ):

	def post( self ):
		return auth_controller.login()


class ForgetPassRouter( MethodView ):

	def post( self ):
		return auth_controller.forget_pass()


class ResetPassRouter( MethodView ):

	def post( self, token ):
		return auth_controller.reset_pass( token )


class LogoutRouter( MethodView ):
	def get( self ):
		return auth_controller.logout()


class ResetLoggedUserPassRouter( MethodView ):
	decorators = [verify_jwt]

	def post( self ):
		return auth_controller.reset_logged_user_pass()