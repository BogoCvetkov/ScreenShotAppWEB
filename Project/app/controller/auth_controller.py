from flask import request, jsonify, make_response
from Project.app.model.all_models import UserModel, ResetPassModel
from Project.app.model import Session
from Project.app.errors import AppServiceError
from Project.app.schemas.auth_schema import AuthSchema
from Project.app.schemas.user_chema import UserSchema
from Project.app.service.utils.email_sender import EmailSender
from flask_jwt_extended import create_access_token, current_user
from datetime import datetime, timedelta
import os


def sign_send_jwt( id, msg ):
	# Send the jwt access token in a cookie
	resp = make_response( jsonify(
		{ "status": "success", "msg": msg } ), 201 )
	token = create_access_token( identity=id )

	if os.environ["ENV"] == "development":
		is_secure = False
	else:
		is_secure = True

	resp.set_cookie( "jwt", token,
	                 max_age=timedelta( minutes=int( os.environ["COOKIE_EXP_TIME"] ) ),
	                 httponly=True,
	                 samesite="Strict",
	                 secure=is_secure )
	return resp


# /login
def login():
	# Validate input
	credentials = AuthSchema().load( request.json )

	# Create Session
	db_sess = Session()

	# Verify email and password
	user = UserModel.find_by_email( db_sess, credentials["email"] )

	if not user or not user.verify_password( credentials["password"] ):
		raise AppServiceError( "Invalid username or password" )

	# Send jwt token
	return sign_send_jwt( user.id, "Log in successful" )


# /forget-pass
def forget_pass():
	# Create Session
	db_sess = Session()

	# Validate input
	data = AuthSchema( exclude=["password"] ).load( request.json )
	email = data["email"]

	# Check if user exists
	user = UserModel.find_by_email( db_sess, email )

	if not user: raise AppServiceError( "Email doesn't exist", 404 )

	# Create expiration reset token
	reset_token = ResetPassModel.generate_token( db_sess, email )

	db_sess.commit()

	# Send email with the expiration link for resetting password
	restore_url = request.url_root + "api" + "/reset-pass" + f"/{reset_token}"
	body = f"Your restoration link (valid for 10 minutes): {restore_url}"
	EmailSender().build_mail( email, body=body ).send_mail()

	return jsonify( { "status": "success", "msg": "A restoration link has been sent to your email",
	                  "token": reset_token } ), 201


# /reset-pass
def reset_pass( token ):
	# Create Session
	db_sess = Session()

	# Check if token exists
	check_token = ResetPassModel.find_by_token( db_sess, token )

	if not check_token: raise AppServiceError( "Invalid token!", 403 )

	# Check if token hasn't expired
	if check_token.has_expired(): raise AppServiceError( "Link is expired!", 401 )

	# Set new password
	new_data = UserSchema( exclude=["email", "username"] ).load( request.json )

	user = UserModel.find_by_email( db_sess, check_token.email )
	user.password = new_data["password"]
	user.last_changed = datetime.now()

	# Invalidate token
	check_token.expires_at = datetime.now()

	db_sess.commit()

	# Send jwt token
	return sign_send_jwt( user.id, "Password updated successfully" )


# /reset-my-pass
def reset_logged_user_pass():
	# Create Session
	db_sess = Session()

	# Set new password
	new_data = UserSchema( exclude=["email", "username"] ).load( request.json )

	user = UserModel.get_by_id( db_sess, current_user.id )
	user.password = new_data["password"]
	user.last_changed = datetime.now()

	db_sess.commit()

	# Send jwt token
	return sign_send_jwt( user.id, "Password updated successfully" )


# /logout
def logout():
	resp = make_response( jsonify(
		{ "status": "success", "msg": "Logout successful" } ), 200 )

	if os.environ["ENV"] == "development":
		is_secure = False
	else:
		is_secure = True

	resp.set_cookie( "jwt", "logout",
	                 max_age=timedelta( minutes=0 ),
	                 httponly=True,
	                 samesite="Strict",
	                 secure=is_secure )
	return resp