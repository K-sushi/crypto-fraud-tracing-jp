# Phase 7: Report Generation

## Report Structure

```
reports/case_study_{protocol}_v{N}.md
```

### Sections (in order)

1. **Executive Summary** — 1 paragraph, key findings, amounts
2. **Incident Overview** — date, protocol, vulnerability type, amount stolen
3. **Attacker Addresses** — table: label, address, chain, role
4. **Attack Sequence** — chronological with tx hashes
5. **Vulnerability Analysis** — technical root cause (brief, reference existing analysis)
6. **Fund Flow** — source → exploit → distribution → laundering
7. **Cross-Chain Activity** — bridge transfers, multi-chain operations
8. **Privacy Tool Usage** — TC/Railgun/Chainflip details
9. **Behavioral Profile** — CV, timezone, cognitive, tempo (Phase 6 output)
10. **OSINT Findings** — ENS, contract sigs, social, CEX touchpoints
11. **Serial Exploiter Analysis** — cross-incident comparison
12. **Fund Recovery Assessment** — triage: laundered %, recoverable %, unknown %
13. **Recommendations** — for protocol, for law enforcement, for recovery
14. **Methodology Notes** — data sources, tools, limitations
15. **Evidence Inventory** — link to evidence/ directory, API call count, hash summary
16. **Confidence Ratings** — per-finding confidence summary table
17. **Delta vs Public Analysis** — what this report adds beyond existing coverage

### Confidence Rating Scale

| Level | Meaning |
|:------|:--------|
| CONFIRMED | On-chain proof, cryptographically verified |
| HIGH | Strong evidence, multiple independent signals |
| MEDIUM | Reasonable inference, single strong signal |
| LOW | Weak inference, circumstantial |
| SPECULATIVE | Hypothesis only, needs validation |

## Evidence Packaging

1. `evidence/{case}_api_log.jsonl` — all API calls with SHA256 hashes
2. All transaction hashes listed in report
3. All addresses listed with chain identifiers
4. Timestamps in UTC throughout

## Sanitization for Public Release

Before publishing:
- Remove skill/methodology references (no SKILL.md paths)
- Remove internal tool names
- Keep all findings and evidence references
- Replace internal paths with generic descriptions

## HTML Report Generation

For interactive reports, generate self-contained HTML:
- Collapsible sections for each phase
- Fund flow visualization
- Timeline chart
- Mobile-responsive

## Output
- Markdown report at `reports/case_study_{protocol}_v{N}.md`
- Evidence log at `evidence/{case}_api_log.jsonl`
- Optional: HTML version at `reports/case_study_{protocol}_v{N}.html`
