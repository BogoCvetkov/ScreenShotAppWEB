from marshmallow import Schema, EXCLUDE, fields, validate


class AccountSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	email = fields.Email(required=True)
	name = fields.Str( validate=validate.Length( min=1 ), required=True )
	email_body = fields.Str()
	active = fields.Boolean()
	last_scrape_fail = fields.Boolean( dump_only=True )
	last_email_fail = fields.Boolean( dump_only=True )
	last_scraped = fields.DateTime(dump_only=True)
	last_emailed = fields.DateTime(dump_only=True)