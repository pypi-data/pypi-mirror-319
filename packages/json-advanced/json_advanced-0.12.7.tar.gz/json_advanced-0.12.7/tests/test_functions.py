import pytest

from json_advanced.json_encoder import dumps


def test_function_serialization():
    def test_func():
        pass

    data = {"func": test_func}
    with pytest.warns(
        UserWarning, match="Attempting to serialize function/coroutine.*"
    ):
        with pytest.raises(
            ValueError, match="Attempting to serialize function/coroutine.*"
        ):
            dumps(data)


@pytest.mark.asyncio
async def test_coroutine_serialization():
    async def test_coro():
        pass

    coro = test_coro()
    try:
        data = {"coro": coro}
        with pytest.warns(
            UserWarning, match="Attempting to serialize function/coroutine.*"
        ):
            with pytest.raises(
                ValueError, match="Attempting to serialize function/coroutine.*"
            ):
                dumps(data)
    finally:
        await coro  # Clean up the coroutine
