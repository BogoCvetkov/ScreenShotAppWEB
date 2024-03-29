from flask import request, jsonify
from flask.views import MethodView
from Project.app.controller import service_controller
from Project.app.auth.jwt import verify_jwt


class ServiceRouter(MethodView):
    decorators = [verify_jwt]

    def get(self):
        return service_controller.get_worker_info()

    def post(self):

        if request.args.get("type") and request.args["type"] == "scrape":
            return service_controller.capture_accounts()

        if request.args.get("type") and request.args["type"] == "email":
            return service_controller.send_emails()

        if request.args.get("type") and request.args["type"] == "test":
            return service_controller.test_schedule()

        else:
            return jsonify({ "status": "failed",
                             "msg": "URL param /type/ missing or invalid. "
                                    "Please specify the type of service bot as a query param.",
                             "args_accepted": ["scrape", "email"] }), 400