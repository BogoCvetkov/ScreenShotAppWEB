from flask.views import View
from flask import render_template
from Project.app.auth.jwt import verify_jwt_in_view, current_user,is_logged_in_view , check_admin_in_view


class LoginViewRouter(View):
    methods = ["GET"]
    decorators = [is_logged_in_view]

    def dispatch_request(self):
        return render_template("login.html")


class ResetViewRouter(View):
    methods = ["GET"]
    decorators = [is_logged_in_view]

    def dispatch_request(self, token):
        return render_template("reset.html")


class HomeViewRouter(View):
    methods = ["GET"]
    decorators = [verify_jwt_in_view]

    def dispatch_request(self):
        return render_template("home.html")


class LogsViewRouter(View):
    methods = ["GET"]
    decorators = [verify_jwt_in_view]

    def dispatch_request(self):
        return render_template("logs.html")


class UsersViewRouter(View):
    methods = ["GET"]
    decorators = [check_admin_in_view,verify_jwt_in_view]

    def dispatch_request(self):
        return render_template("users.html")


class ProfileRoute(View):
    methods = ["GET"]
    decorators = [verify_jwt_in_view]

    def dispatch_request(self):
        return render_template("profile.html")