"""Bearer token auth - Module 4.1 / 4.2.

Two fake tokens are provided  of
401 (no/invalid token) vs 403 (authenticated but not permitted) vs
404 (resource does not exist):

    trainer-admin-token   -> role "admin"  (can create/update/delete)
    viewer-readonly-token -> role "viewer" (read-only)
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=False)

FAKE_TOKENS = {
    "trainer-admin-token": {"username": "trainer", "role": "admin"},
    "viewer-readonly-token": {"username": "viewer", "role": "viewer"},
}


async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    if creds is None or creds.credentials not in FAKE_TOKENS:
        raise HTTPException(status_code=401, detail="UNAUTHENTICATED")
    return FAKE_TOKENS[creds.credentials]


def require_role(role: str):
    """Dependency factory demonstrating authn vs authz (Module 4.2 / 9.3)."""

    async def checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] != role and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="FORBIDDEN")
        return user

    return checker
