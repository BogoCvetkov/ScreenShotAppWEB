from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError, MarshmallowError
from flask import jsonify


def handle_Integrity_err( e ):
	if e.orig.pgcode == "23502":
		msg = e.orig.pgerror.split( "\n" )
		return jsonify( { "status": "failed", "msg": f"{msg[0]}" } )
	if e.orig.pgcode == "23505":
		msg = e.args[0].split( "\n" )
		return jsonify( { "status": "failed", "msg": f"{msg[1]}" } )
	else:
		return jsonify( { "status": "failed", "msg": "Error creating new record" } )


def handle_Marschmello_err( e ):
	if isinstance( e, ValidationError ):
		msg = [{ "field": n[0], "info": n[1] } for n in e.messages.items()]
		return jsonify( { "status": "failed", "msg": msg } )

	else:
		return jsonify( { "status": "failed", "msg": "Error validating input" } )


def global_err_handler( e ):
	if isinstance( e, IntegrityError ):
		return handle_Integrity_err( e ), 400

	if isinstance( e, MarshmallowError ):
		return handle_Marschmello_err( e ), 400

	raise e