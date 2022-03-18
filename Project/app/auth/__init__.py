from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request, current_user
from Project.app.errors import AppServiceError
from functools import wraps


# Factory function for registering the jwt extension with Flask
def register_jwt( app, Session, Model ):
	jwt = JWTManager()
	db_sess = Session()

	# Automatically loading the user form DB after validation,
	# to make it available to the app
	@jwt.user_lookup_loader
	def user_lookup_callback( _jwt_header, jwt_data ):
		id = jwt_data["sub"]
		return Model.get_by_id( db_sess, id )

	jwt.init_app( app )


# Verify jwt token decorator
def verify_jwt( f ):
	@wraps( f )
	def decorator( *args, **kwargs ):
		verify_jwt_in_request()
		return f( *args, **kwargs )

	return decorator


# Restrict to admins decorator
def restrict_to_admin( f ):
	@wraps( f )
	def decorator( *args, **kwargs ):
		if not current_user.admin:
			raise AppServiceError( "Admin permission required", 401 )
		else:
			return f( *args, **kwargs )

	return decorator