from flask.views import MethodView
from Project.app.controller import account_controller
from Project.app.auth import verify_jwt


class AccountsRouter( MethodView ):
	decorators = [verify_jwt]

	def get( self ):
		return account_controller.get_all_accounts()

	def post( self ):
		return account_controller.create_account()


class AccountRouter( MethodView ):
	decorators = [verify_jwt]

	def get( self, id ):
		return account_controller.get_account( id )

	def patch( self, id ):
		return account_controller.update_account( id )

	def delete( self, id ):
		return account_controller.delete_account( id )