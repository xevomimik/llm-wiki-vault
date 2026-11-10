# OpenViking

**Type:** Context Database for AI Agents  
**Status:** Active  
**Sources:** [OpenViking Integration](../projects/openviking-integration.md), [Wanderloots Obsidian+Agentic AI](../sources/wanderloots-obsidian-agentic.md)

## Summary
OpenViking is an open-source context database that organizes agent knowledge as a virtual filesystem under `viking://`. It provides semantic search, session memory, agent integration (MCP/A2A/Hermes plugin), and tenant/user/peer access control.

## Key Features
- **Virtual Filesystem:** `viking://resources/`, `viking://memories/`, `viking://skills/`
- **Three-Tier Context:** L0 (abstract), L1 (overview), L2 (details)
- **Semantic Search:** Scoped to directories, not flat index
- **Session Compilation:** `ov compile` → wiki, knowledge graph, reports
- **Agent Integration:** Hermes plugin (built-in), MCP server, A2A server
- **Access Control:** Tenant/user/peer with three-tier (private/RO/RW)

## Architecture
- **Server:** `openviking-server` on port 1933 (JSON config)
- **Storage:** SQLite + local vector DB + AGFS (RAG filesystem)
- **Embedding:** Local llama.cpp (bge-small-zh-v1.5, 512 dim)
- **VLM:** Nemotron-3-Ultra via OmniRoute (`http://localhost:20128/v1`)

## Configuration Files
- `~/.openviking/ov.conf` — Server config (JSON)
- `~/.openviking/ovcli.conf` — Client config
- `~/.openviking/data/` — Data directory

## Related
- [Hermes Agent](hermes-agent.md)
- [OpenViking Integration](../projects/openviking-integration.md)
