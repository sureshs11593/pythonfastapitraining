"""Cursor-based pagination helpers - Module 4.3."""

import base64
import json


def encode_cursor(last_id: str) -> str:
    raw = json.dumps({"id": last_id}).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def decode_cursor(cursor: str | None) -> str | None:
    if not cursor:
        return None
    raw = base64.urlsafe_b64decode(cursor.encode("utf-8"))
    return json.loads(raw)["id"]
