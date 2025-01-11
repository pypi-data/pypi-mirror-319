import pytest

from json_advanced.json_encoder import dumps, loads


@pytest.mark.skipif(not pytest.importorskip("PIL"), reason="PIL not installed")
def test_image_serialization(image_data):
    from PIL import Image

    json_string = dumps(image_data)
    deserialized = loads(json_string)

    assert isinstance(deserialized["image"], Image.Image)
    # Compare image attributes
    original = image_data["image"]
    decoded = deserialized["image"]
    assert original.size == decoded.size
    assert original.mode == decoded.mode
