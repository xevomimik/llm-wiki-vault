# OmniRoute + Hermes System Architecture

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HERMES DESKTOP APP                          │
│  Config: provider=openai, base_url=http://localhost:20128/v1    │
│  Default Model: auto/best-free (routes via OmniRoute)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/REST (OpenAI-compatible)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OMNIROUTE GATEWAY                           │
│  Port: 20128  |  Process: omniroute serve                       │
│  Runtime: systemd user service (auto-start on boot)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  PROVIDER   │ │  PROVIDER   │ │  PROVIDER   │
    │   (Groq)    │ │  (NVIDIA)   │ │  (Gemini)   │
    └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  MODELS     │ │  MODELS     │ │  MODELS     │
    │ gpt-oss-120b│ │ nemotron-3  │ │ gemini-3    │
    │ gpt-oss-20b │ │ nemotron-3.5│ │ gemini-3.1  │
    │ qwen3.8-27b │ │ muse-glimmer│ │             │
    └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
              ┌─────────────────────────┐
              │      COMBOS (9)         │
              │  Strategy: priority/    │
              │  round-robin/cost-opt   │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   FAILOVER LOGIC        │
              │  Model 1 → Model 2 →    │
              │  Fallback Combo         │
              └─────────────────────────┘
```

---

## Components

### 1. Hermes Desktop App
- **Role:** Chat interface, model selection, conversation management
- **Config:** `~/.hermes/config.yaml`
- **Connection:** OpenAI-compatible client → `http://localhost:20128/v1`
- **Default Model:** `auto/best-free` (resolved by OmniRoute)

### 2. OmniRoute Gateway (Port 20128)
- **Role:** Inference router, provider abstraction, combo management, failover
- **Process:** `omniroute serve --config ~/.config/omniroute/config.yaml`
- **Service:** systemd user (`omniroute.service`)
- **Health:** `GET /health`, `GET /ready`
- **API:** OpenAI-compatible `/v1/chat/completions`, `/v1/models`

### 3. Providers (7 Configured, 5 Active)

| Provider | Type | Models | Status | Auth |
|----------|------|--------|--------|------|
| Groq | Cloud (Free) | 3 | ✅ Active | API Key |
| NVIDIA | Cloud (Free) | 8 | ✅ Active | API Key |
| Cerebras | Cloud (Free) | 1 | ✅ Active | API Key |
| Gemini | Cloud (Free) | 2 | ✅ Active | API Key |
| DeepSeek | Cloud (Free) | 1 | ✅ Active | API Key |
| DeepInfra | Cloud (Free) | 1 | ✅ Active | API Key |
| OpenRouter | Cloud (Free) | 0* | ✅ Active | API Key |
| PS5 Local | Local | 1 | ✅ Active | None |

*OpenRouter free model not in active catalog

### 4. Models (27 Working)

**By Provider:**
- **Groq (3):** `gpt-oss-120b`, `gpt-oss-20b`, `qwen3.8-27b` (vision)
- **NVIDIA (8):** `nemotron-3-ultra-550b-a55b`, `nemotron-3.5-super-vl-120b-a12b`, `nemotron-3.5-lightning-30b-a3b`, `nemotron-3-nano-omni-30b-a3b-reasoning`, `muse-glimmer-30b`, `laguna-xs-2.1`, `gemma-4-31b-it`, `diffusiongemma-26b-a4b-it`
- **Cerebras (1):** `gpt-oss-120b` (ultra-fast)
- **Gemini (2):** `gemini-3-flash-preview`, `gemini-3.1-flash-lite`
- **DeepSeek (1):** `deepseek-v4-flash` (falls back to NVIDIA)
- **DeepInfra (1):** `gpt-oss-120b` (falls back to NVIDIA)
- **PS5 Local (1):** `qwen3.5-9b` (registered as `LOCAL`)

### 5. Combos (9 Active)

| Combo | Strategy | Models (Priority Order) | Purpose |
|-------|----------|-------------------------|---------|
| FLAGSHIP | priority | Best reasoning/coding first | Primary daily driver |
| ROUND-ROBIN | round-robin | All free models | Load distribution |
| NVIDIA | priority | NVIDIA models only | NVIDIA-specific |
| GOOGLE | priority | Gemini models only | Google-specific |
| OPENROUTER | priority | OpenRouter models | OpenRouter-specific |
| CEREBRAS | priority | Cerebras models | Ultra-fast inference |
| CODING | priority | Code-specialized models | Development tasks |
| VISION-MULTIMODAL | priority | Vision-capable models | Image/multimodal |
| PS5LM PLUS | priority | Local PS5 model | Offline/privacy fallback |

