"""Helper functions to encode python data types
to bson data types. A lot has been borowed from 
the bson modul in pymongo."""
import datetime
import re


# __all__ = [""]

BSON_MAPPER = {
        bson.objectid.ObjectId: "objectId",
        bool: "bool",
        datetime.date: "Date",
        datetime.datetime: "Date",
        bson.regex.Regex: "Regex",
        str: "string",
        int: "integer",
        float: "float",
        list: "array",
        dict: "object",
}

def _get_int(value):
    """Encode python int type to bson int32/64."""
    if -2147483648 <= value <= 2147483647:
        return "int"
    else:
        return "long"
