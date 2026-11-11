# SOP-01: Provider Onboarding

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Standard procedure for adding a new provider to OmniRoute with keys, testing models individually, and adding working models to combos.

---

## Prerequisites
- API key for the new provider
- Provider supported by OmniRoute (check `omniroute providers list`)
- OmniRoute running at `http://localhost:20128`

---

## Procedure

### 1. Add Provider Key to OmniRoute Encrypted Env
```bash
# Keys live ONLY in ~/.config/omniroute/.env (encrypted)
# Format: PROVIDER_API_KEY="sk-xxx"
# Never hardcode keys in config files
```

### 2. Restart OmniRoute to Pick Up New Key
```bash
systemctl --user restart omniroute
# Wait for healthy: curl -s http://localhost:20128/health
```

### 3. Import Models from Provider
```bash
# Import ALL models from provider (fetches catalog)
omniroute providers import <provider-name>

# Verify models appeared
omniroute models list --provider <provider-name>
```

### 4. Test Each Model Individually (CRITICAL)
**Never add untested models to combos.**

For each model returned:
```bash
# Test via OmniRoute chat endpoint
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "<provider>/<model-id>", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'
```

**Success criteria:**
- HTTP 200 response
- Valid JSON with `choices[0].message.content`
- Response latency acceptable (<30s for free tier)

**Record result:** Working / Failed / Throttled / Error

### 5. Add Working Models to Combos
Only after live test passes:
```bash
# Add to specific combo(s) by editing combo config
# Combos defined in OmniRoute config (YAML or via CLI)
omniroute combos add-model <combo-name> <provider>/<model-id> --strategy <priority|round-robin|cost-optimized>
```

### 6. Test Combo End-to-End
```bash
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "<combo-name>", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'
```

### 7. Document in LLM Wiki
Update `wiki/omniroute/current_models_and_gaps.md`:
- Add provider to Provider Status table
- Add working models to Working Models table
- Note any gaps or issues

---

## Rollback Procedure
If provider causes issues:
```bash
# Remove provider key from ~/.config/omniroute/.env
# Restart OmniRoute
systemctl --user restart omniroute
# Models from that provider auto-removed from catalog
# Combos auto-failover to next available model
```

**NEVER delete provider entries on transient errors** — only on confirmed permanent failure (billing exhausted, API deprecated, etc.)

---

## Video Workflow Reference
Exact steps from onboarding video:
1. Open `~/.config/omniroute/.env` in editor
2. Add `PROVIDER_API_KEY="..."`
3. Save, exit
4. `systemctl --user restart omniroute`
5. `omniroute providers import <provider>`
6. For each model: test via curl → record → add to combo if working
7. Update LLM Wiki

---

## Related SOPs
- SOP-02: Combo Creation & Testing
- SOP-03: Key Rotation & Expiry Handling
- SOP-06: Model Testing Protocol