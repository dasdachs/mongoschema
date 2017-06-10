import bson
import datetime
import logging


# Exports
__all__ = ["logger"]

# Handle logging
logger = logging.getLogger('MongoSchema')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(console_handler)


def map_dtype_to_bson(value):
    """Maps Python's data types to MongoDB's data types
    :param value: any python object
    :return: a string representing the MongoDB datatype
    """
    # NoneType edge case handling
    # NoneType can not be used directly in python
    # so we need to handle this
    if type(value) == None:
        return "null"
    dtype_maping = {
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
    corresponding_mongodb_dtype = dtype_maping[type(value)]
    return corresponding_mongodb_dtype
