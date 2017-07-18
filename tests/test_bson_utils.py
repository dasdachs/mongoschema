from bson.objectid import ObjectId

from mongoschema.bson_utils import *


class TestMapper(object):
    def test_for_null_one(self):
        assert get_dtype(None) == "null"

    def test_for_null_two(self):
        assert get_dtype("") != "null"

    def test_for_null_three(self):
        assert get_dtype([]) != "null"

    def test_for_int_int(self):
        assert get_dtype(7) == "int"

    def test_for_int_long_one(self):
        assert get_dtype(21474836478) == "long"

    def test_for_int_long_one(self):
        assert get_dtype(-21474836476) == "long"

    def test_for_objectId(self):
        assert get_dtype(ObjectId()) == "ObjectId"

    def test_for_bool_true(self):
        assert get_dtype(True) == "bool"

    def test_for_bool_false(self):
        assert get_dtype(False) == "bool"

    def test_for_bool_not_a_bool(self):
        assert get_dtype(0) != "bool"
