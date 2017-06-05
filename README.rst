###########
Mongoschema
###########

Mongoschema is a tool for analysing the structure of your MongoDB databases and/or collections.

Current state
=============

The tool is is alpha state, so if you happen to come accrose it and use it, be mindfull od it's limittations.

#. To use it jut copy `mongoschema.py` into your working directory.
#. Install `pymongo`
#. `from mongoschema import SchemaAnalyzer`
#. `s = SchemaAnalyzer(db=db_name, collection=collection_name)`:w
#. `s.analyze()`
#. `s.schema`
   Returns a dict with fields and values. If a field is an array or a dict, it will sepperate the
   fields with a comma.

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

