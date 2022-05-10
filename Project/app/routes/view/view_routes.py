from flask.views import View
from flask import render_template


class HomeViewRouter( View ):
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("home.html")

class LogsViewRouter (View):
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("logs.html")