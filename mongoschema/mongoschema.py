import csv
from collections import OrderedDict
import json

from pymongo import MongoClient
from texttable import Texttable

from .utils import logger, map_dtype_to_bson


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
    def __init__(self, host="", db="", collection="", query={}, **kwargs):
        """
        TODO: solve working with new query
        The init metod provides some 'private' props, like `_len`, the 
        length of the query results
        """
        self.cursor = MongoClient(host, **kawrgs)
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
        with self.cursor as cursor:
            logger.info("Analyzing schema.")
            conn = cursor[self.db][self.collection]
            results = conn.find(self.query)
            logger.debug("Analyzing {} in {}".format(self.db, self.collection))
            if isinstance(results, dict):
                self._len = 1
                self._get_from_object(results)
            else:
                results = list(results)
                self._len = len(results)
                self._get_from_list(results)
        self._preprocesss_for_reproting()

    def _get_from_object(self, results, path=[], counted=False):
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
                self._get_from_object(val, path=new_path, counted=counted)
            elif isinstance(val, list):
                self._get_from_list(val, path=new_path, counted=counted)
            elif counted:
                pass
            else:
                full_path = '.'.join(new_path)
                data = self.schema.get(full_path)
                if not data:
                    self.schema[full_path] = {
                        'type': map_dtype_to_bson(val),
                        'sum': 1
                    }
                else:
                    self.schema[full_path]['sum'] += 1
                counted = True

    def _get_from_list(self, results, path=[], nested=False):
        """
        Maps all elements of a list with the method `_get_from_object`.

        :param results: a list from a pymongo cursor
        :param path: a list with parent fields
        """
        for result in results:
            self._get_from_object(result, path=path)

    def _preprocesss_for_reproting(self):
        """Prepares the date for reporting to stdOut or JSON"""
        # Add percentage for field
        for value in self.schema.values():
            percentage = round(value["sum"]*100/self._len, 2)
            value["occurrence"] = str(percentage) + " %"
        # Prepare the data
        # first sorting by occurence
        # than changin occurence to %
        data = sorted(
            self.schema.items(),
            key=lambda x: x[1]["sum"],
            reverse=True
        )
        # Insert into OrderdDict
        # TODO exception for python 3.6 >
        self.schema = OrderedDict()
        for element in data:
            key, value = element
            self.schema[key] = value

    def _get_rows(self):
        """Returns array coresoinding to rows."""
        rows = []
        for key, value in self.schema.items():
            name = key
            type_ = value["type"]
            occurrence = value["occurrence"]
            rows.append([name, type_, occurrence])
        return rows

    def to_json(self):
        """JSON representation of the schema.
        TODO: the first line of to_json an __str__ duplicate code, refactor
        """
        if not self.schema:
            self.analyze()
        return json.dumps(self.schema)

    def to_csv(self, name="report.csv", **kwargs):
        """CSV representation of the schema."""
        if not self.schema:
            self.analyze()
        with open(name, "w") as f:
            csv_writer = csv.writer(f, **kwargs)
            csv_writer.writerow(["Field", "Data Type", "Occurrence"])
            rows = self._get_rows()
            for row in rows:
                csv_writer.writerow(row)

    def __str__(self, out="ascii"):
        """Printable representation of the schema."""
        if not self.schema:
            self.analyze()
        # Prepare the ASCII table
        table = Texttable()
        table.set_cols_align(['l', 'l', 'l'])
        table.set_cols_valign(['m', 'm', 'm'])
        table.set_cols_dtype(['t', 'i','a'])
        table.add_row(["Field", "Data Type", "Occurrence"])
        # Create the rows
        rows = self._get_rows()
        for row in rows:
            table.add_row(row)
        return table.draw() + '\n'
