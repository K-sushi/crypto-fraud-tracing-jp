---
name: crypto-forensics
description: DeFi exploit on-chain 調査 / 行動 profiling / 資金追跡 / OSINT。発動→ hack 解析・attacker 特定・資金回収支援時
argument-hint: <phase|full> <target_address_or_case_name>
---

# Crypto Forensics Pipeline

Investigate DeFi exploits through 8 phases. Run the full pipeline or target a specific phase.

## Invocation

- `/crypto-forensics full 0xAttackerAddress` — all phases
- `/crypto-forensics opsec` — Phase 0 only
- `/crypto-forensics trace 0xAddress` — Phase 1-4 fund tracing
- `/crypto-forensics attribution 0xAddress` — Phase 5 OSINT
- `/crypto-forensics behavioral 0xAddress` — Phase 6 profiling
- `/crypto-forensics report case_name` — Phase 7 report generation

## Phase Overview

| Phase | Name | What it produces |
|:------|:-----|:-----------------|
| 0 | OPSEC | Secure workspace setup |
| 1 | Initial Mapping | Attacker address → first-hop graph |
| 2 | Cross-Chain | Bridge tracing (Stargate, Across, LayerZero, CCTP) |
| 3 | Privacy Tools | TC, Railgun, Chainflip analysis |
| 4 | TC Deanon | Deposit/withdrawal correlation |
| 5 | OSINT Attribution | ENS, contract sigs, CEX deposits, social |
| 6 | Behavioral | CV, timezone, cognitive style, tempo |
| 7 | Report | Structured report + evidence packaging |

## Phase Details

For detailed methodology per phase, Claude should read the relevant file:
- Phase 0: [phases/opsec.md](phases/opsec.md)
- Phase 1-4: [phases/fund-trace.md](phases/fund-trace.md)
- Phase 5: [phases/attribution.md](phases/attribution.md)
- Phase 6: [phases/behavioral.md](phases/behavioral.md)
- Phase 7: [phases/report.md](phases/report.md)

## API Configuration

Etherscan V2 unified endpoint (single key, 60+ chains):
```
source ~/.env.forensics  # ETHERSCAN_API_KEY
```

Free tier chains: ETH(1), Arbitrum(42161), Polygon(137), Sei(1329), Linea(59144), Scroll(534352)
Paid tier: BSC(56), Base(8453), Optimism(10)

## Evidence Preservation Protocol

EVERY API call must be:
1. Response hashed (SHA256)
2. Logged to `evidence/{case}_api_log.jsonl`
3. API key redacted from logs
4. Timestamp in UTC ISO-8601

Format:
```json
{"timestamp_utc":"...","url":"...","params":{...},"response_sha256":"...","result_count":N}
```

## Behavioral Template Script

For Phase 6, use the bundled script:
```bash
# Copy template, configure, execute
cp ${CLAUDE_SKILL_DIR}/scripts/behavioral_template.py scripts/{case}_behavioral.py
# Edit: CASE_NAME, ADDRESSES, CLAIMS
python scripts/{case}_behavioral.py
```

## Cross-Case Analysis

When multiple cases exist, compare:
- CV values (human confirmation threshold: >0.8)
- Timezone estimates (geographic clustering)
- Cognitive style (base-10 vs base-2)
- Protocol overlap (serial exploiter detection)
- Address overlap (definitive same/different attacker)

See examples: [examples/yei_summary.md](examples/yei_summary.md), [examples/abracadabra_summary.md](examples/abracadabra_summary.md)

## Output Standards

- All findings rated: CONFIRMED / HIGH / MEDIUM / LOW / SPECULATIVE
- Probabilities as ranges, not false precision
- Negative findings reported (what was NOT found)
- Delta vs existing public analysis explicitly stated
