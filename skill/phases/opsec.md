# Phase 0: OPSEC

Before starting any investigation:

## Workspace Isolation
1. Dedicated browser profile (no personal accounts logged in)
2. VPN active (jurisdiction-appropriate)
3. No interaction with attacker addresses from personal wallets
4. Evidence directory initialized: `mkdir -p evidence/`

## API Key Safety
- `.env.forensics` must NOT be committed to any repo
- API key appears in NO log files (redacted before logging)
- Evidence JSONL contains hashes only, never raw API keys

## Operational Notes
- Never ping/interact with attacker contracts (read-only analysis)
- Block explorer queries are passive reads, not interactions
- Screenshot preservation: browser screenshots with timestamps for volatile data
- Archive.org/Wayback snapshots of relevant social profiles

## Output
Confirmation that workspace is clean and evidence directory is ready.
