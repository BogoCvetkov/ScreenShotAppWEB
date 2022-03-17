from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError, MarshmallowError
from Project.app.errors.custom_errors import *
from flask import jsonify


def handle_IntegrityErr( e ):
	if e.orig.pgcode == "23502":
		msg = e.orig.pgerror.split( "\n" )
		return jsonify( { "status": "failed", "msg": f"{msg[0]}" } )
	if e.orig.pgcode == "23505":
		msg = e.args[0].split( "\n" )
		return jsonify( { "status": "failed", "msg": f"{msg[1]}" } )
	else:
		return jsonify( { "status": "failed", "msg": "Error creating new record" } )


def handle_MarshmallowError( e ):
	if isinstance( e, ValidationError ):
		msg = [{ "field": n[0], "info": n[1] } for n in e.messages.items()]
		return jsonify( { "status": "failed", "msg": msg } )

	else:
		return jsonify( { "status": "failed", "msg": "Error validating input" } )

def handle_AppServiceError(e):
	return jsonify(e.to_dict())


def global_err_handler( e ):
	if isinstance( e, IntegrityError ):
		return handle_IntegrityErr( e ), 400

	if isinstance( e, MarshmallowError ):
		return handle_MarshmallowError( e ), 400

	if isinstance( e, AppServiceError ):
		return handle_AppServiceError( e ), e.status_code

	raise e