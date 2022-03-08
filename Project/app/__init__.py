from flask import Flask
from Project.app.model import Session
from Project.app.routes.api.user_route import UserRouter,UsersRouter


# Returning the db connection to the pool
def return_to_db_pool(e=None):
	Session.remove()
	print( "Connection closed" )

# App factory pattern
def create_app( config_filename ):
	app = Flask( __name__ )
	app.config.from_object( config_filename )

	# registering API routes
	app.add_url_rule("/users/",view_func=UsersRouter.as_view("users_resource"))
	app.add_url_rule("/users/<int:id>",view_func=UserRouter.as_view("user_resource"))

	return app