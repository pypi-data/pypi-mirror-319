import base64
from datetime import datetime
from io import BytesIO, StringIO
from uuid import uuid4

from json_advanced.json_encoder import dump, dumps, load


def test_dump_load_file():
    # Test data
    data = {
        "string": "hello",
        "bytes": bytes([1, 2, 3]),
        "datetime": datetime.now(),
        "uuid": uuid4(),
    }

    # Test with StringIO
    string_buffer = StringIO()
    dump(data, string_buffer)
    string_buffer.seek(0)  # Reset buffer position to start
    loaded_data = load(string_buffer)

    # Verify data
    assert loaded_data["string"] == data["string"]
    assert loaded_data["bytes"] == data["bytes"]
    assert isinstance(loaded_data["datetime"], datetime)
    assert loaded_data["uuid"] == data["uuid"]


def test_dump_load_binary_file():
    data = {
        "string": "hello",
        "bytes": bytes([1, 2, 3]),
    }

    # Test with BytesIO - need to write bytes
    binary_buffer = BytesIO()
    json_str = dumps(data)  # First get the JSON string
    binary_buffer.write(json_str.encode("utf-8"))  # Then encode to bytes
    binary_buffer.seek(0)
    loaded_data = load(binary_buffer)

    assert loaded_data["string"] == data["string"]
    # Get binary data from data URL
    assert isinstance(loaded_data["bytes"], bytes)
    assert loaded_data["bytes"] == data["bytes"]


def test_dump_load_nested_data():
    data = {
        "nested": {
            "string": "hello",
            "list": [1, 2, bytes([3, 4, 5])],
            "dict": {"date": datetime.now()},
        }
    }

    string_buffer = StringIO()
    dump(data, string_buffer)
    string_buffer.seek(0)
    loaded_data = load(string_buffer)

    assert loaded_data["nested"]["string"] == data["nested"]["string"]
    assert loaded_data["nested"]["list"][:2] == data["nested"]["list"][:2]
    # Get binary data from data URL
    binary_data = loaded_data["nested"]["list"][2]
    if isinstance(binary_data, str) and binary_data.startswith(
        "data:application/octet-stream;base64,"
    ):
        # Extract and decode base64 data
        _, b64data = binary_data.split(";base64,", 1)
        binary_data = base64.b64decode(b64data)
    assert isinstance(binary_data, bytes)
    assert binary_data == data["nested"]["list"][2]
