import pytest

from json_advanced.json_encoder import dumps, loads


@pytest.mark.skipif(not pytest.importorskip("bson"), reason="bson not installed")
def test_bson_types_serialization():
    from bson import ObjectId
    from bson.decimal128 import Decimal128

    data = {"object_id": ObjectId(), "decimal128": Decimal128("123.45")}
    json_string = dumps(data)
    deserialized = loads(json_string)
    assert isinstance(deserialized["object_id"], str)
    assert isinstance(deserialized["decimal128"], str)
