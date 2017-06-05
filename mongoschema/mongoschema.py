import logging

import pymongo
from pymongo import MongoClient


# Export
__all__ = ["SchemaAnalyzer"]
# Handle logging
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(console_handler)

class SchemaAnalyzer(object):
    """SchemaAnalyzer is the main class for building 
    a MongoDB schema analysis.

    The API is simple, instantiate a schema object:

    >>> schema = SchemaAnalyzer()
    >>> schema.info()

    You can export the schema to CSV:

    >>> schema.to_csv()

    The `to_csv()` method is just a wrapper around the 
    csv writer method from the standard library, so you can
    pass in all the arguments you would pass to your csv writer.
    >>> schema.to_csv(delimiter=';')
    >>> schema.save()
    """
    def __init__(self, db, collection, host=None, query={}, schema={}):
        """
        :param host: a url to you MongoDB server, database or collection
        """
        self.host = host
        self.db = db
        self.collection = collection
        self.query = query
        self.schema = schema

    def analyze(self):
        """
        TODO: easier collection selection
        TODO: make it poosible to analyze the db
        """
        with MongoClient(self.host) as cursor:
            conn = cursor[self.db][self.collection]
            results = conn.find(self.query)
            logger.debug(type(results))
            if isinstance(results, dict):
                self._get_from_object(results)
            else:
                self._get_from_list(list(results))

    def _get_from_object(self, results, path=""):
        """
        TODO: this is a first draft, a proof of concept
        TODO: the real thing must create a dict with 
        TODO: dicts inside specifing the values and
        TODO: mitigatin the values + returning the types for js
        """
        path = path + "." if path else path
        for key, val in results.items():
            full_path = path + key
            if isinstance(val, dict):
                self._get_from_object(val, path=full_path)
            elif isinstance(val, list):
                self._get_from_list(val, path=full_path)
            data = self.schema.get(full_path)
            if not data:
                self.schema[full_path] = type(val)

    def _get_from_list(self, results, path=""):
        for element in results:
             self._get_from_object(element, path=path)
