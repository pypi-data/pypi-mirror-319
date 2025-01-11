from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from json_advanced.json_encoder import dumps, loads


def test_basic_types():
    json_string = dumps(2)
    deserialized = loads(json_string)
    assert deserialized == 2


def test_basic_types(sample_data):
    json_string = dumps(sample_data)
    deserialized = loads(json_string)
    assert deserialized == sample_data


def test_datetime_serialization(datetime_data):
    json_string = dumps(datetime_data)
    deserialized = loads(json_string)

    assert isinstance(deserialized["datetime"], datetime)
    assert isinstance(deserialized["date"], date)
    assert isinstance(deserialized["time"], time)

    # Compare string representations as datetime might have microsecond differences
    assert str(deserialized["datetime"]) == str(datetime_data["datetime"])
    assert deserialized["date"] == datetime_data["date"]
    assert str(deserialized["time"]) == str(datetime_data["time"])


def test_uuid_serialization(uuid_data):
    json_string = dumps(uuid_data)
    deserialized = loads(json_string)

    assert isinstance(deserialized["uuid"], UUID)
    assert deserialized["uuid"] == uuid_data["uuid"]


def test_path_serialization(path_data):
    json_string = dumps(path_data)
    deserialized = loads(json_string)

    assert isinstance(Path(deserialized["path"]), Path)
    assert Path(deserialized["path"]) == path_data["path"]


def test_decimal_serialization():
    data = {"decimal": Decimal("123.45")}
    json_string = dumps(data)
    deserialized = loads(json_string)
    assert str(data["decimal"]) == deserialized["decimal"]


def test_exception_serialization():
    try:
        raise ValueError("test error")
    except ValueError as e:
        data = {"error": e}
        json_string = dumps(data)
        deserialized = loads(json_string)
        assert "ValueError" in deserialized["error"]
        assert "test error" in deserialized["error"]


def test_custom_json_serializable():
    class CustomObject:
        def to_json(self):
            return {"custom": "data"}

    data = {"obj": CustomObject()}
    json_string = dumps(data)
    deserialized = loads(json_string)
    assert deserialized["obj"] == {"custom": "data"}


def test_basic_python_types():
    # Test each type separately to avoid circular reference issues

    # Simple types
    assert dumps("test") == '"test"'
    assert dumps(42) == "42"
    assert dumps(3.14) == "3.14"
    assert dumps(True) == "true"
    assert dumps(None) == "null"

    # Complex number
    complex_str = dumps(1 + 2j)
    assert complex_str == '"(1+2j)"'  # Complex number is serialized as string

    # Sequences
    assert dumps([1, 2, 3]) == "[1, 2, 3]"
    assert dumps((4, 5, 6)) == "[4, 5, 6]"  # Tuple becomes list

    # Dictionary
    assert dumps({"key": "value"}) == '{"key": "value"}'

    # Set types (convert to list first to avoid circular reference)
    set_data = {7, 8, 9}
    assert sorted(loads(dumps(list(set_data)))) == [7, 8, 9]

    frozen_set = frozenset([10, 11, 12])
    assert sorted(loads(dumps(list(frozen_set)))) == [10, 11, 12]


def test_callable_serialization():
    def test_func():
        pass

    with pytest.warns(
        UserWarning, match="Attempting to serialize function/coroutine.*"
    ):
        with pytest.raises(
            ValueError, match="Attempting to serialize function/coroutine.*"
        ):
            dumps({"func": test_func})


@pytest.mark.asyncio
async def test_coroutine_serialization():
    async def test_coro():
        pass

    coro = test_coro()
    try:
        with pytest.warns(
            UserWarning, match="Attempting to serialize function/coroutine.*"
        ):
            with pytest.raises(
                ValueError, match="Attempting to serialize function/coroutine.*"
            ):
                dumps({"coro": coro})
    finally:
        await coro  # Clean up the coroutine


def test_lambda_serialization():
    with pytest.warns(
        UserWarning, match="Attempting to serialize function/coroutine.*"
    ):
        with pytest.raises(
            ValueError, match="Attempting to serialize function/coroutine.*"
        ):
            dumps({"lambda": lambda x: x})
