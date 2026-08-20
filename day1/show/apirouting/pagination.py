"""Cursor-based pagination helpers - Module 4.3."""

import base64
import json
'''
This code encodes and decodes a cursor value for pagination.
Encode_cursor turns an item ID into a URL-Safe Base64 token.

decode_cursor converts that token back into the orginal ID.
'''


def encode_cursor(last_id: str) -> str:
    raw = json.dumps({"id": last_id}).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def decode_cursor(cursor: str | None) -> str | None:
    if not cursor:
        return None
    raw = base64.urlsafe_b64decode(cursor.encode("utf-8"))
    return json.loads(raw)["id"]
