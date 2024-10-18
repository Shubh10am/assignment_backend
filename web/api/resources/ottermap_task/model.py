from mongoengine import Document, StringField, FloatField
from web.api.resources.ottermap_task import utils


class Shop(Document):
    prepend_string = "shop"

    shop_id = StringField(required=True)
    name = StringField(required=True, max_length=100)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)

    @classmethod
    def generate_id(cls):
        return utils.generate_id(cls.prepend_string)
