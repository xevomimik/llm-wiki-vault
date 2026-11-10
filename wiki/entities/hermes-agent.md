# Hermes Agent

**Type:** Self-Evolving AI Agent Harness  
**Status:** Active  
**Sources:** [Wanderloots Obsidian+Agentic AI](../sources/wanderloots-obsidian-agentic.md)

## Summary
Hermes Agent is a self-evolving AI agent platform by Nous Research with built-in skills, tools, and persistent memory. It supports multiple coding agents (Claude Code, Codex, OpenCode, etc.) and integrates with external memory providers.

## Key Features
- **Built-in Memory:** MEMORY.md / USER.md always active
- **Plugin System:** OpenViking, Mem0, Hindsight, Byterover, etc.
- **Skill System:** Sandbox/builtin/custom skills with `hermes skills`
- **Coding Agents:** Launch Claude Code, Codex, OpenCode via OmniRoute
- **Compression:** Context compression (Caveman/RTK) built-in
- **Terminal:** Local/Docker/Singularity/Modal/SSH backends

## Current Configuration
- **Model:** Nemotron-3-Ultra via OpenRouter
- **OmniRoute Endpoint:** `http://localhost:20128/v1`
- **Active Memory Provider:** OpenViking
- **OpenViking Plugin:** Installed and enabled
- **Memory Recall Scope:** Shared (all peer memories)

## Integrations
- **OmniRoute:** Routes all LLM calls through free-tier pool
- **OpenViking:** Long-term memory, semantic search, session compilation
- **MCP Server:** Tool calling for agents
- **A2A Server:** Agent-to-Agent protocol

## Related
- [OmniRoute](omniroute.md)
- [OpenViking](openviking.md)
- [Agentic Memory](agentic-memory.md)
