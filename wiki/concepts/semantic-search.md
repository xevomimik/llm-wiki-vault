# Semantic Search

**Type:** Vector-Based Retrieval  
**Status:** Active  
**Sources:** [OpenViking Integration](../projects/openviking-integration.md), [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)

## Summary
Semantic search uses embeddings to find conceptually similar content, not just keyword matches. OpenViking provides scoped semantic search over the `viking://` filesystem.

## OpenViking Search
- **Scope:** Search specific directories (not flat index)
- **Commands:** `ov find "query"` / `ov search "query"`
- **API:** `POST /api/v1/search/find`
- **Headers:** `X-OpenViking-Account`, `X-OpenViking-User`

## Three-Tier Context
| Tier | Content | Use Case |
|------|---------|----------|
| L0 | One-sentence abstract | Quick relevance check |
| L1 | Overview with structure | Planning, drill-down decision |
| L2 | Full original content | Deep reading when needed |

## OmniRoute Integration
- Provider health checks use semantic similarity for model matching
- Combo routing can use semantic signals for provider selection

## Related
- [OpenViking](openviking.md)
- [OpenViking Integration](../projects/openviking-integration.md)
