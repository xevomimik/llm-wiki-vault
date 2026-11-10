# LLM Wiki

**Type:** Shared Memory Layer Methodology  
**Status:** Active  
**Sources:** [Karpathy LLM Wiki Gist](../sources/karpathy-llm-wiki-gist.md), [Wanderloots LLM Wiki Build](../sources/wanderloots-llm-wiki-build.md)

## Summary
The LLM Wiki is a structured methodology for building a shared memory layer for AI agents and humans. It organizes knowledge as a three-layer system: Raw Sources → Structured Wiki → Agentic Schema.

## Core Layers

### Layer 1: Raw (Sources)
- **Location:** `raw/{youtube,papers,web}/`
- **Content:** Unprocessed source material (transcripts, PDFs, web clips)
- **Immutable:** Never modified after ingestion
- **Ingestion:** Web Clipper, manual download, API fetches

### Layer 2: Wiki (Structured Knowledge)
- **Location:** `wiki/{entities,concepts,projects,sources}/`
- **Content:** Extracted concepts, entities, relationships with citations
- **Catalog:** `index.md` — one-line summary per page, organized by category
- **Citations:** Every wiki page cites its raw sources

### Layer 3: Schema (Agentic Instructions)
- **Location:** `schema/{templates,skills}/`
- **Content:** `agents.md` (behavior contract), templates, custom skills
- **Purpose:** Contract between human and agent for wiki maintenance

## Key Principles
1. **Source Preservation:** Raw files never modified
2. **Citation Chain:** Wiki → Raw traceable
3. **Index-First:** `index.md` read before drilling into pages
4. **Schema Governance:** Agent follows `agents.md` contract
5. **Automation:** Python scripts + Git for repeatability

## Automation Scripts
| Script | Purpose |
|--------|---------|
| `ingest_raw.py` | Watch `raw/`, extract to `wiki/` with citations |
| `lint_wiki.py` | Link check, orphan detection, index update |
| `query_wiki.py` | Semantic search + cite |

## Related
- [Karpathy LLM Wiki Gist](../sources/karpathy-llm-wiki-gist.md)
- [Wanderloots LLM Wiki Build](../sources/wanderloots-llm-wiki-build.md)
