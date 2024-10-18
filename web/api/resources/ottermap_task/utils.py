import random
import string
from math import radians, sin, cos, sqrt, atan2

from flask_restx import fields

from web.api.resources.ottermap_task.serializer import api


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def data_envelope(nested_model, as_list=False, skip_none=False):
    nested_model = fields.Nested(model=nested_model, description="Nested Model", allow_null=True, skip_none=skip_none)

    if as_list is True:
        data_field = fields.List(nested_model, description="List of objects")
    else:
        data_field = nested_model

    return api.model("Envelope Model for all APIs", {
        "data": data_field,
        "status_code": fields.Integer(required=True, description="Status code of the response"),
        "success": fields.Boolean(required=True, description="Success status of the response"),
        "message": fields.String(required=True, description="Additional Message in the response"),
        "message_code": fields.String(required=True, description="Additional Message Code in the response")
    })


def format_response(data, status_code, message=None, custom_ob=None, message_code_class=None, save=True):
    message_code = None
    if data is not None:
        if save:
            data.status_code = str(status_code)

        try:
            if save:
                data.save()
            if custom_ob is not None:
                data = custom_ob
        except Exception as e:
            data = None
            status_code = 500
            message = None
    else:
        data = custom_ob

    if 200 <= status_code < 300:
        success_flag = True
        message_code = 'success'
    else:
        success_flag = False
        if status_code == 500 and message is None:
            message = "ERROR_500"
            message_code = 'contact_support'
        elif status_code == 422 and message is None:
            message = "FAILED"
            message_code = 'verification_failed'

    if message_code_class is not None:
        message_code = message_code_class.code
        message = message_code_class.message
    else:
        message_code = message_code

    response_json = ({
                         "data": data,
                         "status_code": status_code,
                         "message_code": message_code,
                         "message": message,
                         "success": success_flag,
                     }, status_code)

    return response_json


def generate_id(prepend_string):
    charset = string.ascii_lowercase + string.ascii_letters
    return prepend_string + "_" + "".join([random.choice(charset) for _ in range(20)])
