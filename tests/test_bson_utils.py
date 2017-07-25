import datetime
import math

from bson.objectid import ObjectId

from mongoschema.bson_utils import get_dtype, _get_int


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

    def test_for_date_with_date(self):
        unix_time = datetime.date(1970, 1, 1)
        assert get_dtype(unix_time) == "Date"

    def test_for_date_with_datetime(self):
        unix_time = datetime.datetime(1970, 1, 1)
        assert get_dtype(unix_time) == "Date"

    def test_for_string(self):
        assert get_dtype("test") == "string"

    def test_for_array_with_list(self):
        assert get_dtype(["test"]) == "array"

    def test_for_array_with_python_array(self):
        """TODO test with pythons array"""
        pass

    def test_for_array_with_np_array(self):
        """TODO test with numpy arrays"""
        pass

    def test_for_object_with_empty_dict(self):
        assert get_dtype({}) == "object"

    def test_for_object_with_dict(self):
        assert get_dtype({"a":"test"}) == "object"

    def test_for_byte(self):
        assert get_dtype(b"11") == "binData"

class TestGetInt(object):
    def test_for_int_with_zero(self):
        assert _get_int(0) == "int"

    def test_for_int_with_positive_integer(self):
        assert _get_int(42) == "int"

    def test_for_int_with_negative_integer(self):
        assert _get_int(-42) == "int"

    def test_for_int_with_pi(self):
        assert _get_int(math.pi) == "int"

    def test_for_int_with_positive_long(self):
        assert _get_int(2147483648) == "long"

    def test_for_int_with_border_positive_int(self):
        assert _get_int(2147483647) != "long"

    def test_for_int_with_negative_long(self):
        assert _get_int(-2147483649) == "long"

    def test_for_int_with_border_negative_int(self):
        assert _get_int(-2147483647) != "long"

    def test_for_int_with_infinity(self):
        assert _get_int(math.inf) == "long"
        assert _get_int(math.inf) != "int"
