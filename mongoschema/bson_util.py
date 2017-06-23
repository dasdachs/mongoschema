"""Helper functions to encode python data types
to bson data types. A lot has been borowed from 
the bson modul in pymongo."""
import datetime
import re


__all__ = ["BSON_MAPPER"]


def get_dtype(value):
    """
    """
    if type(value) == None:
        return "null"
    mapper= {
            bson.objectid.ObjectId: "objectId",
            bool: "bool",
            datetime.date: "Date",
            datetime.datetime: "Date",
            bson.regex.Regex: "Regex",
            str: "string",
            int: _get_ini(),
            float: "float",
            list: "array",
            dict: "object",
    }
    return mapper(value)

def _get_int(value):
    """Encode python int type to bson int32/64."""
    if -2147483648 <= value <= 2147483647:
        return "int"
    else:
        return "long"
