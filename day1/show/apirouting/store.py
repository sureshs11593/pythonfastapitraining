"""In-memory repository standing in for a database - kept deliberately simple
so the whole training project runs with zero external services."""

import itertools
import uuid
from datetime import datetime, timezone
from typing import Optional


class OrderStore:
    def __init__(self) -> None:
        self._orders: dict[str, dict] = {}
        self._seed()

    def _seed(self) -> None:
        now = datetime.now(timezone.utc)
        for i in range(1, 13):
            oid = f"ord_{i:04d}"
            self._orders[oid] = {
                "id": oid,
                "customer_id": f"cust_{i:02d}",
                "quantity": i,
                "notes": None,
                "status": "open",
                "created_at": now,
                "updated_at": now,
            }

    def list(self, after_id: Optional[str], limit: int) -> tuple[list[dict], bool]:
        ordered = sorted(self._orders.values(), key=lambda o: o["id"])
        start = 0
        if after_id:
            for idx, o in enumerate(ordered):
                if o["id"] == after_id:
                    start = idx + 1
                    break
        page = ordered[start : start + limit + 1]
        has_more = len(page) > limit
        return page[:limit], has_more

    def get(self, order_id: str) -> Optional[dict]:
        return self._orders.get(order_id)

    def create(self, customer_id: str, quantity: int, notes: Optional[str]) -> dict:
        oid = f"ord_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        order = {
            "id": oid,
            "customer_id": customer_id,
            "quantity": quantity,
            "notes": notes,
            "status": "open",
            "created_at": now,
            "updated_at": now,
        }
        self._orders[oid] = order
        return order

    def update(self, order_id: str, **fields) -> Optional[dict]:
        order = self._orders.get(order_id)
        if not order:
            return None
        for k, v in fields.items():
            if v is not None:
                order[k] = v
        order["updated_at"] = datetime.now(timezone.utc)
        return order

    def delete(self, order_id: str) -> bool:
        return self._orders.pop(order_id, None) is not None


order_store = OrderStore()
