# Case Study: Yei Finance Flash Loan Exploit ($2.4M) - v3 Integrated Operational Report

**Document class:** `integrated_operational_report`  
**Case ID:** `case_study_yei_finance_v1`  
**Primary narrative:** `reports/case_study_yei_finance_v1.md`  
**Re-analysis ledger:** `reports/case_study_yei_finance_v2.md`  
**Current-state artifact:** `artifacts/current_state_snapshot.json`  
**Operational packet:** `artifacts/lead_packets/case_study_yei_finance_v1.json`  
**Integrated dossier:** `artifacts/case_dossiers/case_study_yei_finance_v1.json`

---

## 1. Executive Decision Summary

Yei is no longer just a historical exploit case. It is an operationally actionable serial-exploiter case.

The central value of this case is not merely that the original exploit can be reconstructed. It is that the post-exploit path is unusually rich in structured pivots: multi-chain reuse, an Aave receipt-token hop, Railgun usage, Tornado Cash deposits, Chainflip conversion, CCTP transfers, Stargate transfers, and a KuCoin-funded secondary wallet. That combination creates a much stronger action surface than the average DeFi exploit report.

What v3 changes is the framing. v1 established the narrative and the new findings. v2 established that the rerun does not drift. The current-state and packet layers now make this case usable as an operating document for monitoring, disclosure preparation, and external engagement.

The core conclusion is:
- the v1 findings remain intact,
- the rerun supports them,
- the case has multiple still-meaningful action paths,
- and the KuCoin linkage remains the strongest practical escalation route.

---

## 2. What Still Stands from v1

The following conclusions remain the baseline position.

- The Yei exploit is best understood as part of a broader serial-exploiter pattern rather than an isolated one-off event.
- The attacker workflow after the exploit was not linear. It was fragmented on purpose across chains, bridges, wallets, and privacy tools.
- The Ethereum mainnet leg and the secondary wallet `0x3137...fC99` remain central to understanding the laundering path.
- The Aave hop is still one of the most important findings because it creates a deliberate chain-of-custody break while remaining fully explainable on-chain.
- The KuCoin 17 gas funding remains the strongest concrete KYC-oriented lead in the case.
- Railgun and Tornado Cash were both used, which means the attacker layered privacy rather than relying on a single concealment step.
- The case remains materially stronger than the public baseline because the public reporting did not reconstruct the same level of chain-by-chain operational detail.

In short: v1 remains analytically strong and still provides the correct skeleton for the case.

---

## 3. What v2 Re-analysis Confirmed

The rerun did not materially change the case.

Confirmed by `reports/case_study_yei_finance_v2.md`:
- aggregate score unchanged: `45.0 -> 45.0`
- event count unchanged: `11073 -> 11073`
- signal count unchanged
- temporal profile unchanged
- drift check pass condition satisfied: `drift_count = 0`

Operational meaning:
- the current extraction pipeline reproduces the same analytical baseline,
- the Yei case is not resting on a fragile one-off parse,
- and the high-value findings from v1 can be carried into action planning without reopening the entire case from scratch.

That is important because this case is now mature enough to support external-facing decisions.

---

## 4. Current-State Assessment

The live layer here is materially better than in Abracadabra.

Snapshot status:
- `freshness_status = live_checked`
- `last_checked_utc = 2026-03-18T11:37:06Z`
- monitored addresses: `8`
- live monitored addresses: `8`
- live attempts: `29`
- explorer hits: `5`
- activity rows: `5`

Coverage from the dossier:
- `address_state_coverage = 1000`
- `last_activity_coverage = 625`
- `last_outbound_coverage = 500`

Interpretation:
- the case has genuine live-operational support,
- not just historical reconstruction,
- and several key addresses are now in a state where future movement can be operationally interpreted rather than merely logged.

This does not mean every branch is fully resolved. It means the current-state layer is strong enough to support action prioritization.

---

## 5. Why This Case Is More Actionable Than Average

Yei is unusually strong because the attacker made several choices that create leverage instead of reducing it.

Those choices include:
- reusing the same EOA across multiple chains,
- introducing an Aave receipt-token hop that is still traceable,
- accepting KuCoin gas funding into the secondary wallet,
- splitting value into multiple bridge and privacy routes rather than disappearing in one move,
- and leaving residual assets and continued activity patterns that extend beyond the immediate exploit window.

That combination makes the case valuable in three ways:
- as a recovery-support case,
- as a serial-exploiter intelligence case,
- and as a premium monitoring / escalation case.

This is not just a strong report. It is a reusable operating case.

---

## 6. Primary Lead and Operational Priority

For Yei, the primary lead should remain the KuCoin-linked secondary wallet path.

