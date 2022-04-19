from flask import Flask
from Project.model.DB import Session
from Project.app.routes.all_routes import register_api_routes, register_view_routes
from Project.app.auth.jwt import register_jwt
from Project.model.all_models import UserModel
from flask_sse import sse
import rq_dashboard

from Project.errors.handler import global_err_handler


# Returning the db connection to the pool
def return_to_db_pool(e=None):
    Session.remove()
    print("DB Session closed")


# App factory pattern
def create_app(config_filename):
    app = Flask(__name__, template_folder="views",static_folder='public')
    app.config.from_object(config_filename)

    # Register JWT verification
    register_jwt(app, Session, UserModel)

    # Register all routes with the application
    register_api_routes(app, prefix="/api")
    register_view_routes(app)

    # Register error handler
    app.register_error_handler(Exception, global_err_handler)

    # Register blueprint for SSE events
    app.register_blueprint(sse, url_prefix='/api/stream/')

    # Monitor the workers
    app.config.from_object(rq_dashboard.default_settings)
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq/")

    return app