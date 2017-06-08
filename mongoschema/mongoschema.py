import json

import pymongo
from pymongo import MongoClient
from texttable import Texttable

from.utils import logger


# Export
__all__ = ['SchemaAnalyzer']


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

        The init metod provides some 'private' props, like `_len`, the 
        length of the query results

        :param host: a url to you MongoDB server, database or collection
        """
        self.host = host
        self.db = db
        self.collection = collection
        self.query = query
        self.schema = schema
        self._len = 0

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
                self._len = 1
                self._get_from_object(results)
            else:
                results = list(results)
                self._len = len(results)
                self._get_from_list(results)

    def _get_from_object(self, results, path=[]):
        """
        The main method that creates the schema. 

        TODO: this is a first draft, a proof of concept
        TODO: the real thing must create a dict with 
        TODO: dicts inside specifing the values and
        TODO: mitigatin the values + returning the types for js
        TODO: iteritems for python 2
        """
        for key, val in results.items():
            new_path = path + [key]
            if isinstance(val, dict):
                self._get_from_object(val, path=new_path)
            elif isinstance(val, list):
                self._get_from_list(val, path=new_path)
            else:    
                full_path = '.'.join(new_path)
                data = self.schema.get(full_path)
                if not data:
                    self.schema[full_path] = {
                        'type': type(val),
                        'occurrence': 1
                    }
                else:
                    data['occurrence'] += 1

    def _get_from_list(self, results, path=[]):
        """
        Maps all elements of a list with the method `_get_from_object`.

        :param results: a list from a pymongo cursor
        :param path: a list with parent fields
        """
        for result in results:
            self._get_from_object(result, path=path)

    def __str__(self, out="ascii"):
        """Printable representation of the schema.
        :param out: a string representing the output method
         could be ascii for the console or a json
        """
        if not self.schema:
            self.analyze()
        # Prepare the data
        data = sorted(
            self.schema.items(),
            key=lambda x: x[1]["occurrence"],
            reverse=True
        )
        for value in data:
            v = value[1]
            v["occurrence"] = str(v["occurrence"]*100/self._len) + " %"
        if out == "json":
            return json.dumps(data)
        else: 
            # Prepare the ASCII table
            table = Texttable()
            table.set_cols_align(['r', 'r', 'r'])
            table.set_cols_valign(['m', 'm', 'm'])
            table.set_cols_dtype(['t', 'i','a'])
            table.add_row(["Field", "Data Type", "Occurrence"])
            for element in data:
                name = element[0]
                type_ = element[1]["type"]
                occurrence = element[1]["occurrence"]
                table.add_row([name, type_, occurrence])
            return table.draw() + '\n'
