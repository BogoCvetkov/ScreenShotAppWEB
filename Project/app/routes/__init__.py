from Project.app.routes.api.account_route import *
from Project.app.routes.api.page_route import *
from Project.app.routes.api.service_route import *
from Project.app.routes.api.user_route import *

def register_routes( application ):

	# registering API routes
	application.add_url_rule( "/users/", view_func=UsersRouter.as_view( "users_resource" ) )
	application.add_url_rule( "/users/<int:id>", view_func=UserRouter.as_view( "user_resource" ) )

	application.add_url_rule( "/accounts/", view_func=AccountsRouter.as_view( "accounts_resource" ) )
	application.add_url_rule( "/accounts/<int:id>", view_func=AccountRouter.as_view( "account_resource" ) )

	application.add_url_rule( "/pages/", view_func=PagesRouter.as_view( "pages_resource" ) )
	application.add_url_rule( "/pages/<int:id>", view_func=PageRouter.as_view( "page_resource" ) )

	application.add_url_rule( "/service/", view_func=ServiceRouter.as_view( "service_resource" ) )