"""
Module for JSON validation with marshmallow
"""
from marshmallow import *


class MessageSchema(Schema):
    message = fields.String(required=True, attribute="message")
    sender = fields.String(required=True, attribute="sender")
    conversation_id = fields.Int(required=True, attribute= "conversation_id")