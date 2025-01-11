import asyncio
import base64
import datetime
import json
import re
import uuid
from decimal import Decimal
from io import BytesIO
from pathlib import Path

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None

try:
    from bson import ObjectId
    from bson.decimal128 import Decimal128
except ImportError:
    Decimal128 = None
    ObjectId = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from PIL import Image
except ImportError:
    Image = None


class JSONSerializer(json.JSONEncoder):
    def default(self, obj):
        # Text Type:	str
        # Numeric Types:	int, float, complex
        # Sequence Types:	list, tuple, range
        # Mapping Type:	dict
        # Set Types:	set, frozenset
        # Boolean Type:	bool
        # Binary Types:	bytes, bytearray, memoryview
        # None Type:	NoneType
        if isinstance(
            obj,
            (
                str,
                int,
                float,
                complex,
                list,
                tuple,
                range,
                dict,
                set,
                frozenset,
                bool,
                type(None),
            ),
        ):
            return str(obj)
        if isinstance(obj, (bytes, bytearray, memoryview)):
            base64_str = base64.b64encode(bytes(obj)).decode("utf-8")
            return f"data:application/octet-stream;base64,{base64_str}"
        if isinstance(obj, BytesIO):
            base64_str = base64.b64encode(obj.getvalue()).decode("utf-8")
            return f'data:application/octet-stream;base64,{base64.b64encode(obj.getvalue()).decode("utf-8")}'
        if Image and isinstance(obj, Image.Image):
            buffered = BytesIO()
            format = (
                getattr(obj, "format", "PNG") or "PNG"
            )  # Get original format or default to PNG
            obj.save(buffered, format=format)
            base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/{format.lower()};base64,{base64_str}"
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S.%f")
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, Path):
            return str(obj)
        if hasattr(obj, "to_json"):
            return obj.to_json()
        if BaseModel and isinstance(obj, BaseModel):
            return obj.model_dump()
        if ObjectId and isinstance(obj, ObjectId):
            return str(obj)
        if Decimal128 and isinstance(obj, Decimal128):
            return str(obj)
        if isinstance(obj, Exception):
            return repr(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        if pd and isinstance(obj, pd.Series):
            return obj.to_dict()
        if np and isinstance(obj, np.ndarray):
            return obj.tolist()
        if callable(obj) or asyncio.iscoroutine(obj):
            import warnings

            func_name = getattr(obj, "__name__", str(obj))
            warnings.warn(
                f"Attempting to serialize function/coroutine '{func_name}' which is not supported"
            )
            raise ValueError(
                f"Attempting to serialize function/coroutine '{func_name}' which is not supported"
            )
        return super().default(obj)


def json_deserializer(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            # Try to parse JSON strings that might be from pandas Series
            if value.startswith("{") and value.endswith("}"):
                try:
                    dct[key] = loads(value)
                    continue
                except json.JSONDecodeError:
                    pass

            # Data URL decoding (handles bytes, bytearray, memoryview, BytesIO, and Images)
            if value.startswith("data:"):
                try:
                    mime_type, b64data = value[5:].split(";base64,", 1)
                    binary_data = base64.b64decode(b64data)

                    if mime_type.startswith("image/") and Image:
                        dct[key] = Image.open(BytesIO(binary_data))
                    elif mime_type == "application/octet-stream":
                        dct[key] = binary_data
                    continue
                except (ValueError, TypeError):
                    pass

            # Non-serializable function references (skip conversion)
            if value.startswith("<non-serializable-function:"):
                continue

            # UUID conversion
            if re.match(
                r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
                value,
            ):
                try:
                    dct[key] = uuid.UUID(value)
                    continue
                except ValueError:
                    pass

            # Datetime patterns
            datetime_patterns = [
                # ISO format with timezone
                (
                    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$",
                    lambda v: datetime.datetime.fromisoformat(v.replace("Z", "+00:00")),
                ),
                # Date and time
                (
                    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?$",
                    lambda v: datetime.datetime.strptime(
                        v, "%Y-%m-%d %H:%M:%S.%f" if "." in v else "%Y-%m-%d %H:%M:%S"
                    ),
                ),
                # Date only
                (
                    r"^\d{4}-\d{2}-\d{2}$",
                    lambda v: datetime.datetime.strptime(v, "%Y-%m-%d").date(),
                ),
                # Time with microseconds
                (
                    r"^\d{2}:\d{2}:\d{2}\.\d+$",
                    lambda v: datetime.datetime.strptime(v, "%H:%M:%S.%f").time(),
                ),
                # Time without microseconds
                (
                    r"^\d{2}:\d{2}:\d{2}$",
                    lambda v: datetime.datetime.strptime(v, "%H:%M:%S").time(),
                ),
            ]

            for pattern, parser in datetime_patterns:
                if re.match(pattern, value):
                    try:
                        dct[key] = parser(value)
                        break
                    except ValueError:
                        continue

    return dct


def dumps(*args, **kwargs):
    kwargs.setdefault("cls", JSONSerializer)
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs.setdefault("cls", JSONSerializer)
    return json.dump(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs.setdefault("object_hook", json_deserializer)
    return json.loads(*args, **kwargs)


def load(*args, **kwargs):
    kwargs.setdefault("object_hook", json_deserializer)
    return json.load(*args, **kwargs)
