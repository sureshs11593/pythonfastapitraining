"""Two response shapes for the SAME resource to demonstrate a breaking
change between v1 and v2 - Module 10.1."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderReadV1(BaseModel):
    """Legacy flat shape."""

    id: str
    customer_id: str
    quantity: int
    price: float
    created_at: datetime


class MoneyV2(BaseModel):
    amount: float
    currency: str = "USD"


class OrderReadV2(BaseModel):
    """v2 groups price into a structured `amount` object - a breaking change
    that justified the major version bump rather than an in-place edit."""

    id: str
    customer_id: str
    quantity: int
    amount: MoneyV2
    created_at: datetime


class OrderItemV2(BaseModel):
    id: str
    sku: str
    quantity: int


class PageMetaV2(BaseModel):
    next_cursor: Optional[str] = None
    has_more: bool
    limit: int


class OrderPageV2(BaseModel):
    data: list[OrderReadV2]
    page: PageMetaV2
