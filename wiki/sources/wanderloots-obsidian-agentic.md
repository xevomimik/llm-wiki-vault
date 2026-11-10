# Wanderloots: Obsidian + Agentic AI

**Type:** Video Transcript  
**Source:** https://youtu.be/znj-WpMj1dI  
**Date:** 2026-07-23  
**Channel:** Wanderloots

## Summary
Complete workflow for connecting Obsidian to Agentic AI (Hermes) with three-tier access controls, Docker mount scoping, and LLM Wiki integration.

## Key Concepts

### Three-Tier Access
| Level | Folder | Agent Permissions |
|-------|--------|-------------------|
| 🔒 Private | `private/` | No access (no Docker mount) |
| 📖 Read-Only | `readonly/` | Read only (Docker mount `:ro`) |
| 📝 Read-Write | `readwrite/` | Full access (Docker mount `:rw`) |

### Docker Mount Scoping
```bash
# Read-only for agent
docker run -v /vault/readonly:/data:ro ...

# Read-write for ingestion
docker run -v /vault/readwrite:/data:rw ...

# No access
# (simply don't mount /vault/private)
```

### Hermes Integration
- **Built-in Skill:** OpenViking memory plugin
- **Profile-based:** Different access per profile
- **Scope Control:** `recall_scope: shared` or `peer`
- **Auto-Commit:** 20,000 token threshold

### LLM Wiki Integration
- Obsidian vault structured as LLM Wiki (Raw→Wiki→Schema)
- Hermes has built-in LLM Wiki skill
- Agent operates as "librarian" over the vault

## Implementation Steps
1. Create Obsidian vault in Hermes workspace folder
2. Create three folders: `private/`, `readonly/`, `readwrite/`
3. Configure Docker mounts for each access level
4. Install OpenViking plugin in Hermes
5. Set up OpenViking server (Quick Local or Custom)
5. Test access controls with file operations
6. Add Git version control
7. Structure vault for LLM Wiki (Raw→Wiki→Schema)

## Related
- [OpenViking Integration](../projects/openviking-integration.md)
- [LLM Wiki](llm-wiki.md)
