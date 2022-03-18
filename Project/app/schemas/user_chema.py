from marshmallow import Schema, EXCLUDE, fields, validate, \
	validates_schema, ValidationError, \
	post_load,pre_load


class UserSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	email = fields.Email( required=True )
	username = fields.Str( validate=validate.Length( min=3 ), required=True )
	password = fields.Str( validate=validate.Length( min=8 ), required=True )
	confirm_password = fields.Str( required=True )

	@post_load
	def confirm_user_password( self, data, **kwargs ):
		if ("password" in data) and data["password"] != data["confirm_password"]:
			raise ValidationError( "Password and confirm password fields don't match","check_pass" )
		self.remove_confirm_field(data)
		return data

	# Confirm field is not part of the UserModel
	def remove_confirm_field( self, data ):
		data.pop( "confirm_password", None )