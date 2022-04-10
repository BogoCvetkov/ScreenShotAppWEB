from flask.views import MethodView
from Project.app.controller import event_controller


class EventRouter(MethodView):

    def post(self):
        return event_controller.publish_event()