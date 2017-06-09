###########
Mongoschema
###########

Mongoschema is a tool for analysing the structure of your MongoDB databases and/or collections.

Current state
=============

The tool is in it's **alpha state**, so if you happen to find it, take this into consideration.

#. To use it jut copy `mongoschema.py` into your working directory.
#. Install **pymongo**
#. ``from mongoschema import SchemaAnalyzer``
#. ``s = SchemaAnalyzer(db=db_name, collection=collection_name)``
#. ``s.analyze()``
   Saves a dict with fields, values and number of ocurrences to a property called ``schema``. If a field is an array or a dict,
   it will sepparate the fields with a comma.
#. For stdout call ``print(s)``, for a JSON call ``to_json()``.

Roadmap
=======

v 0.2
-----

- Improve the core
- Account for edge cases
- Test

v 0.3
-----

- Make better API

v 0.4
-----

- Add CLI tool

v 0.5
------

- Add `export_to_csv()`method

v 0.6
-----

- Make visual representation of the database/collection

v 0.7
-----

- Pandas integration

