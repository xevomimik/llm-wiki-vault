# OpenViking Integration

**Type:** Memory + Obsidian + LLM Wiki Integration  
**Status:** Active  
**Sources:** [OpenViking](openviking.md), [Hermes Agent](hermes-agent.md), [Wanderloots Obsidian+Agentic AI](../sources/wanderloots-obsidian-agentic.md)

## Summary
OpenViking serves as the agent-facing context database, connecting Hermes Agent's memory to the Obsidian vault structured as an LLM Wiki.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Hermes     │────►│  OpenViking      │◄───►│  Obsidian Vault │
│  Agent      │ MCP │  Context DB      │     │  (LLM Wiki)     │
└─────────────┘     └──────────────────┘     └─────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
             ┌────────────┐ ┌────────────┐
             │ viking://  │ │ viking://  │
             │ memories/  │ │ resources/ │
             └────────────┘ └────────────┘
```

## Current Configuration

| Component | Setting |
|-----------|---------|
| OpenViking Server | `http://127.0.0.1:1933` |
| Hermes Plugin | Enabled (`openviking`) |
| Memory Recall Scope | `shared` |
| Commit Threshold | 20,000 tokens |
| Embedding | Local llama.cpp (bge-small-zh-v1.5) |
| VLM | Nemotron-3-Ultra via OmniRoute |

## Three-Tier Access (Wanderloots Method)

| Folder | Mount | Agent Access |
|--------|-------|--------------|
| `raw/` | Read-Write | Ingest sources, create wiki |
| `wiki/` | Read-Only | Search, cite, read |
| `schema/` | Read-Only | Read contracts, templates |
| `private/` | No Mount | Zero access |

## Data Flow

1. **Ingest:** Agent adds source to `raw/` → triggers `ingest_raw.py`
2. **Extract:** Script extracts concepts to `wiki/` with citations
3. **Index:** `index.md` updated, `lint_wiki.py` validates
4. **Commit:** Session committed to OpenViking → memories extracted
5. **Recall:** Future sessions query `viking://resources/` + `viking://memories/`

## OpenViking Skills for LLM Wiki

| Skill | Purpose |
|-------|---------|
| `ingest_raw` | Watch `raw/`, extract to `wiki/` with citations |
| `lint_wiki` | Link check, orphan detection, `index.md` update |
| `compile_wiki` | `ov compile` → knowledge graph from sessions |

## Related
- [OpenViking](openviking.md)
- [Hermes Agent](hermes-agent.md)
- [LLM Wiki](llm-wiki.md)
