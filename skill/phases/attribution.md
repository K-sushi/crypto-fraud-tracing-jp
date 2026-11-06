# Phase 5: OSINT Attribution

## On-Chain Identity Markers

1. **ENS names**: Check all addresses for forward/reverse ENS resolution
   - Etherscan V2: search address activity for ENS registrar interactions
   - Cross-reference ENS names with social media

2. **Contract function signatures**: Custom function names in attack contracts
   - Cultural references (e.g., `AtInverseBrah` = CT reference)
   - Language markers in error strings
   - Code style analysis (naming conventions, patterns)

3. **CEX deposit addresses**: If attacker sends to known CEX hot wallets
   - KYC disclosure path exists
   - Log exact: address, amount, tx hash, timestamp
   - Priority: this is the strongest attribution vector

4. **Token approvals**: What protocols has attacker used before?
   - Historical approval patterns reveal DeFi experience level
   - Cross-reference with known exploit patterns

## Off-Chain OSINT

1. **Social media**: Search attacker addresses on Twitter/X, Discord, forums
   - Direct mentions of the address
   - Claims of responsibility
   - Bounty negotiation messages

2. **GitHub/code**: Search for unique function signatures in public repos
   - Deployed bytecode similarity search (e.g., Dedaub, Heimdall)
   - Constructor arguments analysis

3. **Web3 identity**: Check Lens, Farcaster, ENS, Unstoppable Domains
   - Avatar/profile consistency across platforms

## Serial Exploiter Cross-Reference

For each known exploit in similar category:
1. Extract all attacker addresses
2. Check for ANY address overlap with current case
3. Check for behavioral similarity (CV, timezone, cognitive style)
4. 0 overlap = different attacker (CONFIRMED)
5. >0 overlap = same attacker or connected (investigate further)

## Output
- Identity markers found (rated by confidence)
- CEX touchpoints (if any) — highest priority for recovery
- Serial exploiter assessment
- Off-chain exposure level: ZERO / LOW / MEDIUM / HIGH
