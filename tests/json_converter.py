from typing import Any
from blacksheep.contents import Content
from essentials.json import dumps


def json_content(
    data: Any, content_type: bytes = b"application/json"
) -> Content:
    return Content(
        content_type,
        dumps(data, separators=(",", ":")).encode("utf8"),
    )
