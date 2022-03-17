from flask import request, jsonify, make_response
from Project.app.model.all_models import UserModel
from Project.app.model import Session
from Project.app.errors import AppServiceError
from Project.app.schemas.auth_schema import LoginSchema
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import os


def login():
	# Validate input
	credentials = LoginSchema().load( request.json )

	# Create Session
	db_sess = Session()

	# Verify email and password
	user = UserModel.find_by_email( db_sess, credentials["email"] )

	if not user or not user.verify_password( credentials["password"] ):
		raise AppServiceError( "Invalid username or password" )

	# Send the jwt access token in a cookie
	resp = make_response( jsonify(
		{ "status": "success", "msg": "Log in successful" } ), 200 )
	token = create_access_token( identity=user.id )

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