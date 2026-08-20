"""Pydantic request/response schemas - Module 1.3.

Create / Update / Read are kept as separate models on purpose: the public
contract must never be coupled to internal storage shape.
"""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_serializer
'''
This schema will create Example Value
Schema
{
  "customer_id": "cust_42",
  "quantity": 3,
  "notes": "string"
}
in swagger doc for user convinence
'''


class OrderCreate(BaseModel):
    customer_id: str = Field(..., min_length=1, examples=["cust_42"])
    quantity: int = Field(..., gt=0, examples=[3])
    notes: Optional[str] = None

'''
This emits below information in swagger doc

Example Value
Schema
{
  "quantity": 1,
  "notes": "string",
  "status": "cancelled"
}
'''

class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(open|shipped|cancelled)$")

class OrderRead(BaseModel):
    id: str
    customer_id: str
    quantity: int
    notes: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_utc_z(self, dt: datetime) -> str:
        """Module 4.4 - always emit UTC, ISO-8601, trailing Z."""
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class PageMeta(BaseModel):
    next_cursor: Optional[str] = None
    has_more: bool
    limit: int


class OrderPage(BaseModel):
    data: list[OrderRead]
    page: PageMeta
