"""Helper functions to encode python data types
to bson data types. A lot has been borowed from 
the bson modul in pymongo."""
import datetime
import re

import bson
from bson.objectid import ObjectId

from .logger import logger


__all__ = ["get_dtype"]


def get_dtype(value):
    """
    """
    logger.debug("Creating bson mapping for {}, type {}".format(value, type(value)))
    if type(value) == None:
        return "null"
    elif isinstance(value, ObjectId):
        return "ObjectId"
    mapper= {
            bool: "bool",
            datetime.date: "Date",
            datetime.datetime: "Date",
            bson.regex.Regex: "Regex",
            str: "string",
            int: _get_int(value),
            float: "float",
            list: "array",
            dict: "object",
            bytes: "binData"
    }
    return mapper[type(value)]

def _get_int(value):
    """Encode python int type to bson int32/64."""
    if -2147483648 <= value <= 2147483647:
        return "int"
    else:
        return "long"

def _get_float(value):
    pass
