SERVICE_NAME = "orders-training-api"
SERVICE_VERSION = "2.0.0"
'''
SLO stands for Service Level Objective
 - it is the target reliability goal a serivice is expected to meet,
 usually expressed as a percentage
 
 AVAILABILITY_SLO_TARGET=0.999
  means the service's availability target is 99.9%
  
  it means, the service should be available 99.9% of the time
  over a measurement period. That leaves only about .1% downtime allowed 
  which is rougly 43.8 min per month
  8.75 hours per year
  
  LATENCY_P95_SLO_MS=300
  means:
    - the service's latency SLO is 300milliseconds
    - P95 means the 95th percentile latency
    in practise, 95% of requests should complet within 300ms or less
    The remaining 5% can be slower, but the goal is the most requests stay
    under the threshold.
    
    FAST_BURN_RATE_THREASHOLD=14.4 
    means 
    - if the service is burning through its error budget at a rate of 14.4 times
    faster than it should, raise a high-severity alert
    
    in practical terms:
     - SLO budget is the allowed failure rate
     - a fast burn means the service is consuming that budget too quickly
     - 14.4 is teh multiplier used to decide that this is urget enough to page someone.
     So this line a threshold for triggering a page now alert when reliability is dropping too fast

'''


# SLO targets used across 
AVAILABILITY_SLO_TARGET = 0.999      # 99.9%
LATENCY_P95_SLO_MS = 300

# Fast-burn alert threshold : consuming budget this many
# times faster than sustainable triggers a page.
FAST_BURN_RATE_THRESHOLD = 14.4
