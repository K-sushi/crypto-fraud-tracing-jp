# Phase 6: Behavioral Profiling

The human behind the transactions. Run `behavioral_template.py` or analyze manually.

## 6.1 Bot vs Human (CV Analysis)

**Coefficient of Variation** = stdev / mean of inter-transaction intervals (intra-session, <1h gaps)

| CV Range | Classification |
|:---------|:--------------|
| < 0.3 | BOT (regular timing) |
| 0.3 - 0.8 | HYBRID (script + human oversight) |
| > 0.8 | HUMAN (irregular, decision-making pauses) |

Per-chain CV can reveal different operators on different chains.
Sub-minute intervals indicate scripted segments within human sessions.

## 6.2 Timezone Estimation (Sleep Gap)

1. Plot hourly transaction distribution (UTC)
2. Find inter-session gaps > 4 hours
3. Shortest gap = likely sleep duration
4. Test timezone hypotheses: UTC-5 through UTC+12
5. Normal sleep: 20:00-00:00 local, wake: 05:00-09:00 local
6. Best fit = where sleep/wake align with gap boundaries

## 6.3 Cognitive Fingerprint (Denomination Preference)

- **Base-10 dominant** (100, 500, 1000): Finance/trader cognitive style
- **Base-2 dominant** (128, 256, 512, 1024): Programmer cognitive style
- **Round number ratio**: >70% = manual decision-making, <30% = automated
- **Dominant denomination**: Cognitive anchor (e.g., always 500 ETH batches)

## 6.4 Operation Tempo (Session Structure)

Group transactions into sessions (>2h gap = new session):
- **BURST**: 3+ tx in <20 min (scripted execution)
- **DELIBERATE**: >60 min session (careful operation)
- **SINGLE**: isolated transaction
- Analyze session timing patterns for work schedule inference

## 6.5 Fermi Estimation (Claim Validation)

For claims like "lost funds to phishing" or "white-hat operation":
- Claimed loss / total proceeds ratio
- >30% sacrifice = probably real (too costly to fake)
- <15% sacrifice = possibly staged (affordable deception)
- Does subsequent behavior match the claim?

## 6.6 Attacker Generation (DeFi Biography)

Map protocols used to their launch dates:
- Earliest protocol = minimum DeFi active-since date
- Latest protocol = stays current with ecosystem
- Protocol selection reveals sophistication and era

## Output
- CV value + classification (per-chain if multi-chain)
- Timezone estimate with confidence range
- Cognitive style assessment
- Operation tempo characterization
- All claims Fermi-tested
