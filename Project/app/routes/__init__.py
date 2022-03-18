from Project.app.routes.api.account_route import *
from Project.app.routes.api.page_route import *
from Project.app.routes.api.service_route import *
from Project.app.routes.api.user_route import *
from Project.app.routes.api.auth_route import *

def register_routes( application, prefix=None ):

	# registering API routes
	application.add_url_rule( f"{prefix}/users/", view_func=UsersRouter.as_view( "users_resource" ) )
	application.add_url_rule( f"{prefix}/users/<int:id>", view_func=UserRouter.as_view( "user_resource" ) )

	application.add_url_rule( f"{prefix}/accounts/", view_func=AccountsRouter.as_view( "accounts_resource" ) )
	application.add_url_rule( f"{prefix}/accounts/<int:id>", view_func=AccountRouter.as_view( "account_resource" ) )

	application.add_url_rule( f"{prefix}/pages/", view_func=PagesRouter.as_view( "pages_resource" ) )
	application.add_url_rule( f"{prefix}/pages/<int:id>", view_func=PageRouter.as_view( "page_resource" ) )

	application.add_url_rule( f"{prefix}/service/", view_func=ServiceRouter.as_view( "service_resource" ) )

	application.add_url_rule( f"{prefix}/login/", view_func=LoginRouter.as_view( "login_resource" ) )
	application.add_url_rule( f"{prefix}/forget-pass/", view_func=ForgetPassRouter.as_view( "forget_resource" ) )
	application.add_url_rule( f"{prefix}/reset-pass/<string:token>", view_func=ResetPassRouter.as_view( "reset_resource" ) )