Why this lead stands above the others:
- it is concrete,
- it connects to a real exchange touchpoint,
- it sits inside the most important laundering wallet after the Aave hop,
- and it creates a plausible legal-process route rather than a purely inferential identity hypothesis.

The current packet is directionally correct here.

Operationally, the right top line is:
- **Priority lead:** `kucoin_kyc_link`
- **Disclosure target:** KuCoin compliance / law-enforcement liaison
- **Why now:** the case has a stable rerun, structured evidence packaging, and enough current-state support to justify external escalation

Unlike Abracadabra, the lead packet does not fundamentally contradict the narrative baseline. It reinforces it.

---

## 7. Recommended Action Path

The next actions should stay narrow and economically justified.

1. **Preserve the KuCoin disclosure path as the top escalation route**  
Reason: it is the strongest identity-adjacent leverage point in the case.

2. **Maintain live monitoring on the secondary wallet and linked destination set**  
Reason: this is the fastest way to catch new off-ramp behavior or chain re-entry.

3. **Treat Base / BSC / Chainflip branches as structured sub-cases, not side notes**  
Reason: these are not decorative details; they are the main fragmentation layer in the laundering strategy.

4. **Keep Railgun and Tornado Cash as separate privacy layers in legal framing**  
Reason: collapsing them into one "privacy step" weakens the explanatory precision of the case.

5. **Use this case as a cross-incident comparison anchor**  
Reason: the serial-exploiter thesis is part of the case value, not just background context.

---

## 8. Recovery Posture

This case should be treated as a live-actionable but not fully recoverable case.

What can be stated with confidence:
- some value was irreversibly pushed into privacy routes,
- some branches remain traceable enough to support monitoring and structured follow-up,
- and the identity-adjacent lead is materially stronger than in many exploit cases.

What should not be overstated:
- that KuCoin linkage alone proves identity,
- that all downstream flows are equally actionable,
- or that full recovery is realistically implied by the current score saturation.

The right posture is:
- actionable,
- intelligence-rich,
- but still mixed in recoverability.

---

## 9. Evidence Chain and Reproducibility Position

Yei now has a stronger internal posture than the original v1 release.

Combined evidence posture now includes:
- the v1 narrative findings,
- the v2 no-drift rerun,
- immutable references from re-analysis,
- a current-state snapshot,
- a dossier with typed coverage,
- a lead packet with execution and recoverability framing.

This matters because the case can now support operational review without forcing the reader to traverse every artifact manually.

It also means the case is suitable for repeat internal use: monitoring, escalation prep, comparative analysis, and premium case packaging.

---

## 10. Confidence and Limits

High-confidence statements:
- the main laundering path is reconstructed at a high level,
- the secondary wallet is central and real,
- the KuCoin gas-funding event is material,
- the rerun did not break the case,
- and the case remains stronger than the public baseline.

Medium-confidence statements:
- the best external escalation path remains the KuCoin route,
- cross-incident clustering remains operationally useful,
- and future movement across linked chains can still improve the case.

Low-confidence / should-not-overclaim:
- direct human identity attribution,
- complete visibility across every downstream branch,
- or guaranteed recovery from privacy-routed funds.

Primary limitations carried forward:
- some downstream chain detail remains dependent on non-free or richer external data sources,
- privacy-layer exits are not fully knowable with current public tooling,
- and identity remains a legal-process question rather than a completed analytical fact.

---

## 11. Open Loops That Still Matter

Even with strong packaging, the case is not closed.

The open loops that still matter are:
- continued monitoring of the secondary wallet and linked destinations,
- deeper follow-up on Base and BSC branches when movement warrants it,
- preserving the KuCoin route as an active escalation option,
- and keeping the serial-exploiter comparison live rather than freezing the case as a single-incident artifact.

The mistake here would be to overwork the narrative while underworking the monitoring.

---

## 12. Immediate Next Action

**Immediate next action:** keep the KuCoin-linked secondary wallet path as the main operating lead, and treat any new movement from `0x3137...fC99` or its linked destinations as the trigger for disclosure escalation and branch-specific tracing.

That is the smartest next move because it matches the strongest remaining asymmetry in the case: the attacker created noise, but also left one of the clearest exchange-adjacent pivots available in the repo.

---

## 13. v3 Bottom Line

Yei v3 is not just a stronger report. It is a stronger operating case.

The original investigation still stands. The rerun supports it. The live layer is meaningful. The lead packet is directionally consistent with the case. And the best next move is not to reopen every analytical branch, but to preserve focus on the secondary wallet, the KuCoin route, and the fragmented but still-interpretable downstream paths.

That is the correct posture for now:
- stable baseline,
- strong rerun,
- real operational lead,
- mixed recoverability,
- and monitoring plus disclosure as the highest-value next step.
