# OmniRoute

**Type:** AI Gateway / Multi-Provider LLM Router  
**Status:** Active  
**Sources:** [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)

## Summary
OmniRoute is a smart AI router with auto-fallback that provides a single OpenAI-compatible endpoint for multiple AI providers. It handles provider health, circuit breaking, load balancing, and token compression.

## Key Features
- **Unified Endpoint:** `http://localhost:20128/v1` for all providers
- **18 Free-Tier Providers:** Groq, Cerebras, NVIDIA NIM, DeepSeek, Gemini, etc.
- **4 Routing Combos:** Flagship-Coding, Vision-Multimodal, High-Throughput, Balanced-General
- **Resilience:** Circuit breakers (12 failures/30s), cooldown/backoff, P2C load balancing
- **Compression:** Caveman (rule-based) + RTK (command-aware) active
- **Format Translation:** OpenAI ↔ Anthropic ↔ Gemini auto-morph

## Configuration
- **Server:** `omniroute serve` on port 20128
- **Admin Password:** Set via `omniroute setup --password`
- **Provider Keys:** Stored encrypted in `~/.config/omniroute/storage.sqlite`
- **Active Combo:** Balanced-General (P2C strategy)

## Provider Tiers
| Tier | Providers | Strategy |
|------|-----------|----------|
| Flagship | DeepSeek, Cerebras, Groq, NVIDIA, OpenRouter | Priority |
| Vision | Gemini, NVIDIA, Groq, OpenRouter | Priority |
| High-Throughput | Cerebras, Groq, Friendli, SambaNova, Baseten, Nebius | Least-used |
| General | DeepInfra, Novita, Inference.net, OpenVecta, Requesty, Groq-8B, Cerebras-8B | P2C |

## Related
- [OmniRoute Infrastructure](../projects/omniroute-infrastructure.md)
- [OpenViking Integration](../projects/openviking-integration.md)
