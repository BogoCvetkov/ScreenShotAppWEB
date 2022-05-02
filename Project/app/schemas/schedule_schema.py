from marshmallow import Schema, EXCLUDE, fields, validate


class ScheduleSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	id = fields.Integer( dump_only=True )
	day = fields.Integer(required=True,validate=validate.Range(min=0, max=6))
	hour = fields.Integer(required=True,validate=validate.Range(min=0, max=23))
	account_id = fields.Integer(required=True)