from Project.app.routes.api.account_route import *
from Project.app.routes.api.page_route import *
from Project.app.routes.api.service_route import *
from Project.app.routes.api.user_route import *
from Project.app.routes.api.auth_route import *
from Project.app.routes.api.me_route import *
from Project.app.routes.api.schedule_route import *
from Project.app.routes.api.event_route import *
from Project.app.routes.api.log_route import *

# View Routers
from Project.app.routes.view.home import *


def register_api_routes(application, prefix=None):
    # registering API routes

    # No JWT token required
    application.add_url_rule(f"{prefix}/login/", view_func=LoginRouter.as_view("login_route"))
    application.add_url_rule(f"{prefix}/forget-pass/",
                             view_func=ForgetPassRouter.as_view("forget_route"))
    application.add_url_rule(f"{prefix}/reset-pass/<string:token>",
                             view_func=ResetPassRouter.as_view("reset_route"))
    application.add_url_rule(f"{prefix}/logout/",
                             view_func=LogoutRouter.as_view("logout_route"))

    application.add_url_rule(f"{prefix}/stream/event/",
                             view_func=EventRouter.as_view("event_route"))

    # JWT token required
    application.add_url_rule(f"{prefix}/accounts/",
                             view_func=AccountsRouter.as_view("accounts_route"))
    application.add_url_rule(f"{prefix}/accounts/<int:id>",
                             view_func=AccountRouter.as_view("account_route"))

    application.add_url_rule(f"{prefix}/pages/", view_func=PagesRouter.as_view("pages_route"))
    application.add_url_rule(f"{prefix}/pages/<int:id>",
                             view_func=PageRouter.as_view("page_route"))

    application.add_url_rule(f"{prefix}/schedules/", view_func=SchedulesRouter.as_view("schedules_route"))
    application.add_url_rule(f"{prefix}/schedules/<int:id>",
                             view_func=ScheduleRouter.as_view("schedule_route"))

    application.add_url_rule(f"{prefix}/service/",
                             view_func=ServiceRouter.as_view("service_route"))

    application.add_url_rule(f"{prefix}/me/",
                             view_func=MeRouter.as_view("me_route"))
    application.add_url_rule(f"{prefix}/reset-my-pass/",
                             view_func=ResetLoggedUserPassRouter.as_view("reset_my_pass_route"))

    application.add_url_rule(f"{prefix}/logs/", view_func=LogRouter.as_view("logs_route"))

    # /users/ is restricted to admins only
    application.add_url_rule(f"{prefix}/users/", view_func=UsersRouter.as_view("users_route"))
    application.add_url_rule(f"{prefix}/users/<int:id>",
                             view_func=UserRouter.as_view("user_route"))


def register_view_routes(appplication):
    # Register routes for the frontend

    appplication.add_url_rule("/", view_func=HomeViewRouter.as_view("home_view_route"))