from flask.views import MethodView
from Project.app.controller import log_controller
from Project.app.auth.jwt import verify_jwt

class LogRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self ):
		return log_controller.get_all_logs()

# class ScheduleRouter( MethodView ):
#
# 	decorators = [verify_jwt]
#
# 	def get( self, id ):
# 		return schedule_controller.get_schedule( id )
#
# 	def patch( self, id ):
# 		return schedule_controller.update_schedule( id )
#
# 	def delete( self, id ):
# 		return schedule_controller.delete_schedule( id )