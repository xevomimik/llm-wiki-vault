# SOP-02: Combo Creation & Testing

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Create, configure, and validate routing combos in OmniRoute. Combos define model selection strategy (priority, round-robin, cost-optimized) for different use cases.

---

## Current Combos (9 Active)

| Combo | Strategy | Purpose |
|-------|----------|---------|
| FLAGSHIP | priority | Best reasoning/coding models first |
| ROUND-ROBIN | round-robin | Free model rotation |
| NVIDIA | priority | NVIDIA models only |
| GOOGLE | priority | Gemini models only |
| OPENROUTER | priority | OpenRouter models only |
| CEREBRAS | priority | Cerebras ultra-fast inference |
| CODING | priority | Code-specialized models |
| VISION-MULTIMODAL | priority | Vision + multimodal models |
| PS5LM PLUS | priority | Local PS5 fallback (always-on) |

---

## Combo Strategies

### Priority (Default)
Models tried in order until one succeeds. Best for: flagship, coding, vision.

### Round-Robin
Distributes requests across models evenly. Best for: free model rotation, load balancing.

### Cost-Optimized
Selects cheapest working model first. Best for: high-volume, cost-sensitive workloads.

---

## Procedure: Create New Combo

### 1. Define Combo in Config
Edit OmniRoute config (location varies — check `omniroute config path`):
```yaml
combos:
  my-new-combo:
    strategy: priority  # or round-robin, cost-optimized
    models:
      - provider/model-id
      - provider/model-id
    # Optional: fallback combo
    fallback: ROUND-ROBIN
```

### 2. Validate Config
```bash
omniroute config validate
```

### 3. Reload Combos (No Restart Needed)
```bash
omniroute combos reload
```

### 4. Test Combo
```bash
# Basic connectivity
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "my-new-combo", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'

# Test failover: temporarily disable first model, verify second responds
```

### 5. Test All Strategies
| Test | Priority | Round-Robin | Cost-Optimized |
|------|----------|-------------|----------------|
| First request hits model 1 | ✅ | ✅ | ✅ (cheapest) |
| Model 1 down → model 2 | ✅ | ✅ | ✅ |
| Even distribution | ❌ | ✅ | N/A |
| Cheapest-first | ❌ | ❌ | ✅ |

---

## Procedure: Modify Existing Combo

### Add Model
```bash
omniroute combos add-model <combo-name> <provider>/<model-id>
```

### Remove Model
```bash
omniroute combos remove-model <combo-name> <provider>/<model-id>
```

### Change Strategy
```bash
omniroute combos set-strategy <combo-name> <priority|round-robin|cost-optimized>
```

### Reorder (Priority Only)
Edit config directly, then `omniroute combos reload`

---

## Validation Checklist
- [ ] All models in combo are **individually tested and working** (per SOP-06)
- [ ] Combo responds to hello prompt
- [ ] Failover works (disable first model, verify second responds)
- [ ] Strategy behavior matches intent
- [ ] Updated in `wiki/omniroute/current_models_and_gaps.md`

---

## Current Gaps (Per Wiki)
- ❌ Priority (coding) — not created
- ❌ Vision-Multimodal — not created  
- ❌ Round-Robin (free) — not created
- ❌ Cost-Optimized — not created
- ❌ Auto-aliases — not configured

---

## Related SOPs
- SOP-01: Provider Onboarding
- SOP-04: Systemd Service Management
- SOP-06: Model Testing Protocol