# SOP-03: Key Rotation & Expiry Handling

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Manage API key lifecycle: rotation on expiry, handling credit exhaustion, preserving keys for providers that may recover.

---

## Key Storage
**Single source of truth:** `~/.config/omniroute/.env` (encrypted)
```
GROQ_API_KEY="sk-xxx"
NVIDIA_API_KEY="sk-xxx"
GEMINI_API_KEY="sk-xxx"
DEEPSEEK_API_KEY="sk-xxx"
DEEPINFRA_API_KEY="sk-xxx"
OPENROUTER_API_KEY="sk-xxx"
# PS5_LOCAL_API_KEY="not-needed"  # Local model
```

**Never** store keys in:
- OmniRoute config YAML
- Git repos
- Clipboard history
- Plain text files

---

## Key States

| State | Action |
|-------|--------|
| **Active** | Working, models responding |
| **Throttled** | Rate limited — wait, do NOT rotate |
| **Credit Exhausted** | Mark expired, **keep key in .env**, remove models from catalog |
| **Revoked/Invalid** | Rotate immediately |
| **Expired (Time)** | Rotate before expiry if possible |

---

## Procedure: Rotate Key (Standard)

### 1. Obtain New Key
Get new API key from provider dashboard.

### 2. Update .env Atomically
```bash
# Edit ~/.config/omniroute/.env
# Replace OLD_KEY with NEW_KEY for that provider
# Save
```

### 3. Restart OmniRoute
```bash
systemctl --user restart omniroute
```

### 4. Verify
```bash
# Health check
curl -s http://localhost:20128/health

# Test a model from that provider
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "<provider>/<known-working-model>", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'
```

### 5. Update Documentation
- Note rotation date in `wiki/omniroute/current_models_and_gaps.md`
- Update Provider Status table if needed

---

## Procedure: Handle Credit Exhaustion (Free Tier)

**Critical Rule:** NEVER remove provider from `.env` on transient errors.

### 1. Confirm Exhaustion
- Multiple 429/402 errors over hours
- Provider dashboard shows $0 credit
- Other providers working normally

### 2. Mark Models as Failed (Not Provider)
```bash
# Remove failed models from catalog (they'll be re-added on next import)
omniroute models remove <provider>/<model-id>  # per model
# OR re-import provider to refresh catalog
omniroute providers import <provider>
```

### 3. Keep Key in .env
```bash
# DO NOT DELETE the API key line
# Comment it with status:
# GROQ_API_KEY="sk-xxx"  # CREDITS EXHAUSTED 2026-11-11 - keep for recovery
```

### 4. Update Wiki
Move provider to "Expired" section in `current_models_and_gaps.md`:
```markdown
| Groq | ⚠️ Expired | Credits exhausted 2026-11-11, key retained |
```

### 5. Recovery Monitoring
- Check provider dashboard weekly for credit refresh
- When credits restored: uncomment key, re-import, test models, restore to combos

---

## Procedure: Emergency Key Revocation

If key compromised:
1. **Immediately** revoke in provider dashboard
2. Generate new key
3. Follow standard rotation (above)
4. Audit logs for unauthorized usage

---

## Scheduled Maintenance

| Frequency | Task |
|-----------|------|
| Weekly | Check provider dashboards for credit status |
| Monthly | Verify all active keys still work (test one model per provider) |
| Quarterly | Rotate keys proactively for high-value providers (Anthropic, OpenAI when added) |

---

## Current Provider Key Status (2026-11-11)

| Provider | Status | Notes |
|----------|--------|-------|
| Groq | ✅ Active | Free tier, 3 models working |
| NVIDIA | ✅ Active | Free tier, 8 models working |
| Cerebras | ✅ Active | Free tier, 1 model working |
| Gemini | ✅ Active | Free tier, 2 models working |
| DeepSeek | ✅ Active | Free tier, falls back to NVIDIA |
| DeepInfra | ✅ Active | Free tier, falls back to NVIDIA |
| OpenRouter | ✅ Active | Free model not in catalog |
| PS5 Local | ✅ Active | No key needed |

**Expired (Keys Retained):**
- NVIDIA (old key) — retained per policy
- Cerebras (old key) — retained per policy
- OpenRouter (old key) — retained per policy

---

## Related SOPs
- SOP-01: Provider Onboarding
- SOP-04: Systemd Service Management
- SOP-05: Backup/Restore via GitHub