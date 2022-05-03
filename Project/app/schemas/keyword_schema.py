from marshmallow import Schema, EXCLUDE, fields, validate


class KeywordSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	keyword = fields.Str(validate=validate.Length( min=1 ),required=True)
	active = fields.Boolean()
	account_id = fields.Integer(required=True)