from marshmallow import Schema, EXCLUDE, fields, validate


class AccountSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	email = fields.Email()
	name = fields.Str( validate=validate.Length( min=1 ) )
	email_body = fields.Str()
	active = fields.Boolean()