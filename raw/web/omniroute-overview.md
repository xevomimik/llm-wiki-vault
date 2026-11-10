# OmniRoute Overview

OmniRoute is a smart AI router with auto-fallback that provides a single OpenAI-compatible endpoint for multiple AI providers. It handles provider health, circuit breaking, load balancing, and token compression.

Key features:
- Unified endpoint: http://localhost:20128/v1 for all providers
- 18 free-tier providers including Groq, Cerebras, NVIDIA NIM, DeepSeek, Gemini
- 4 routing combos: Flagship-Coding, Vision-Multimodal, High-Throughput, Balanced-General
- Circuit breakers (12 failures/30s), cooldown/backoff, P2C load balancing
- Caveman + RTK token compression (30-50% savings)
- Format translation: OpenAI ↔ Anthropic ↔ Gemini auto-morph

Providers:
- Groq: LPU speed, 1000+ tok/s
- Cerebras: Fastest inference
- NVIDIA NIM: Nemotron-3-Ultra, Nemotron-3-VL
- DeepSeek: Best coding model (DeepSeek-Coder-V2)
- OpenRouter: 300+ models meta-routing
- Requesty: Free meta-routing
- DeepInfra: 50+ models
- Gemini: 2M context, video, multimodal
- Cohere: Command R+, embed v3
- Perplexity: Web search + reasoning
- xAI (Grok): Grok models
