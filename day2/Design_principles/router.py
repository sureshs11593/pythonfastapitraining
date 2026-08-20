"""
Day 2 - Modules 5-6: API design principles & responsibility framework.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/day2", tags=["Design Principles & Responsibility"])


@router.get("/responsibility-matrix")
async def responsibility_matrix():
    """Module 5.2 - who owns what between the API team and infrastructure."""
    return {
        "api_team_owns": [
            "Resource & URL design",
            "Request/response contracts (OpenAPI)",
            "Business validation rules",
            "Status codes & error bodies",
            "Structured application logs",
            "Authentication/authorization logic",
            "API-level rate limit rules & SLOs",
        ],
        "shared_contract": [
            "SLOs / SLIs",
            "OpenAPI specification",
            "Log & metric schema",
            "Trace header propagation format",
        ],
        "infrastructure_team_owns": [
            "Load balancing / ingress",
            "TLS termination & certificate rotation",
            "Autoscaling / orchestration",
            "Network policy / firewalls",
            "Log & metrics pipeline operation (ELK, Grafana)",
            "Global rate-limit enforcement",
        ],
    }


@router.get("/url-design-examples")
async def url_design_examples():
    """Module 6.3 / 8.3 - resource modeling & no-verbs-in-paths rules."""
    return {
        "rule": "no verbs in URL paths; plural nouns for collections",
        "examples": [
            {"bad": "/getOrder?id=1", "good": "GET /orders/1"},
            {"bad": "/createOrder", "good": "POST /orders"},
            {"bad": "/deleteOrder/1", "good": "DELETE /orders/1"},
            {"bad": "/order/1/cancelOrder", "good": "POST /orders/1/cancel"},
            {"bad": "/customers/1/orders/1/items/1/notes/1/edit", "good": "PATCH /orders/1/items/1 (avoid deep nesting)"},
        ],
    }


@router.get("/api-checklist")
async def api_checklist():
    """Module 5.1 - what makes a standard API."""
    return [
        "Predictable: consistent naming, status codes, error shapes",
        "Discoverable: complete, accurate OpenAPI contract as source of truth",
        "Secure by default: authn/authz enforced centrally, never opt-in",
        "Observable: every request logged, measured, and traceable",
        "Stable: versioned, with a published deprecation lifecycle",
    ]
