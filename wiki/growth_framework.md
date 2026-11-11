# Growth Framework

**Version:** 1.0
**Last Updated:** 2026-11-11
**Status:** Active

---

## Purpose
Define the iteration cycle, review cadence, and metric tracking for continuous improvement of the OmniRoute + Hermes inference layer.

---

## Iteration Cycle

### Weekly Cycle (Every Monday)
**Time:** ~30 minutes
**Trigger:** Calendar reminder / start of work week

| Step | Action | Owner | Output |
|------|--------|-------|--------|
| 1 | **Provider Health Check** | Hermes | All 9 combos respond to hello prompt |
| 2 | **Credit Dashboard Review** | User | Free tier credits status per provider |
| 3 | **Key Expiry Scan** | Hermes | Keys expiring in <30 days flagged |
| 4 | **Model Catalog Refresh** | Hermes | `omniroute providers import` for active providers |
| 5 | **Test New/Changed Models** | Hermes | SOP-06 Level 1 smoke test |
| 6 | **Update Wiki** | Hermes | `current_models_and_gaps.md` current |
| 7 | **Git Commit** | Hermes | Weekly snapshot to both repos |

### Monthly Cycle (First Monday)
**Time:** ~60 minutes
**Trigger:** Calendar reminder

| Step | Action | Owner | Output |
|------|--------|-------|--------|
| 1 | **Full Regression Suite** | Hermes | All combos + flagship models tested (SOP-06) |
| 2 | **Provider Audit** | User + Hermes | New free providers evaluated (Mistral, Fireworks, Together, xAI, Anthropic) |
| 3 | **Combo Strategy Review** | User | Adjust priorities, add/remove models |
| 4 | **Performance Baseline** | Hermes | Latency p50/p95 per combo recorded |
| 5 | **SOP Review** | User | Update SOPs for any process changes |
| 6 | **Architecture Doc Update** | Hermes | `system_architecture.md` reflects current state |
| 7 | **Backup Verification** | Hermes | Restore test on staging (optional) |

### Quarterly Cycle (Jan/Apr/Jul/Oct)
**Time:** ~2 hours
**Trigger:** Calendar reminder

| Step | Action | Owner | Output |
|------|--------|-------|--------|
| 1 | **Full Disaster Recovery Drill** | Hermes | Restore to clean VM, verify all combos |
| 2 | **Key Rotation (Proactive)** | User + Hermes | Rotate high-value provider keys |
| 3 | **Model Landscape Survey** | User | New models, deprecated models, pricing changes |
| 4 | **Strategy Evolution** | User | New combo strategies, auto-aliases |
| 5 | **Tool/Infra Upgrade** | Hermes | OmniRoute, Hermes, systemd, OS updates |
| 6 | **Documentation Audit** | User | All SOPs, architecture, protocol current |

---

## Metric Tracking

### Primary Metrics (Tracked Weekly)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Combo Availability** | 100% (9/9 responding) | Hello prompt test |
| **Flagship Latency (p50)** | < 5s | `curl -w %{time_total}` |
| **Flagship Latency (p95)** | < 15s | 20 requests, sort |
| **Failover Rate** | < 5% of requests | OmniRoute logs |
| **Provider Error Rate** | < 1% per provider | HTTP 5xx/429 count |
| **Key Health** | 0 expired unnoticed | Dashboard check |

### Secondary Metrics (Tracked Monthly)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Model Diversity** | ≥ 3 providers per combo | Combo config audit |
| **Free Tier Utilization** | > 80% of requests | Provider request logs |
| **Local Fallback Readiness** | PS5LM PLUS responds < 10s | Direct test |
| **SOP Currency** | All SOPs < 90 days old | Git log check |
| **Wiki Completeness** | 0 "TODO" in architecture doc | Manual review |

### Leading Indicators (Watch List)

| Indicator | Warning Threshold | Action |
|-----------|-------------------|--------|
| Provider credit < 20% | Weekly check | Prep rotation |
| New model in catalog | On import | Test per SOP-06 |
| OmniRoute version behind | > 2 minor versions | Schedule upgrade |
| Hermes config drift | Any manual edit | Sync to repo |

---

## Review Cadence Summary

| Cadence | Duration | Focus | Artifacts Updated |
|---------|----------|-------|-------------------|
| **Weekly** | 30 min | Health, credits, keys, wiki | `current_models_and_gaps.md`, Git |
| **Monthly** | 60 min | Regression, providers, combos, perf | Architecture, SOPs, baselines |
| **Quarterly** | 2 hr | DR drill, rotation, landscape, upgrades | All docs, infra, strategies |

---

## Iteration Roles

| Role | Responsibilities |
|------|------------------|
| **User (Steward)** | Sets priority, approves changes, calls drift, owns provider relationships, decides combo strategy |
| **Hermes (Executor)** | Runs tests, updates docs, manages Git, executes SOPs, reports state, maintains infra |

---

## Decision Gates

### Add New Provider
- [ ] Free tier available
- [ ] API key obtained
- [ ] At least 1 model passes SOP-06 Level 1
- [ ] Added to `.env` (encrypted)
- [ ] Documented in wiki

### Add Model to Combo
- [ ] Model passes SOP-06 Level 1
- [ ] Capability matches combo purpose
- [ ] Combo strategy respected (priority order)
- [ ] Failover tested

### Change Combo Strategy
- [ ] User approves
- [ ] Config validated
- [ ] Regression suite passes
- [ ] Wiki updated

### Rotate Key
- [ ] New key obtained
- [ ] Old key marked (not deleted)
- [ ] OmniRoute restarted
- [ ] Smoke test passes
- [ ] Wiki updated

---

## Continuous Improvement Loop

```
┌─────────────┐
│   OBSERVE   │  Weekly metrics, user feedback, provider changes
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   ORIENT    │  Compare to targets, identify gaps
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   DECIDE    │  User chooses action (combo change, new provider, etc.)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    ACT      │  Hermes executes via SOPs
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   VERIFY    │  Tests pass, wiki current, Git committed
└──────┬──────┘
       │
       └──────▶ (back to OBSERVE)
```

---

## Tooling for Automation

### Desired (Not Yet Implemented)
- Cron job: Weekly health check → Git commit
- Cron job: Monthly regression → Report
- Alert: Provider credit < threshold → Notify
- Script: `omniroute-doctor` — full system check
- Dashboard: Local Grafana/Prometheus for metrics

### Current (Manual via SOPs)
- All steps executed manually per SOP
- Git commits manual
- Metrics recorded in wiki manually

---

## Version History
- **1.0 (2026-11-11):** Initial framework from partnership alignment