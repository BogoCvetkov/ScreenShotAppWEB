from flask import Flask
from Project.app.model import Session
from Project.app.routes import register_routes


# Returning the db connection to the pool
def return_to_db_pool( e=None ):
	Session.remove()
	print( "DB Session closed" )


# App factory pattern
def create_app( config_filename ):
	app = Flask( __name__ )
	app.config.from_object( config_filename )

	# Register all routes with the application
	register_routes( app )

	return app