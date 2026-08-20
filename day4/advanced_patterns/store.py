from datetime import datetime, timezone


class VersionedOrderStore:
    def __init__(self) -> None:
        now = datetime.now(timezone.utc)
        self._orders = {
            f"ord_{i:04d}": {
                # contains i loop variable , :04d is a decimal integer with leading zeros to width 4
                # ex: ord_0001
                "id": f"ord_{i:04d}",
                "customer_id": f"cust_{i:02d}",
                "quantity": i,
                "price": round(i * 9.99, 2),
                "created_at": now,
                "items": [{"id": f"item_{i}_1", "sku": f"SKU-{i}", "quantity": i}],
                "status": "open",
            }
            for i in range(1, 9)
        }

    def list(self, after_id, limit):
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

    def get(self, order_id):
        return self._orders.get(order_id)

    def cancel(self, order_id):
        order = self._orders.get(order_id)
        if order:
            order["status"] = "cancelled"
        return order


versioned_order_store = VersionedOrderStore()
