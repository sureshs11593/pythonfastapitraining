"""SLI/SLO definitions + CMM level 1-5 checklist - Appendix A.1 / A.7.
In the context of CMMI (Capability Maturity Model Integration), SLI and SLO are commonly used in IT Service Management (ITSM), DevOps, SRE (Site Reliability Engineering), and software quality measurement. They are not official CMMI maturity level terms, but they support CMMI practices related to process measurement, quality, and performance.

1. SLI (Service Level Indicator)

A Service Level Indicator (SLI) is a quantitative metric that measures a specific aspect 
of a service's performance.

Examples:

API availability (%)
Response time (milliseconds)
Error rate (%)
Throughput (requests per second)
CPU utilization
Database latency

Example:

Website Availability = 99.95%
Average API Response Time = 180 ms
Error Rate = 0.2%

2. SLO (Service Level Objective)

A Service Level Objective (SLO) is the target or goal that you want your SLI to achieve.

Examples:

SLI	                                                    SLO
Availability	                                ≥ 99.9%
Response Time	                        < 200 ms
Error Rate	                                < 1%
Login Success Rate	                    > 99.5%
Incident Resolution	                    < 4 hours

Example:

SLI:
Average Response Time = 180 ms

SLO:
Average Response Time must be less than 200 ms

Since 180 ms < 200 ms, the SLO is met.

SLI vs SLO
SLI	                                                SLO
Measurement	                                Target
What is happening?	                    What should happen?
Metric	                                            Goal
Current performance	                Expected performance

Example:

SLI = 99.85% uptime
SLO = 99.90% uptime

Result:

SLO NOT met
SLA (Service Level Agreement)

People often confuse SLA, SLO, and SLI.

Term	                                    Meaning
SLI	                                        Measurement
SLO	                                        Target
SLA	                                        Contract with customer

Example

SLI:

Availability = 99.93%

SLO:

Target Availability = 99.9%

SLA:

If availability drops below 99.5%, the customer receives a service credit.
==================================================
How They Relate to CMMI Maturity Levels

SLIs and SLOs support several CMMI process areas:

CMMI Level	                    Focus	                                    Role of SLI/SLO:

Level 2 –Managed	    Basic project monitoring	        Measure service and process 
                                                                                         performance using SLIs.
Level 3 – Defined	    Standardized processes	            Define organization-wide SLIs and SLOs
                                                                                            for consistency.
Level 4 – Quantitatively Managed	Data-driven mngt	    Use SLIs to statistically monitor performance against SLOs and take corrective action.
Level 5 – Optimizing	Continuous improvement	        Analyze SLI trends to improve processes and set progressively better SLOs.

Example: Online Banking Application

Metric	                                    SLI	                                SLO
Availability	                        99.97%	                        ≥ 99.95%
API Response Time	            60 ms	                        ≤ 200 ms
Error Rate	                            0.4%	                        ≤ 1%
Login Success Rate	            99.8%	                        ≥ 99.5%
Incident Resolution Time	    2.5 hours	                ≤ 4 hours


SLI (Service Level Indicator) is a measurable metric that indicates the current 
of a service, such as uptime, latency, or error rate. 

SLO (Service Level Objective) is 
the desired target for that metric. 

In CMMI, particularly at Levels 4 and 5,
organizations use SLIs and SLOs to quantitatively manage process performance, 
monitor quality, and drive continuous improvement.

In a real org this would live as a checked-in slo.yaml reviewed alongside
the OpenAPI contract (Module 7.4 pattern applied to SLOs).
"""

SLO_DEFINITION = {
    "service": "orders-training-api",
    "slis": [
        {"name": "availability", "definition": "successful_requests / total_requests"},
        {"name": "latency_p95", "definition": "95th percentile of request duration in ms"},
    ],
    "slos": [
        {"sli": "availability", "target": "99.9%", "window": "rolling 30 days"},
        {"sli": "latency_p95", "target": "< 300ms", "window": "rolling 30 days"},
    ],
}

_self_assessment_state: dict = {}

CMM_LEVELS = [
    {
        "level": 1,
        "name": "Initial (ad hoc)",
        "observability": "No structured logs, no metrics; debugging via print()/manual server access",
        "slo_practice": "No SLOs defined; readiness checked manually before releases",
    },
    {
        "level": 2,
        "name": "Repeatable / Managed",
        "observability": "Basic access logs exist; a /health endpoint is present",
        "slo_practice": "Informal targets ('should be fast'); manual smoke tests after deploy",
    },
    {
        "level": 3,
        "name": "Defined",
        "observability": "Standardized structured JSON logs w/ request ID; /metrics endpoint;documented schema",
        "slo_practice": "SLIs formally defined; SLOs documented and reviewed;automated compliance tests in CI",
    },
    {
        "level": 4,
        "name": "Quantitatively Managed",
        "observability": "Dashboards track SLIs continuously; distributed tracing; alerting on SLO burn rate",
        "slo_practice": "Error budgets calculated and tracked; automated SLO regression tests gate deploys",
    },
    {
        "level": 5,
        "name": "Optimizing",
        "observability": "Predictive/anomaly alerting; auto-remediation; chaos/fault-injection testing",
        "slo_practice": "SLO-driven progressive delivery with auto-rollback on burn-rate breach",
    },
]

