from json_advanced.json_encoder import dumps, loads


def test_binary_serialization(binary_data):
    json_string = dumps(binary_data)
    deserialized = loads(json_string)

    # Test bytes
    assert isinstance(deserialized["binary"], bytes)
    assert deserialized["binary"] == binary_data["binary"]

    # Test BytesIO
    assert isinstance(deserialized["bytesio"], bytes)
    binary_data["bytesio"].seek(0)
    assert deserialized["bytesio"] == binary_data["bytesio"].getvalue()
