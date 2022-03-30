from flask.views import MethodView
from Project.app.controller import me_controller
from Project.app.auth.jwt import verify_jwt


class MeRouter( MethodView ):
	decorators = [verify_jwt]

	def get( self ):
		return me_controller.get_logged_user()

	def patch( self ):
		return me_controller.update_logged_user_info()