from flask import Flask
from Project.app.model import Session
from Project.app.routes.api.user_route import UserRouter, UsersRouter
from Project.app.routes.api.account_routes import AccountRouter, AccountsRouter
from Project.app.routes.api.page_routes import PageRouter, PagesRouter
from Project.app.routes.api.service_routes import ServiceRouter


# Returning the db connection to the pool
def return_to_db_pool( e=None ):
	Session.remove()
	print( "DB Session closed" )


# App factory pattern
def create_app( config_filename ):
	app = Flask( __name__ )
	app.config.from_object( config_filename )

	# registering API routes
	app.add_url_rule( "/users/", view_func=UsersRouter.as_view( "users_resource" ) )
	app.add_url_rule( "/users/<int:id>", view_func=UserRouter.as_view( "user_resource" ) )

	app.add_url_rule( "/accounts/", view_func=AccountsRouter.as_view( "accounts_resource" ) )
	app.add_url_rule( "/accounts/<int:id>", view_func=AccountRouter.as_view( "account_resource" ) )

	app.add_url_rule( "/pages/", view_func=PagesRouter.as_view( "pages_resource" ) )
	app.add_url_rule( "/pages/<int:id>", view_func=PageRouter.as_view( "page_resource" ) )

	app.add_url_rule( "/service/", view_func=ServiceRouter.as_view( "service_resource" ) )

	return app