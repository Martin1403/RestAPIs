from marshmallow import Schema, fields, EXCLUDE


class UserIdSchema(Schema):
    """User Id"""
    class Meta:
        unknown = EXCLUDE
    user_id = fields.Integer(required=True)


class LoginSchema(Schema):
    """User credentials"""

    class Meta:
        unknown = EXCLUDE
    username = fields.String(required=True)
    email = fields.String(required=True)


class GetUserSchema(UserIdSchema, LoginSchema):
    """User credentials"""
    class Meta:
        unknown = EXCLUDE
    password = fields.String(required=True)


class UpdateUserSchema(LoginSchema):
    """User credentials"""

    class Meta:
        unknown = EXCLUDE
    password = fields.String()


class AllUsersSchema(Schema):
    users = fields.List(fields.Nested(GetUserSchema), required=False)
