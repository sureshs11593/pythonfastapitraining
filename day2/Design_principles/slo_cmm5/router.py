"""Observability & SLO API Testing: CMM Levels 1-5.

Demo script (interactive, live in Swagger "Try it out"):
  GET  /appendix/slo/definition
  GET  /appendix/slo/cmm-levels
  GET  /appendix/slo/error-budget?total=10000&errors=5&target=0.999
       -> Exercise 4: error budget remaining
  GET  /appendix/slo/burn-rate?error_rate_last_hour=0.02&target=0.999
       -> Exercise 4/5: fast-burn alert decision
  POST /appendix/slo/self-assessment  {"level": 3, "item": "...", "result": "Pass"}
  GET  /appendix/slo/self-assessment
       -> Exercise/A.7: submit + retrieve the maturity checklist live
"""

from fastapi import APIRouter, HTTPException, Query

from slo_definitions import CMM_LEVELS, SLO_DEFINITION, _self_assessment_state
from app.core.config import AVAILABILITY_SLO_TARGET, FAST_BURN_RATE_THRESHOLD, LATENCY_P95_SLO_MS

router = APIRouter(prefix="/appendix/slo", tags=["Appendix A - Observability & SLO Testing (CMM 1-5)"])


@router.get("/definition")
async def get_slo_definition():
    return SLO_DEFINITION


@router.get("/cmm-levels")
async def get_cmm_levels():
    return CMM_LEVELS


@router.get("/error-budget")
async def error_budget(
    total: int = Query(..., gt=0, description="Total requests in the measurement window"),
    errors: int = Query(..., ge=0, description="Failed requests in the measurement window"),
    target: float = Query(AVAILABILITY_SLO_TARGET, gt=0, lt=1, description="Availability SLO target, e.g. 0.999"),
):
    """Exercise 4 (CMM Level 4): compute remaining error budget."""
    if errors > total:
        raise HTTPException(status_code=400, detail="VALIDATION_ERROR")
    allowed_error_rate = 1 - target
    allowed_errors = total * allowed_error_rate
    remaining_fraction = max(0.0, (allowed_errors - errors) / allowed_errors) if allowed_errors else 0.0
    return {
        "total_requests": total,
        "errors": errors,
        "slo_target": target,
        "allowed_errors_in_window": round(allowed_errors, 2),
        "error_budget_remaining_fraction": round(remaining_fraction, 4),
        "budget_exhausted": remaining_fraction <= 0.0,
        "recommendation": "halt risky deploys until budget recovers" if remaining_fraction <= 0.0 else "safe to deploy",
    }


@router.get("/burn-rate")
async def burn_rate(
    error_rate_last_hour: float = Query(..., ge=0, lt=1, description="Observed error rate over the last hour, e.g. 0.02"),
    target: float = Query(AVAILABILITY_SLO_TARGET, gt=0, lt=1),
):
    """Exercise 4/5 (CMM Level 4-5): fast-burn alert decision."""
    allowed_error_rate = 1 - target
    rate = error_rate_last_hour / allowed_error_rate if allowed_error_rate else float("inf")
    should_page = rate >= FAST_BURN_RATE_THRESHOLD
    return {
        "error_rate_last_hour": error_rate_last_hour,
        "slo_target": target,
        "burn_rate_multiplier": round(rate, 2),
        "fast_burn_threshold": FAST_BURN_RATE_THRESHOLD,
        "action": "PAGE_ON_CALL" if should_page else "OK",
    }


@router.get("/latency-slo")
async def latency_slo_check(p95_ms: float = Query(..., gt=0, description="Observed p95 latency in ms")):
    """Exercise 3 (CMM Level 3): latency SLO compliance check."""
    compliant = p95_ms < LATENCY_P95_SLO_MS
    return {"observed_p95_ms": p95_ms, "slo_target_ms": LATENCY_P95_SLO_MS, "compliant": compliant}


@router.post("/self-assessment", status_code=201)
async def submit_self_assessment(level: int, item: str, result: str):
    """Exercise/A.7: record Pass/Fail/Partial/N/A for a CMM-level checklist item."""
    if result not in {"Pass", "Fail", "Partial", "N/A"}:
        raise HTTPException(status_code=400, detail="VALIDATION_ERROR")
    key = f"L{level}:{item}"
    _self_assessment_state[key] = {"level": level, "item": item, "result": result}
    return _self_assessment_state[key]


@router.get("/self-assessment")
async def get_self_assessment():
    return list(_self_assessment_state.values())
