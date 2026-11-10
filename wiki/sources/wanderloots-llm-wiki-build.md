# Wanderloots LLM Wiki Build

**Type:** Video Transcript + Implementation Guide  
**Source:** https://youtu.be/QbjAQFJJyt0  
**Date:** 2026-05-17  
**Channel:** Wanderloots

## Summary
Complete implementation guide for building an LLM Wiki in Obsidian with three core layers, Python+Git automation, local model support, and advanced features (Obsidian Firewall, local model launchers).

## Three Core Layers

### Layer 1: Raw (Sources)
- `raw/youtube/` — Web Clipper captures
- `raw/papers/` — PDF transcripts
- `raw/web/` — Web clips
- **Immutable:** Never modified after ingestion

### Layer 2: Wiki (Structured)
- `wiki/entities/` — People, tools, projects
- `wiki/concepts/` — Ideas, methodologies
- `wiki/projects/` — Active workstreams
- `wiki/sources/` — Source documentation
- `wiki/index.md` — Catalog (Karpathy style)

### Layer 3: Schema (Agentic)
- `schema/agents.md` — Agent behavior contract
- `schema/templates/` — Note templates
- `schema/skills/` — Custom skills

## Automation Scripts

| Script | Trigger | Purpose |
|--------|---------|---------|
| `check_raw_sources.py` | Manual/Watch | Find new raw files |
| `draft_wiki.py` | Manual | Extract concepts to proposed/ |
| `apply_latest_draft.py` | Manual | Commit proposed to wiki/ |
| `lint_wiki.py` | Git hook/CI | Link check, orphan detection, index update |
| `maintain_wiki.py` | Scheduled | Full maintenance pass |

## Local Model Workflow (Ollama)

### Launcher Commands
```bash
# Check raw sources
python check_raw_sources.py --model ollama

# Draft with local model
python draft_wiki.py --model ollama --source new_video.md

# Apply latest draft
python apply_latest_draft.py --overwrite
```

### Launcher Buttons (macOS .command / Windows .bat)
- Double-click to run without terminal
- Connect to Obsidian for seamless workflow

## Advanced Features

### 1. Obsidian Firewall (Agentic Firewall)
- Three vaults: `agent-vault` (RW), `human-vault` (RO), `private-vault` (None)
- Docker mount scoping per vault
- Prevents agent from accessing private/human-only content

### 2. Local Model Setup (Free + Private)
- **Ollama** for local inference
- **llama-cpp-python** for embedding
- **OpenViking Quick Local** for embedded server
- No cloud API keys needed

### 3. Advanced Querying
- RAG + Graph RAG for improved retrieval
- PDF ingest pipeline
- Molecular Zettelkasten (advanced knowledge theory)

## Vault Structure (Final)
```
vault/
├── raw/{youtube,papers,web}/
├── wiki/{entities,concepts,projects,sources,index.md}/
├── schema/{templates,skills,agents.md}/
├── proposed/           # Draft concepts awaiting review
├── scripts/            # Python automation
├── commands/           # Launcher .command/.bat files
├── .obsidian/          # Plugins, config
└── .git/               # Version control
```

## Key Principles
1. **Build once, use forever** — Foundation scales to 1000s of notes
2. **Index-first** — `index.md` catalog drives all retrieval
3. **Source preservation** — Raw never modified, Wiki cites Raw
4. **Schema governance** — `agents.md` is the contract
5. **Automation over manual** — Python + Git for repeatability

## Related
- [LLM Wiki](llm-wiki.md)
- [Karpathy LLM Wiki Gist](../sources/karpathy-llm-wiki-gist.md)
