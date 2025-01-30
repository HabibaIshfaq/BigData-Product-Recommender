import json
from werkzeug.routing import BaseConverter
from bson import ObjectId
import isodate as iso
from datetime import datetime, date


class MongoJSONEncoder(json.JSONEncoder):  # Use json.JSONEncoder from Python's standard library
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)  # Format datetime and date objects to ISO format
        if isinstance(o, ObjectId):
            return str(o)  # Convert ObjectId to a string
        else:
            return super().default(o)  # Use the default encoder


class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)  # Convert URL string to ObjectId

    def to_url(self, value):
        return str(value)  # Convert ObjectId to string for URLs
