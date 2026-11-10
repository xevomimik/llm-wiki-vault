# Agentic Memory

**Type:** Cross-Session Memory for AI Agents  
**Status:** Active  
**Sources:** [OpenViking Integration](../projects/openviking-integration.md), [Wanderloots Obsidian+Agentic AI](../sources/wanderloots-obsidian-agentic.md)

## Summary
Agentic memory is the persistent, cross-session memory layer for AI agents. Unlike RAG (retrieval), agentic memory captures user preferences, project state, and operational patterns — the "instructions to the librarian" for accessing world knowledge.

## Two Memory Layers

| Layer | System | Purpose |
|-------|--------|---------|
| **World Knowledge** | Obsidian + LLM Wiki | Facts, sources, structured knowledge (the library) |
| **Agentic Memory** | OpenViking | Preferences, project state, operational patterns (the librarian's instructions) |

## OpenViking Memory Types
- **Preferences:** Writing style, coding habits, UI preferences
- **Profile:** User identity, recurring context
- **Events:** Notable interactions, decisions
- **Entities:** People, projects, tools
- **Soul:** Core identity/values

## Hermes Integration
- **Provider:** OpenViking (enabled)
- **Recall Scope:** Shared (all peer memories)
- **Commit Threshold:** 20,000 pending tokens
- **Auto-Commit:** Session end, session switch, threshold

## Key Differences from RAG
| Aspect | RAG | Agentic Memory |
|--------|-----|----------------|
| Retrieval | Semantic similarity | Scoped + contextual |
| Persistence | Session-limited | Cross-session |
| Content | Document chunks | Structured facts + preferences |
| Update | Re-index | Incremental extraction |

## Related
- [OpenViking](openviking.md)
- [OpenViking Integration](../projects/openviking-integration.md)
