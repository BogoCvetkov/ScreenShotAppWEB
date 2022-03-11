from flask.views import MethodView
from Project.app.controller import user_controller


class UsersRouter( MethodView ):

	def get( self ):
		return user_controller.get_all_users()

	def post( self ):
		return user_controller.create_user()


class UserRouter( MethodView ):

	def get( self, id ):
		return user_controller.get_user( id )

	def patch( self, id ):
		return user_controller.update_user( id )

	def delete( self, id ):
		return user_controller.delete_user( id )