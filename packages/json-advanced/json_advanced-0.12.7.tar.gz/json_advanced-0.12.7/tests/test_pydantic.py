from datetime import datetime
from uuid import UUID, uuid4

import pytest

from json_advanced.json_encoder import dumps, loads


@pytest.mark.skipif(
    not pytest.importorskip("pydantic"), reason="pydantic not installed"
)
def test_pydantic_serialization():
    from pydantic import BaseModel, Field

    class Item(BaseModel):
        uid: UUID = Field(default_factory=uuid4)
        at: datetime = Field(default_factory=datetime.now)
        name: str
        price: float
        is_offer: bool | None = None

    data = Item(name="item", price=1.0)
    json_string = dumps(data)
    deserialized = loads(json_string)

    assert deserialized["name"] == data.name
    assert deserialized["price"] == data.price
    assert deserialized["uid"] == data.uid
    assert isinstance(deserialized["at"], datetime)
