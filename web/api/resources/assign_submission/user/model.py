from mongoengine import Document, StringField, DateTimeField, ReferenceField, EmailField
from datetime import datetime
from web.api.resources.assign_submission.user import utils


class AssignUser(Document):
    prepend_string = "user"

    user_id = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    access_token = StringField()
    user_type = StringField(choices=["admin", "user"])
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.username

    @classmethod
    def generate_id(cls):
        return utils.generate_id(cls.prepend_string)


class Assignment(Document):
    prepend_string = "assign"

    assign_id = StringField(required=True, unique=True)
    user = ReferenceField(AssignUser, required=True)
    task = StringField(required=True)
    admin = StringField()
    submitted_at = DateTimeField(default=datetime.utcnow)
    status = StringField(choices=["pending", "accepted", "rejected"], default="pending")

    @classmethod
    def generate_id(cls):
        return utils.generate_id(cls.prepend_string)
