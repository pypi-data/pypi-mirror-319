import pytest

from json_advanced.json_encoder import dumps, loads


@pytest.mark.skipif(not pytest.importorskip("numpy"), reason="numpy not installed")
def test_numpy_serialization():
    import numpy as np

    data = {"array": np.array([1, 2, 3])}
    json_string = dumps(data)
    deserialized = loads(json_string)
    assert isinstance(deserialized["array"], list)
    assert deserialized["array"] == [1, 2, 3]


@pytest.mark.skipif(not pytest.importorskip("pandas"), reason="pandas not installed")
def test_pandas_serialization():
    import pandas as pd

    data = {"series": pd.Series([1, 2, 3], index=["a", "b", "c"])}
    json_string = dumps(data)
    deserialized = loads(json_string)
    # The series is serialized as a JSON string, let's parse it
    if isinstance(deserialized["series"], str):
        deserialized["series"] = loads(deserialized["series"])
    assert isinstance(deserialized["series"], dict)
    assert deserialized["series"] == {"a": 1, "b": 2, "c": 3}


@pytest.mark.skipif(not pytest.importorskip("pandas"), reason="pandas not installed")
def test_pandas_series_serialization():
    import pandas as pd

    series = pd.Series([1, 2, 3], index=["a", "b", "c"])
    json_string = dumps({"series": series})
    deserialized = loads(json_string)
    assert deserialized["series"] == {"a": 1, "b": 2, "c": 3}
