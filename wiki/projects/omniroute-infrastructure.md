# OmniRoute Infrastructure

**Type:** Free-Tier Multi-Provider AI Gateway  
**Status:** Active (18 providers, 4 combos)  
**Sources:** [OmniRoute](omniroute.md), [OmniRoute Weekly Refresh](../skills/omniroute-weekly-refresh.md)

## Summary
Complete free-tier AI infrastructure using OmniRoute as a smart router. No credit card required for operation.

## Provider Pool (18 Active)

| Provider | Category | Strength |
|----------|----------|----------|
| Groq | Flagship/Throughput | LPU speed (1000+ tok/s) |
| Cerebras | Flagship/Throughput | Fastest inference |
| NVIDIA NIM | Flagship/Vision | Nemotron-3-Ultra, Nemotron-3-VL |
| DeepSeek | Flagship | Best coding model (DeepSeek-Coder-V2) |
| OpenRouter | Aggregator | 300+ models meta-routing |
| Requesty | Aggregator | Free meta-routing |
| DeepInfra | General | 50+ models |
| Gemini | Vision | 2M context, video, multimodal |
| Cohere | Embeddings | Command R+, embed v3 |
| Perplexity | Search | Web search + reasoning |
| xAI (Grok) | Flagship | Grok models |
| Nebius | General | Strong open models |
| Novita | Aggregator | 200+ models |
| FriendliAI | Throughput | Fast serving engine |
| Inference.net | Aggregator | Free tier |
| SambaNova | Throughput | Fast Llama-3.1-70B |
| Baseten | Throughput | 90-day trial |
| OpenVecta | Aggregator | Free tier |

## Routing Combos
| Combo | Strategy | Models |
|-------|----------|--------|
| Flagship-Coding | Priority | DeepSeek, Cerebras, Groq, NVIDIA, OpenRouter |
| Vision-Multimodal | Priority | Gemini, NVIDIA, OpenRouter, Groq |
| High-Throughput | Least-used | Cerebras, Groq, Friendli, SambaNova, Baseten, Nebius |
| Balanced-General | P2C | DeepInfra, Novita, Inference.net, OpenVecta, Requesty, Groq-8B, Cerebras-8B |

## Resilience
- **Circuit Breakers:** 12 failures/30s → open 30s
- **Cooldown:** 3s base, 5 steps exponential backoff
- **Quota Preflight:** Disabled (can enable per-provider)
- **Token Compression:** Caveman + RTK (30-50% savings)

## Maintenance
- **Weekly Refresh:** `omniroute-weekly-refresh` skill
- **Health Check:** `omniroute providers test-all`
- **Key Rotation:** Monthly check, 90-day expiry (Baseten)

## Related
- [OmniRoute](omniroute.md)
- [Weekly Refresh Skill](../skills/omniroute-weekly-refresh.md)
