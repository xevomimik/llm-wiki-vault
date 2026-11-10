# Karpathy LLM Wiki Gist

**Type:** GitHub Gist  
**Source:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f  
**Author:** Andrej Karpathy

## Summary
The original LLM Wiki methodology by Andrej Karpathy — a structured approach to building a shared memory layer for AI agents using a three-layer system.

## Core Principles

### 1. Index-First (`index.md`)
- **Content-oriented catalog** of everything in the wiki
- Each page: link + one-line summary + optional metadata
- Organized by category (entities, concepts, sources, etc.)
- LLM reads index first to find relevant pages, then drills in

### 2. Source Preservation
- Raw source material never modified
- Wiki pages cite raw sources
- Traceable citation chain: Wiki → Raw

### 3. Three Layers
| Layer | Purpose |
|-------|---------|
| Raw | Source material (immutable) |
| Wiki | Structured knowledge with citations |
| Schema | Agentic instructions/contract |

### 4. Automation
- Python scripts for ingestion, linting, querying
- Git for version control (save points)
- LLM updates index on every ingest

## Tools & Plugins
- **Obsidian Graph View:** Best for visualizing wiki shape
- **Marp:** Markdown slide decks from wiki content
- **Dataview:** Query page frontmatter

## Key Quote
> "The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them."

## Related
- [LLM Wiki](llm-wiki.md)
- [Wanderloots LLM Wiki Build](../sources/wanderloots-llm-wiki-build.md)
