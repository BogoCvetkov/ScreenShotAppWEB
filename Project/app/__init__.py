from flask import Flask
from Project.app.model import Session
from Project.app.routes import register_routes
from Project.app.auth import register_jwt
from Project.app.model.all_models import UserModel

from Project.app.errors.handler import global_err_handler


# Returning the db connection to the pool
def return_to_db_pool( e=None ):
	Session.remove()
	print( "DB Session closed" )


# App factory pattern
def create_app( config_filename ):
	app = Flask( __name__ )
	app.config.from_object( config_filename )

	# Register JWT verification
	register_jwt( app, Session, UserModel )

	# Register all routes with the application
	register_routes( app, prefix="/api" )

	# Register error handler
	app.register_error_handler( Exception, global_err_handler )

	return app