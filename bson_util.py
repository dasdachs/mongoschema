"""Helper functions to encode python data types
to bson data types. A lot has been borowed from 
the bson modul in pymongo."""
import datetime
import re


# __all__ = [""]

def _get_int(value):
    """Encode python int type to bson int32/64."""
    if -2147483648 <= value <= 2147483647:
        return "int"
    else:
        return "long"
