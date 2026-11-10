# Circuit Breaker

**Type:** Resilience Pattern  
**Status:** Active  
**Sources:** [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)

## Summary
Circuit breakers prevent cascade failures by stopping calls to failing providers. OmniRoute implements per-provider circuit breakers with automatic recovery.

## OmniRoute Configuration
- **Failure Threshold:** 12 failures / 30 seconds (API key providers)
- **Degradation Threshold:** 7 failures / 30 seconds
- **Reset Timeout:** 30 seconds
- **States:** Closed (normal) → Open (blocked) → Half-Open (probe)

## Behavior
1. **Closed:** Normal operation, requests pass through
2. **Open:** Provider blocked, requests fail fast, next provider tried
3. **Half-Open:** After reset timeout, probe request allowed; success → closed, failure → open

## Related
- [OmniRoute](omniroute.md)
- [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)
