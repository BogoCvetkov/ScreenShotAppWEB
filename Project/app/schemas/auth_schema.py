from marshmallow import Schema, EXCLUDE, fields, validate


class AuthSchema( Schema ):
	class Meta:
		unknown = EXCLUDE
		ordered = True

	# Id field is read only
	email = fields.Email(
		required=True,
		error_messages={
			"required": "Email not provided" }, )
	password = fields.String(
		required=True,
		error_messages={ "required": "Password not provided" },
	)