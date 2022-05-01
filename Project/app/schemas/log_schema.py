from marshmallow import Schema, EXCLUDE, fields, validate


class LogSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	started_by = fields.String(dump_only=True)
	account_name = fields.String(dump_only=True)
	log_msg = fields.String(dump_only=True)
	log_details = fields.String(dump_only=True)
	date = fields.DateTime(dump_only=True)
	fail = fields.Boolean(dump_only=True)
	account_id = fields.Integer( dump_only=True )