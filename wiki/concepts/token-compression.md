# Token Compression

**Type:** Context Optimization  
**Status:** Active  
**Sources:** [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)

## Summary
Token compression reduces context size by removing redundancy while preserving essential information. OmniRoute uses two complementary compression engines.

## Engines

### Caveman (Rule-Based)
- Removes redundant lines, logs, noisy Git diffs
- Language packs for common patterns
- Output mode controls (summary, diff, full)
- Analytics track savings

### RTK (Command-Aware)
- Command-aware compression for tool output
- Terminal logs, build results, test output
- Preserves semantic structure of commands
- Strips boilerplate, keeps errors/results

## OmniRoute Configuration
- **Enabled:** Yes
- **Savings Target:** 30-50% token reduction
- **Applied To:** All provider requests automatically
- **Analytics:** Available via `omniroute compression stats`

## Related
- [OmniRoute](omniroute.md)
- [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)
