from marshmallow import Schema, EXCLUDE, fields, validate


class UserSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer(dump_only=True)
	email = fields.Email()
	username = fields.Str( validate=validate.Length( min=3 ) )
	password = fields.Str( validate=validate.Length( min=6 ) )