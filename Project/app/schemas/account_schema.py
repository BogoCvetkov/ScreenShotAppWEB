from marshmallow import Schema, EXCLUDE, fields, validate
from Project.app.schemas.validators import validate_country


# When fetching multiple accounts
class AccountsSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    # Id field is read only
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(validate=validate.Length(min=1), required=True)
    email_body = fields.Str()
    active = fields.Boolean()
    last_scrape_fail = fields.Boolean(dump_only=True)
    last_email_fail = fields.Boolean(dump_only=True)
    last_scraped = fields.DateTime(dump_only=True)
    last_emailed = fields.DateTime(dump_only=True)
    country = fields.String(validate=validate_country)


class ScreenshotSchema(Schema):
    id = fields.Integer(dump_only=True)
    file_dir = fields.String(dump_only=True)


# Fetching by ID - loads the relationship
class AccountSchema(AccountsSchema):
    screenshot = fields.Nested(ScreenshotSchema)