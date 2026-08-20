class IdempotencyStore:
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    def get(self, key: str) -> dict | None:
        return self._store.get(key)

    def save(self, key: str, response_body: dict) -> None:
        self._store[key] = response_body


idempotency_store = IdempotencyStore()
