from marshmallow import Schema, EXCLUDE, fields, validate


class LoginSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	email = fields.Email(required=True)
	password = fields.Str( required=True )