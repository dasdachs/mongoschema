from pytest_mongodb.plugin import mongodb

from mongoschema.mongoschema import SchemaAnalyzer


def test_mock_mongo(mongodb):
    assert "employees" in mongodb.collection_names()

def test_SchemaAnalyzer_init(mongodb):
    s = SchemaAnalyzer(db="mongodb", collection="employees")
    s.analyze()
    print(s.schema)

class TestSchemaInit(object):
    pass


