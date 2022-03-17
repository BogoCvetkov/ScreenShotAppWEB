from flask.views import MethodView
from Project.app.controller import user_controller
from Project.app.auth import restrict_to_admin, verify_jwt


# Using decorators to verify user, and restrict access

class UsersRouter( MethodView ):
	decorators = [restrict_to_admin, verify_jwt]

	# Using jwt validation for all routes
	# def __init__( self ):
	# 	verify_jwt_in_request()

	def get( self ):
		return user_controller.get_all_users()

	def post( self ):
		return user_controller.create_user()


class UserRouter( MethodView ):
	decorators = [restrict_to_admin, verify_jwt]

	def get( self, id ):
		return user_controller.get_user( id )

	def patch( self, id ):
		return user_controller.update_user( id )

	def delete( self, id ):
		return user_controller.delete_user( id )