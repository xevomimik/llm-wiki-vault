# OmniRoute Current Models & Agentic Orchestration Gaps

**Last Updated:** 2026-11-11  
**OmniRoute Version:** 3.8.53  
**Endpoint:** http://localhost:20128/v1

---

## ✅ Working Models (Tested 2026-11-11)

| Provider | Model | Capabilities | Notes |
|----------|-------|--------------|-------|
| **Groq** | `groq/openai/gpt-oss-120b` | Chat, reasoning | Flagship coding |
| **Groq** | `groq/openai/gpt-oss-20b` | Chat, reasoning | Fast, efficient |
| **Groq** | `groq/qwen/qwen3.8-27b` | Chat, vision | Vision support |
| **NVIDIA** | `nvidia/nvidia/nemotron-3-ultra-550b-a55b` | Chat, reasoning | Best reasoning (minimal throttling) |
| **NVIDIA** | `nvidia/nvidia/nemotron-3.5-super-vl-120b-a12b` | Vision, multimodal | Strong vision |
| **NVIDIA** | `nvidia/nvidia/nemotron-3.5-lightning-30b-a3b` | Chat, fast | High throughput |
| **NVIDIA** | `nvidia/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | Reasoning, omni | Reasoning model |
| **NVIDIA** | `nvidia/meta/muse-glimmer-30b` | Chat | |
| **NVIDIA** | `nvidia/poolside/laguna-xs-2.1` | Code | Code specialization |
| **NVIDIA** | `nvidia/google/gemma-4-31b-it` | Chat | |
| **NVIDIA** | `nvidia/google/diffusiongemma-26b-a4b-it` | Diffusion, chat | |
| **Cerebras** | `cerebras/gpt-oss-120b` | Chat, reasoning | Ultra-fast inference |
| **Gemini** | `gemini/gemini-3-flash-preview` | Chat, multimodal | |
| **Gemini** | `gemini/gemini-3.1-flash-lite` | Chat, fast | |
| **DeepSeek** | `deepseek/deepseek-v4-flash` | Chat, reasoning | Falls back to NVIDIA |
| **DeepInfra** | `deepinfra/openai/gpt-oss-120b` | Chat | Falls back to NVIDIA |

---

## ⚠️ Models Not Currently Working

| Provider | Model | Issue |
|----------|-------|-------|
| **OpenRouter** | `xingchen-agi/xing4.0-29b-a4b:free` | Not in active live catalog |
| **PS5 Local** | `ps5-qwen3.5-9b` | Provider name mismatch (registered as LOCAL) |

---

## 📋 Provider Status

| Provider | Status | Notes |
|----------|--------|-------|
| Groq | ✅ Active | 3/3 models working |
| NVIDIA | ✅ Active | 8/8 models working (minimal throttling) |
| Cerebras | ✅ Active | 1/1 working |
| Gemini | ✅ Active | 2/2 working |
| DeepSeek | ✅ Active | 1/1 working (falls back) |
| DeepInfra | ✅ Active | 1/1 working (falls back) |
| OpenRouter | ✅ Active | Free model not in catalog |
| PS5 Local | ✅ Active | Local model, name fix needed |

---

## 🎯 Agentic Orchestration Gaps

### Critical Missing Capabilities
| Capability | Current Status | Needed For |
|------------|----------------|------------|
| **Tool Calling / Function Calling** | Partial (Groq, NVIDIA support) | Agentic workflows, code execution |
| **Long Context (>128k)** | NVIDIA Nemotron 3 Ultra (550B) | Large codebases, document analysis |
| **Vision + Code Combined** | NVIDIA Nemotron 3.5 Super VL | UI generation, screenshot analysis |
| **Ultra-Fast Inference** | Cerebras gpt-oss-120b | Real-time agents, low latency |
| **Local Model (No Cloud)** | PS5 Local (needs name fix) | Privacy, offline, zero cost |
| **Structured Output / JSON Mode** | Unknown | Reliable parsing |

### Provider Gaps for Full Agentic Stack
| Gap | Recommended Provider | Why |
|-----|---------------------|-----|
| **Mistral** | `mistral` | Strong code, function calling |
| **Fireworks** | `fireworks` | Fast Llama, function calling |
| **Together AI** | `together` | Cheap, diverse models |
| **Anthropic (Claude)** | `anthropic` or `claude-code` | Best reasoning, agentic |
| **OpenAI** | `openai` | GPT-4o, o1, function calling |
| **xAI Grok** | `xai` | Large context, reasoning |
| **Voyage/Jina** | Embeddings | RAG, semantic search |

### Routing Strategy Gaps
| Strategy | Status | Need |
|----------|--------|------|
| **Priority (coding)** | ❌ Not created | Flagship-Coding chain |
| **Vision-Multimodal** | ❌ Not created | Vision + code chain |
| **Round-Robin (free)** | ❌ Not created | Free model rotation |
| **Cost-Optimized** | ❌ Not created | Cheapest-first routing |
| **Auto-Aliases** | ❌ Not configured | auto/best-free, auto/pro-coding |

---

## 🔧 Action Items

1. **Fix PS5 Local model name** — registered as `LOCAL` not `openai/ps5-qwen3.5-9b`
2. **Re-add OpenRouter with import-free-models** → test all → use working
3. **Create routing combos** per video workflow:
   - Flagship-Coding (priority)
   - Vision-Multimodal-Extended (priority)
   - Free-Round-Robin (round-robin)
   - Cost-Optimized-Free (cost-optimized)
4. **Add missing providers** (Mistral, Fireworks, Together, xAI, Anthropic)
5. **Configure auto-aliases**: auto/best-free, auto/pro-coding, auto/best-reasoning
6. **Test tool calling** on each working model
7. **Create startup script** for OmniRoute persistence
