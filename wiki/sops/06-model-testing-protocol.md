# SOP-06: Model Testing Protocol

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Standardized testing for every model before adding to combos. Ensures reliability, measures latency, validates capabilities.

---

## Test Levels

### Level 1: Smoke Test (Required for All Models)
**Goal:** Verify model responds via OmniRoute
```bash
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "<provider>/<model-id>", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'
```
**Pass Criteria:**
- HTTP 200
- Valid JSON response
- `choices[0].message.content` non-empty
- Latency < 30s (free tier)

### Level 2: Capability Test (Per Model Type)
**Goal:** Verify advertised capabilities work

| Capability | Test Prompt | Expected |
|------------|-------------|----------|
| **Chat/Reasoning** | "Explain quantum computing in 2 sentences" | Coherent explanation |
| **Code Generation** | "Write a Python fibonacci function" | Valid, runnable code |
| **Vision** | Image + "Describe this image" | Accurate description |
| **Tool Calling** | "What's the weather in Tokyo?" (with tools) | Tool call attempted |
| **Structured Output** | "Return JSON: {name: string, age: int}" | Valid JSON matching schema |
| **Long Context** | 50k token prompt + "Summarize" | Complete summary |

### Level 3: Stress Test (Flagship Models Only)
**Goal:** Verify production readiness
- 10 sequential requests, all succeed
- 5 concurrent requests, all succeed
- Latency p95 < 15s
- No degradation over 5 min

---

## Test Procedure

### 1. Pre-Test Checklist
- [ ] Provider key active in `.env`
- [ ] OmniRoute healthy (`/health` returns 200)
- [ ] Model imported (`omniroute models list --provider <name>`)
- [ ] Model ID exact (case-sensitive)

### 2. Run Smoke Test
```bash
MODEL="<provider>/<model-id>"
START=$(date +%s%N)
RESPONSE=$(curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"hello\"}], \"max_tokens\": 10}")
END=$(date +%s%N)
LATENCY_MS=$(( (END - START) / 1000000 ))
echo "Latency: ${LATENCY_MS}ms"
echo "$RESPONSE" | jq .
```

### 3. Run Capability Tests (If Applicable)
```bash
# Code test
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "'$MODEL'", "messages": [{"role": "user", "content": "Write a Python function to calculate fibonacci(n)"}], "max_tokens": 200}'

# Reasoning test
curl -s -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "'$MODEL'", "messages": [{"role": "user", "content": "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops Lazzies?"}], "max_tokens": 100}'
```

### 4. Record Results
Update `wiki/omniroute/current_models_and_gaps.md`:

| Provider | Model | Smoke | Code | Vision | Tools | JSON | Latency | Status |
|----------|-------|-------|------|--------|-------|------|---------|--------|
| Groq | gpt-oss-120b | ✅ | ✅ | ❌ | ✅ | ? | 2.1s | Working |

**Status Values:** `Working`, `Throttled`, `Failed`, `Partial`, `Untested`

---

## Decision Matrix

| Test Results | Action |
|--------------|--------|
| Smoke ✅ + Capabilities ✅ | Add to appropriate combo(s) |
| Smoke ✅ + Capabilities Partial | Add with capability notes; don't route for missing caps |
| Smoke ✅ + Throttled | Add to combo but mark as fallback only |
| Smoke ❌ | Do NOT add; investigate (key, catalog, provider status) |
| Intermittent | Test 3x over 1 hour; if 2/3 pass, add with warning |

---

## Testing New Providers (Batch)

When importing a new provider with many models:
```bash
# 1. Import all
omniroute providers import <provider>

# 2. Get model list
MODELS=$(omniroute models list --provider <provider> --format json | jq -r '.[].id')

# 3. Test each (script)
for model in $MODELS; do
  echo "Testing $model..."
  # Run smoke test, record result
done

# 4. Only add working models to combos
```

---

## Regression Testing

### When to Re-Test
- Provider key rotated
- OmniRoute updated
- Model added/removed from combo
- Weekly for flagship models

### Quick Regression Suite
```bash
# Test all combos
for combo in FLAGSHIP ROUND-ROBIN NVIDIA GOOGLE OPENROUTER CEREBRAS CODING VISION-MULTIMODAL "PS5LM PLUS"; do
  curl -s -X POST http://localhost:20128/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"$combo\", \"messages\": [{\"role\": \"user\", \"content\": \"hello\"}], \"max_tokens\": 10}" \
    -w "\n$combo: %{http_code} %{time_total}s\n" -o /dev/null
done
```

---

## Documentation Template
Add to `current_models_and_gaps.md` for each model:
```markdown
### <provider>/<model-id>
- **Tested:** 2026-11-11
- **Smoke:** ✅ 2.1s
- **Code:** ✅
- **Vision:** ❌
- **Tools:** ✅
- **JSON:** ❓ Untested
- **Status:** Working
- **Added to:** FLAGSHIP, CODING
- **Notes:** Best reasoning model available free tier
```

---

## Related SOPs
- SOP-01: Provider Onboarding (includes testing)
- SOP-02: Combo Creation & Testing (validates combo after adding models)
- SOP-03: Key Rotation & Expiry Handling (re-test after rotation)