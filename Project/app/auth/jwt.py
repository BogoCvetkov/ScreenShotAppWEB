from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request, current_user, get_jwt
from Project.errors.custom_errors import AppServiceError
from flask import redirect, g
from functools import wraps
from datetime import datetime


# Factory function for registering the jwt extension with Flask
def register_jwt(app, Session, Model):
    jwt = JWTManager()
    db_sess = Session()

    # Automatically loading the user form DB after validation,
    # to make it available to the app
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        id = jwt_data["sub"]
        user = Model.get_by_id(db_sess, id)

        # Validate user still exists
        if not user:
            raise AppServiceError("User doesn't exist", 404)
        return user

    jwt.init_app(app)


## DECORATORS USED INSIDE THE API

# Verify jwt token decorator
def verify_jwt(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()

        # Check if password was changed after the access-token was created
        if current_user.last_changed and (
                current_user.last_changed > datetime.fromtimestamp(get_jwt()["iat"])):
            raise AppServiceError("Password was changed, please log in again!", 401)
        return f(*args, **kwargs)

    return decorator


# Restrict to admins decorator
def restrict_to_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.admin:
            raise AppServiceError("Admin permission required", 403)
        else:
            return f(*args, **kwargs)

    return decorator


## DECORATORS USED INSIDE THE WEBSITE

def verify_jwt_in_view(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Prevent auto Error raising
        verify_jwt_in_request(optional=True)

        if not current_user:
            return redirect("/login")

        # Check if password was changed after the access-token was created
        if current_user.last_changed and (
                current_user.last_changed > datetime.fromtimestamp(get_jwt()["iat"])):
            return redirect("/login")

        # Making the user easily accessible inside templates
        g.user = current_user

        return f(*args, **kwargs)

    return decorator


def is_logged_in_view(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Prevent auto Error raising
        verify_jwt_in_request(optional=True)

        if current_user:
            return redirect("/")

        return f(*args, **kwargs)

    return decorator


def check_admin_in_view(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.admin:
            return redirect("/")

        return f(*args, **kwargs)

    return decorator