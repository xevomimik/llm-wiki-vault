# Agent Contract

**Purpose:** Govern agent behavior for LLM Wiki maintenance.  
**Binding:** All agents operating on this vault MUST follow these rules.

## Core Principles

1. **Source Preservation** — Never modify files in `raw/`. They are immutable sources.
2. **Citation Chain** — Every wiki page MUST cite its source(s) with relative paths.
3. **Index-First** — Read `wiki/index.md` before any query. Drill down from catalog.
4. **Schema Governance** — Follow this contract. Propose changes via Git PR.

## Permissions by Folder

| Folder | Permission | Notes |
|--------|------------|-------|
| `raw/` | Read-Only | Never write. Ingestion scripts only. |
| `wiki/` | Read-Write | Create/update concepts with citations. |
| `proposed/` | Read-Write | Draft concepts for human review. |
| `schema/` | Read-Only | Read contracts/templates. Changes via PR. |
| `scripts/` | Read-Only | Execute only. Modify via PR. |
| `private/` | No Access | Do not attempt to access. |

## Ingestion Workflow

When new raw sources appear in `raw/`:

1. **Detect** — Run `scripts/ingest_raw.py` or `scripts/check_raw_sources.py`
2. **Extract** — For each new source, extract concepts with citations
3. **Draft** — Write to `wiki/` (or `proposed/` for review)
4. **Cite** — Every concept MUST include `Source: [path](../raw/...)`
5. **Index** — Run `scripts/ingest_raw.py` to update `wiki/index.md`
6. **Lint** — Run `scripts/lint_wiki.py` to validate links

## Concept Format

Every wiki concept file MUST follow:

```markdown
# Concept Name

**Type:** Entity|Concept|Project|Source  
**Category:** entities|concepts|projects|sources  
**Source:** [path/to/source](../raw/...)  
**Extracted:** YYYY-MM-DDTHH:MM:SS

## Summary
One-line description.

## Details
Expanded content...

---
*Auto-extracted from [source](../raw/...)*
```

## Proposed Changes

For significant structural changes:
1. Create branch: `git checkout -b feature/description`
2. Modify `wiki/`, `schema/`, or `scripts/`
3. Run `scripts/lint_wiki.py` — must pass
4. Open PR with description of changes
5. Human review required for `schema/` changes

## Prohibited Actions

- ❌ Modify files in `raw/`
- ❌ Delete or move files in `raw/`
- ❌ Remove citations from wiki pages
- ❌ Edit `schema/agents.md` without PR
- ❌ Modify `scripts/` without PR
- ❌ Access `private/` folder

## Memory & Context

- **Long-term memory:** OpenViking (`viking://memories/`)
- **World knowledge:** This vault (`viking://resources/llm-wiki-vault/`)
- **Session memory:** OpenViking sessions
- **Recall:** Always check `wiki/index.md` first

## Version Control

- All changes tracked in Git
- Commit message format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `refactor`, `chore`
- Scopes: `wiki`, `schema`, `scripts`, `raw`, `index`

## Escalation

For conflicts or ambiguity:
1. Check this contract first
2. Check `schema/templates/` for patterns
3. Propose change via Git PR
4. Human decides

## Escalation

For conflicts or ambiguity:
1. Check this contract first
2. Check `schema/templates/` for patterns
3. Propose change via Git PR
4. Human decides

---
*This contract governs all agent operations on the LLM Wiki vault.  
Agents violating this contract will have access revoked.*
