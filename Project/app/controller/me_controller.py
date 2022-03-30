from Project.model.all_models import UserModel
from Project.app.schemas.user_chema import UserSchema
from Project.app.controller.controller_factory import update_factory, get_one_factory
from Project.app.auth.jwt import current_user
from Project.errors.custom_errors import AppServiceError
from flask import request


# /me
def get_logged_user():
	id = current_user.id

	get_me = get_one_factory( UserModel, UserSchema( exclude=["password"] ) )

	return get_me( id )


# /update-me
def update_logged_user_info():
	id = current_user.id

	if "password" in request.json:
		raise AppServiceError( "Can't update your password in this route" )

	update_me = update_factory( UserModel,
	                            UserSchema( exclude=["password", "confirm_password"],
	                                        partial=True ) )

	return update_me( id )