---

## Failover Logic

### Request Flow
```
1. User sends request to combo (e.g., FLAGSHIP)
2. OmniRoute selects first model in combo priority list
3. Request forwarded to provider
4. On success: return response
5. On failure (timeout, 5xx, 429, auth error):
   a. Log failure
   b. Try next model in combo
   c. Repeat until success or exhausted
6. If combo exhausted: try fallback combo (if configured)
7. If all exhausted: return 503 to user
```

### Failure Types Handled
- **Timeout** (configurable, default 30s)
- **HTTP 5xx** (provider errors)
- **HTTP 429** (rate limited)
- **HTTP 401/403** (auth failed — triggers key rotation alert)
- **Network error** (DNS, connection refused)
- **Invalid response** (malformed JSON, empty content)

### NOT Handled (User Responsibility)
- **HTTP 400** (bad request — prompt too long, invalid params)
- **Content policy violations** (provider-specific)

---

## Data Flow

### Configuration
```
~/.config/omniroute/
├── config.yaml          # Combos, providers, models, routing rules
├── .env                 # ENCRYPTED API keys (SOPS/age)
└── catalog/             # Cached model catalogs (auto-generated)
```

### Runtime State
- In-memory only (no persistent DB)
- Model health tracked per-request
- Combo state: static config + dynamic health

### Logging
- systemd journal (`journalctl --user -u omniroute`)
- Structured JSON logs (configurable)
- Access logs: request/response metadata (no prompt content)

---

## Security Model

### Secrets Management
- **API Keys:** ONLY in `~/.config/omniroute/.env` (encrypted at rest via SOPS/age)
- **No keys in:** config.yaml, git, logs, memory, clipboard
- **Key Rotation:** Manual via SOP-03; never automated

### Network
- **OmniRoute binds:** `127.0.0.1:20128` (localhost only)
- **No external exposure** unless explicitly tunneled
- **Providers:** Outbound HTTPS only

### Access Control
- **Hermes → OmniRoute:** Local loopback, no auth
- **OmniRoute → Providers:** API key per provider
- **User → Hermes:** Desktop app auth (OS user session)

---

## Deployment Topology

### Current (Single Machine)
```
Laptop (Omarchy/Arch)
├── Hermes Desktop App
├── OmniRoute (systemd user service)
├── PS5 Local Model Server (192.168.4.32:8081) — separate device
└── LLM Wiki Vault (~/llm-wiki-vault)
```

### Future (Multi-Machine)
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Laptop     │     │  PS5        │     │  Server     │
│  (Primary)  │────▶│  (Local)    │     │  (Backup)   │
│             │     │  qwen3.5-9b │     │  OmniRoute  │
└─────────────┘     └─────────────┘     └─────────────┘
     │                    │                    │
     └────────────────────┴────────────────────┘
                          │
                   GitHub Sync (config/wiki)
```

---

## Monitoring & Observability

### Health Endpoints
- `GET /health` — Liveness (process alive)
- `GET /ready` — Readiness (providers loaded, combos valid)
- `GET /v1/models` — List all available models + combos

### Key Metrics (Manual)
- Request latency per model/combo
- Success rate per provider
- Failover frequency
- Token throughput

### Alerting (Manual)
- Daily: Check `/health` via cron
- Weekly: Test all combos (SOP-06 regression)
- On failure: Journal logs → investigate

---

## Disaster Recovery

### RTO/RPO Targets
- **RTO:** < 15 min (config restore + service start)
- **RPO:** 0 (config in Git, keys in password manager)

### Recovery Steps
1. Provision new Arch/Omarchy machine
2. Install OmniRoute, Hermes, Git, SOPS/age
3. Clone `omniroute-config` and `llm-wiki-vault`
4. Decrypt `.env` from backup
5. Restore systemd service
6. Start OmniRoute, verify health
7. Test all 9 combos

---

## Related Documentation
- `wiki/sops/01-provider-onboarding.md`
- `wiki/sops/02-combo-creation-testing.md`
- `wiki/sops/03-key-rotation-expiry.md`
- `wiki/sops/04-systemd-service-management.md`
- `wiki/sops/05-backup-restore-github.md`
- `wiki/sops/06-model-testing-protocol.md`
- `wiki/omniroute/current_models_and_gaps.md` (live model status)