# Phase 1-4: Fund Tracing

## Phase 1: Initial Mapping

Starting from the attacker address:

1. **Funding source**: Where did gas/initial capital come from?
   - TC deposit? (check 0.1/1/10/100 ETH patterns)
   - CEX withdrawal? (hot wallet identification)
   - Fresh wallet from faucet?

2. **First-hop graph**: Map immediate transfers OUT
   - Etherscan V2: `module=account&action=txlist`
   - Token transfers: `module=account&action=tokentx`
   - Internal transactions: `module=account&action=txlistinternal`

3. **Contract identification**: What contracts did attacker deploy?
   - Check `contractCreator` via Etherscan
   - Decompile/analyze attack contract functions

## Phase 2: Cross-Chain Tracing

Track funds across chains:

| Bridge | Detection Method |
|:-------|:----------------|
| Stargate/LayerZero | Look for `sgReceive`, `lzReceive` events |
| Across V3 | `FilledRelay` events on destination |
| Circle CCTP | `MessageReceived` + USDC mint on destination |
| Native bridges | L1→L2 deposit/withdrawal messages |

For each bridge transfer:
- Source chain + tx hash
- Destination chain + tx hash
- Amount + token
- Timestamp correlation

## Phase 3: Privacy Tool Analysis

### Tornado Cash
- Deposit denominations: 0.1, 1, 10, 100 ETH
- Deposit tx → note → withdrawal tx
- Timing pattern: gap between deposit and withdrawal
- Multiple deposits = aggregation pattern

### Railgun
- Shield/unshield events
- UTXO-based, harder to trace
- Look for shield amounts matching exploit proceeds

### Chainflip
- Cross-chain swap (e.g., ETH→BTC)
- Channel events on Chainflip State Chain

## Phase 4: TC Deanonymization Techniques

Correlation methods (passive, read-only):
1. **Amount matching**: Deposit amount ≈ withdrawal amount (minus fee)
2. **Timing**: Deposits close to exploit, withdrawals with pattern
3. **Gas price fingerprinting**: Similar gas settings across wallets
4. **Multi-denomination**: 100+10+1 ETH deposits → single recipient withdrawing same pattern
5. **Linked withdrawals**: Multiple withdrawals to same destination within timeframe

**IMPORTANT**: TC deanon is probabilistic. Rate all correlations with confidence levels.

## Output
- Fund flow graph (text-based or mermaid diagram)
- Amount triage: % laundered, % potentially recoverable, % unknown
- CEX touchpoints identified (for KYC disclosure path)
