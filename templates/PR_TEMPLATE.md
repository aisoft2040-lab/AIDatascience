# Pull Request Template

## Purpose
- What problem does this PR solve? Why now?

## Changes
- List key changes (endpoints, configs, prompts, data flows).

## Screenshots / Evidence (optional)
- Add images/links/logs if helpful.

## Tests
- Unit: list new/updated tests and how to run them.
- Integration: describe any end-to-end checks.

## Metrics (Before → After)
| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Recall@5 |  |  |  |
| JSON Validity (%) |  |  |  |
| Latency p95 (ms) |  |  |  |
| Cost / Session ($) |  |  |  |
| Cache Hit Rate (%) |  |  |  |

## Safety & Compliance
- PII Handling: redaction/masking? any external transmission?
- Prompt Safety: injection protections, content filters.
- JSON Schema: enforced? validity rate?

## Rollout Plan
- Feature flag? shadow/beta/% rollout? rollback steps.

## Risks & Mitigations
- Risk 1: … → Mitigation: …
- Risk 2: … → Mitigation: …

## Checklist
- [ ] Feature flag wired and default OFF
- [ ] .env.example updated (no secrets committed)
- [ ] Unit tests added/updated (≥ N)
- [ ] JSON schema enforced (validator + tests)
- [ ] Metrics instrumented (latency, cost, hit rate)
- [ ] Docs updated (README/CHANGELOG/Runbook)

## Links
- Issue: 
- Design/Spec: 
- Dashboard/Logs: 
- Related PRs: 
