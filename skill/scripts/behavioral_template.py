#!/usr/bin/env python3
"""Crypto Forensics — Generic Behavioral Analysis Template

Usage:
  1. Fill in CASE_NAME and TRANSACTIONS list below
  2. Run: python scripts/forensics_behavioral_template.py
  3. Integrate output into reports/case_study_*.md

Methodology (reverse-engineered from Yei Finance case study):
  - Phase 6.1: Bot vs Human (CV on inter-tx intervals)
  - Phase 6.2: Timezone estimation (sleep gap analysis)
  - Phase 6.3: Cognitive fingerprint (denomination preference)
  - Phase 6.4: Operation tempo (session structure)
  - Phase 6.5: Fermi estimation framework (claim validation)
  - Phase 6.6: Attacker generation estimation
"""
import sys, os, json, time, hashlib, urllib.request
from datetime import datetime, timezone, timedelta
from statistics import mean, stdev, median
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

# ============================================================
# CONFIGURATION — Fill these in per case
# ============================================================

CASE_NAME = "TEMPLATE"  # e.g., "YEI_FINANCE"

# Transaction data: list of (unix_timestamp_utc, label, value, denomination)
# value = numeric amount, denomination = "ETH", "USDC", etc.
# Collect from Etherscan/Arbiscan tx lists
TRANSACTIONS = [
    # (1739628227, "Deposit (Aave)", 596.0, "ETH"),
    # (1739628275, "Approve (WETH)", 0, ""),
    # (1739628335, "Shield (Railgun)", 594.51, "WETH"),
    # ... add all transactions chronologically
]

# Etherscan API V2 configuration (single key, all chains)
# source .env.forensics before running, or set ETHERSCAN_API_KEY env var
ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY", "")

# V2: unified base URL + chainid parameter. No separate explorer keys needed.
ETHERSCAN_V2_BASE = "https://api.etherscan.io/v2/api"

CHAIN_IDS = {
    # FREE tier (Etherscan V2)
    "ethereum": 1,
    "arbitrum": 42161,
    "polygon": 137,
    "sei": 1329,
    "linea": 59144,
    "scroll": 534352,
    "sonic": 146,
    "zksync": 324,
    # PAID tier (require $199/mo plan)
    "bsc": 56,
    "base": 8453,
    "optimism": 10,
    "avalanche": 43114,
}

# Addresses to analyze (for auto-collection)
ADDRESSES = {
    # "label": ("0xaddress", "chain"),
    # "primary_arb": ("0xcd2860fc4abf1748b8e4aebf35ddef2ab03e17c5", "arbitrum"),
}

# Claims to Fermi-test
CLAIMS = [
    # {"claim": "TC phishing loss is real", "amount_usd": 7764500, "total_proceeds_usd": 18500000},
]


# ============================================================
# AUTO-COLLECTION (if API key + addresses configured)
# ============================================================

def _init_evidence_log():
    """Initialize evidence directory and log file for current case."""
    evidence_dir = Path("evidence")
    evidence_dir.mkdir(exist_ok=True)
    return evidence_dir / "{}_api_log.jsonl".format(CASE_NAME.lower())


def _preserve_evidence(url_redacted, params_redacted, response_raw, status):
    """Hash and log API response for legal evidence preservation."""
    response_hash = hashlib.sha256(
        json.dumps(response_raw, sort_keys=True).encode()
    ).hexdigest()
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "epoch": time.time(),
        "url": url_redacted,
        "params": params_redacted,
        "response_sha256": response_hash,
        "response_status": status,
        "result_count": len(response_raw.get("result", [])) if isinstance(response_raw.get("result"), list) else 0,
    }
    log_path = _init_evidence_log()
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return response_hash


def explorer_api(chain, params):
    """Call Etherscan API V2 (unified endpoint, single key, all chains).
    Automatically preserves evidence hashes per SKILL.md Evidence Preservation Protocol."""
    chain_id = CHAIN_IDS.get(chain)
    if chain_id is None:
        print("    [Unknown chain: {}]".format(chain))
        return []
    params["chainid"] = chain_id
    if ETHERSCAN_API_KEY:
        params["apikey"] = ETHERSCAN_API_KEY
    qs = "&".join("{}={}".format(k, v) for k, v in params.items())
    url = "{}?{}".format(ETHERSCAN_V2_BASE, qs)
    # Redacted copies for evidence log (strip API key)
    params_redacted = {k: v for k, v in params.items() if k != "apikey"}
    url_redacted = url.replace(ETHERSCAN_API_KEY, "REDACTED") if ETHERSCAN_API_KEY else url
    for attempt in range(3):
        try:
            delay = 0.25 if ETHERSCAN_API_KEY else 5.5
            time.sleep(delay)
            r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(r, timeout=30) as resp:
                data = json.loads(resp.read())
            # Evidence preservation: hash every API response
            _preserve_evidence(url_redacted, params_redacted, data, data.get("status"))
            if data.get("status") == "1":
                return data.get("result", [])
            elif data.get("message") == "No transactions found":
                return []
            else:
                print("    [API: {} - {}]".format(
                    data.get("message", "?"), str(data.get("result", ""))[:80]))
                return []
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                print("    [API fail: {}]".format(str(e)[:80]))
    return []


def auto_collect_transactions():
    """Fetch tx lists from Etherscan APIs for all configured addresses."""
    if not ADDRESSES:
        return []
    if not ETHERSCAN_API_KEY:
        print("  [WARN] No ETHERSCAN_API_KEY set. Using manual TRANSACTIONS list.")
        return []

    all_tx = []
    for label, (addr, chain) in ADDRESSES.items():
        print("  Collecting {} ({} on {})...".format(label, addr[:12] + "..", chain))

        # Normal transactions
        txs = explorer_api(chain, {
            "module": "account", "action": "txlist",
            "address": addr, "startblock": "0", "endblock": "99999999",
            "sort": "asc",
        })
        for tx in txs:
            ts = int(tx.get("timeStamp", 0))
            func = tx.get("functionName", "").split("(")[0] or "transfer"
            value = int(tx.get("value", "0")) / 1e18
            direction = "OUT" if tx.get("from", "").lower() == addr.lower() else "IN"
            native_map = {"bsc": "BNB", "sei": "SEI", "polygon": "MATIC", "avalanche": "AVAX"}
            native = native_map.get(chain, "ETH")
            all_tx.append((ts, "{} {} ({})".format(direction, func, label), value, native))

        # Token transfers (with spam filter)
        tokens = explorer_api(chain, {
            "module": "account", "action": "tokentx",
            "address": addr, "startblock": "0", "endblock": "99999999",
            "sort": "asc",
        })
        # Known legitimate token symbols (add per case as needed)
        LEGIT_TOKENS = {"USDC", "USDT", "DAI", "WETH", "WBTC", "ETH", "BNB", "WBNB",
                        "aEthWETH", "USDC.e", "USDT.e", "DAI.e", "ODOS-LP"}
        SPAM_KEYWORDS = {"visit", "claim", "reward", "airdrop", ".xyz", ".io", ".com",
                         ".net", ".pro"}
        for tx in tokens:
            ts = int(tx.get("timeStamp", 0))
            sym = tx.get("tokenSymbol", "?")
            token_name = tx.get("tokenName", "").lower()
            decimals = int(tx.get("tokenDecimal", "18"))
            value = int(tx.get("value", "0")) / (10 ** decimals)
            # Skip airdrop spam and phishing tokens
            if any(kw in token_name for kw in SPAM_KEYWORDS):
                continue
            if any(kw in sym.lower() for kw in SPAM_KEYWORDS):
                continue
            # Skip tokens with homoglyph characters (phishing USDC/ETH)
            if sym not in LEGIT_TOKENS and not sym.isascii():
                continue
            direction = "OUT" if tx.get("from", "").lower() == addr.lower() else "IN"
            func = tx.get("functionName", "").split("(")[0] or "transfer"
            all_tx.append((ts, "{} {} {} ({})".format(direction, func, sym, label), value, sym))

    all_tx.sort(key=lambda x: x[0])
    print("  Collected {} total transactions".format(len(all_tx)))
    return all_tx


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def analyze_bot_vs_human(txs):
    """Phase 6.1: CV analysis on inter-transaction intervals."""
    print("=" * 70)
    print("1. BOT vs HUMAN DETERMINATION")
    print("=" * 70)

    if len(txs) < 3:
        print("  Insufficient transactions for analysis (need 3+, have {})".format(len(txs)))
        return

    # Calculate all consecutive intervals
    all_intervals = []
    for i in range(len(txs) - 1):
        gap = txs[i + 1][0] - txs[i][0]
        all_intervals.append((gap, txs[i][1], txs[i + 1][1]))

    # Intra-session intervals (< 1 hour)
    intra = [(g, a, b) for g, a, b in all_intervals if 0 < g < 3600]

    if len(intra) < 3:
        print("  Insufficient intra-session intervals (need 3+, have {})".format(len(intra)))
        return

    gaps = [g for g, _, _ in intra]
    cv = stdev(gaps) / mean(gaps) if mean(gaps) > 0 else 0

    print()
    print("  INTRA-SESSION INTERVALS (< 1 hour):")
    print("  Count: {}".format(len(gaps)))
    print("  Mean: {:.0f}s".format(mean(gaps)))
    print("  Median: {:.0f}s".format(median(gaps)))
    print("  Stdev: {:.0f}s".format(stdev(gaps)))
    print("  Min: {:.0f}s".format(min(gaps)))
    print("  Max: {:.0f}s".format(max(gaps)))
    print()
    print("  Coefficient of Variation: {:.3f}".format(cv))

    if cv < 0.3:
        print("  >>> LOW CV: Regular timing = LIKELY BOT")
    elif cv < 0.8:
        print("  >>> MODERATE CV: Semi-regular = HYBRID (script + human oversight)")
    else:
        print("  >>> HIGH CV: Irregular timing = LIKELY HUMAN")

    # Detail sub-minute intervals
    print()
    print("  Sub-minute intervals (bot signature if dominant):")
    sub_min = [(g, a, b) for g, a, b in intra if g < 60]
    for g, a, b in sorted(sub_min):
        a_short = a[:35].ljust(35)
        b_short = b[:35].ljust(35)
        print("    {:>5.0f}s | {} -> {}".format(g, a_short, b_short))

    print()
    print("  Long pauses within session (human thinking):")
    long_pause = [(g, a, b) for g, a, b in intra if g > 300]
    for g, a, b in sorted(long_pause, reverse=True):
        a_short = a[:35].ljust(35)
        b_short = b[:35].ljust(35)
        print("    {:>5.0f}s ({:>5.1f}m) | {} -> {}".format(g, g / 60, a_short, b_short))

    return cv


def analyze_timezone(txs):
    """Phase 6.2: Sleep gap analysis for timezone estimation."""
    print()
    print("=" * 70)
    print("2. TIMEZONE ESTIMATION (SLEEP GAP)")
    print("=" * 70)

    if len(txs) < 5:
        print("  Insufficient transactions")
        return

    # Hourly distribution
    hours = [datetime.fromtimestamp(ts, tz=timezone.utc).hour for ts, _, _, _ in txs]
    print()
    print("  HOURLY DISTRIBUTION (UTC):")
    for h in range(24):
        count = hours.count(h)
        bar = "#" * count
        marker = " <<<" if count == 0 else ""
        print("    {:02d}:00  {:>3d} {}{}".format(h, count, bar, marker))

    # Find sleep gaps (inter-session gaps > 4 hours)
    print()
    print("  INTER-SESSION GAPS (> 4 hours):")
    gaps = []
    for i in range(len(txs) - 1):
        gap_sec = txs[i + 1][0] - txs[i][0]
        if gap_sec > 4 * 3600:
            t1 = datetime.fromtimestamp(txs[i][0], tz=timezone.utc)
            t2 = datetime.fromtimestamp(txs[i + 1][0], tz=timezone.utc)
            gaps.append((gap_sec, t1, t2))
            print("    {} -> {} ({:.1f}h)".format(
                t1.strftime("%Y-%m-%d %H:%M"), t2.strftime("%Y-%m-%d %H:%M"),
                gap_sec / 3600))

    if not gaps:
        print("    No gaps > 4h found")
        return

    # Shortest gap = likely sleep duration
    min_gap = min(gaps, key=lambda x: x[0])
    print()
    print("  SHORTEST GAP: {:.1f}h ({} -> {})".format(
        min_gap[0] / 3600,
        min_gap[1].strftime("%H:%M UTC"),
        min_gap[2].strftime("%H:%M UTC")))

    sleep_start_utc = min_gap[1].hour
    wake_utc = min_gap[2].hour

    # Test timezone hypotheses
    print()
    print("  TIMEZONE HYPOTHESIS TABLE:")
    print("  {:>6} | {:>12} | {:>10} | {}".format("TZ", "Local Sleep", "Local Wake", "Assessment"))
    print("  " + "-" * 55)
    for offset in range(-5, 13):
        local_sleep = (sleep_start_utc + offset) % 24
        local_wake = (wake_utc + offset) % 24
        # Normal sleep: 20:00-00:00, Normal wake: 05:00-09:00
        sleep_ok = 20 <= local_sleep or local_sleep <= 1
        wake_ok = 5 <= local_wake <= 9
        if sleep_ok and wake_ok:
            assess = "<<< BEST FIT"
        elif (19 <= local_sleep or local_sleep <= 2) and (4 <= local_wake <= 10):
            assess = "POSSIBLE"
        else:
            assess = ""
        sign = "+" if offset >= 0 else ""
        print("  UTC{}{:<2d} | {:>8}:00   | {:>6}:00   | {}".format(
            sign, offset, local_sleep, local_wake, assess))


def analyze_cognitive_fingerprint(txs):
    """Phase 6.3: Denomination preference analysis."""
    print()
    print("=" * 70)
    print("3. COGNITIVE FINGERPRINT — DENOMINATION PREFERENCE")
    print("=" * 70)

    # Filter value-bearing transactions
    valued = [(ts, label, val, denom) for ts, label, val, denom in txs if val > 0]

    if not valued:
        print("  No value-bearing transactions")
        return

    round_numbers = {1, 2, 5, 10, 15, 20, 25, 30, 50, 100, 200, 250, 500, 1000,
                     2000, 5000, 10000, 25000, 50000, 100000}
    round_count = 0
    total_count = 0

    print()
    print("  VALUE-BEARING TRANSACTIONS:")
    denom_freq = {}
    for ts, label, val, denom in valued:
        is_round = val in round_numbers or int(val) in round_numbers
        marker = " <<< ROUND" if is_round else ""
        print("    {:>12,.2f} {} | {}{}".format(val, denom, label[:50], marker))
        if is_round:
            round_count += 1
        total_count += 1
        denom_freq.setdefault(int(val) if val == int(val) else val, 0)
        denom_freq[int(val) if val == int(val) else val] += 1

    ratio = round_count / total_count if total_count > 0 else 0
    print()
    print("  ROUND NUMBER RATIO: {}/{} = {:.0%}".format(round_count, total_count, ratio))

    if ratio > 0.7:
        print("  >>> HIGH round preference = MANUAL decision-making")
    elif ratio > 0.4:
        print("  >>> MODERATE round preference = mixed manual/automated")
    else:
        print("  >>> LOW round preference = likely optimized/automated")

    # Dominant denomination
    if denom_freq:
        dominant = max(denom_freq.items(), key=lambda x: x[1])
        print()
        print("  DOMINANT DENOMINATION: {} (used {} times)".format(dominant[0], dominant[1]))
        print("  = Cognitive anchor for this attacker")

    # Base-10 vs Base-2
    base2 = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}
    b2_count = sum(1 for _, _, v, _ in valued if int(v) in base2)
    b10_count = round_count
    if b2_count > b10_count:
        print("  BASE-2 DOMINANT: programmer cognitive style")
    elif b10_count > 0:
        print("  BASE-10 DOMINANT: non-programmer / finance cognitive style")


def analyze_operation_tempo(txs):
    """Phase 6.4: Session structure analysis."""
    print()
    print("=" * 70)
    print("4. OPERATION TEMPO — SESSION STRUCTURE")
    print("=" * 70)

    if len(txs) < 2:
        print("  Insufficient transactions")
        return

    # Group into sessions (gap > 2h = new session)
    sessions = []
    current_session = [txs[0]]
    for i in range(1, len(txs)):
        gap = txs[i][0] - txs[i - 1][0]
        if gap > 7200:  # 2 hours
            sessions.append(current_session)
            current_session = [txs[i]]
        else:
            current_session.append(txs[i])
    sessions.append(current_session)

    print()
    print("  {} SESSIONS IDENTIFIED:".format(len(sessions)))
    print()

    for i, session in enumerate(sessions):
        t_start = datetime.fromtimestamp(session[0][0], tz=timezone.utc)
        t_end = datetime.fromtimestamp(session[-1][0], tz=timezone.utc)
        duration = (session[-1][0] - session[0][0]) / 60  # minutes
        n = len(session)

        # Classify session type
        if n >= 3 and duration < 20:
            stype = "BURST"
        elif n == 1:
            stype = "SINGLE"
        elif duration > 60:
            stype = "DELIBERATE"
        else:
            stype = "MIXED"

        ops = set()
        for _, label, _, _ in session:
            # Extract operation type from label
            for keyword in ["Deposit", "Withdraw", "Approve", "Shield", "Transfer",
                            "Swap", "Send", "Create Order", "CCTP", "Bridge"]:
                if keyword.lower() in label.lower():
                    ops.add(keyword)

        print("  [{}] {} - {} | {} tx | {:.0f}min | {} | {}".format(
            i, t_start.strftime("%Y-%m-%d %H:%M"),
            t_end.strftime("%H:%M") if t_start.date() == t_end.date() else t_end.strftime("%Y-%m-%d %H:%M"),
            n, duration, stype, ", ".join(sorted(ops)) or "misc"))

    # Analyze session timing patterns
    print()
    print("  SESSION TIMING PATTERNS:")
    start_hours = [datetime.fromtimestamp(s[0][0], tz=timezone.utc).hour for s in sessions]
    morning = sum(1 for h in start_hours if 3 <= h <= 6)
    midday = sum(1 for h in start_hours if 10 <= h <= 14)
    evening = sum(1 for h in start_hours if 15 <= h <= 19)
    night = sum(1 for h in start_hours if h >= 20 or h <= 2)
    print("    Early morning (03-06 UTC): {} sessions".format(morning))
    print("    Midday (10-14 UTC): {} sessions".format(midday))
    print("    Afternoon/evening (15-19 UTC): {} sessions".format(evening))
    print("    Night (20-02 UTC): {} sessions".format(night))


def analyze_fermi(claims):
    """Phase 6.5: Fermi estimation for claim validation."""
    print()
    print("=" * 70)
    print("5. FERMI ESTIMATION — CLAIM VALIDATION")
    print("=" * 70)

    if not claims:
        print("  No claims configured for Fermi testing")
        return

    for claim_data in claims:
        claim = claim_data["claim"]
        amount = claim_data["amount_usd"]
        total = claim_data["total_proceeds_usd"]
        ratio = amount / total if total > 0 else 0

        print()
        print("  CLAIM: {}".format(claim))
        print("  Amount: ${:,.0f}".format(amount))
        print("  Total proceeds: ${:,.0f}".format(total))
        print("  Ratio: {:.1%}".format(ratio))
        print()
        print("  IF REAL:")
        if ratio > 0.3:
            print("    - {:.0%} loss is devastating for solo operator".format(ratio))
            print("    - Consistent with careless/impulsive behavior pattern?")
        else:
            print("    - {:.0%} loss is significant but survivable".format(ratio))
        print("    - Does subsequent behavior match 'loss' (scraping small amounts)?")
        print("    - Is emotional response (e.g., on-chain message) authentic?")
        print()
        print("  IF STAGED:")
        if ratio > 0.2:
            print("    - {:.0%} is LARGE for rational deception (typical max: 5-10%)".format(ratio))
            print("    - Sacrifice too high unless strategic purpose is extreme")
        else:
            print("    - {:.0%} is within plausible deception range".format(ratio))
        print("    - Does attacker control both sides?")
        print("    - Strategic purpose? (avoid return demands, confuse investigators?)")
        print()

        # Auto-assessment
        if ratio > 0.3:
            print("  AUTO-ASSESSMENT: PROBABLY REAL (ratio > 30% = too costly to fake)")
        elif ratio > 0.15:
            print("  AUTO-ASSESSMENT: UNCERTAIN (ratio 15-30% = could go either way)")
        else:
            print("  AUTO-ASSESSMENT: POSSIBLY STAGED (ratio < 15% = affordable deception)")


def analyze_attacker_generation(protocols_used):
    """Phase 6.6: DeFi biography from protocol usage."""
    print()
    print("=" * 70)
    print("6. ATTACKER GENERATION — DeFi BIOGRAPHY")
    print("=" * 70)

    # Protocol launch dates for reference
    PROTOCOL_DATES = {
        "Tornado Cash": 2019,
        "Uniswap V2": 2020,
        "Aave V2": 2020,
        "Uniswap V3": 2021,
        "Aave V3": 2022,
        "Railgun": 2022,
        "CoW Protocol": 2022,
        "Chainflip": 2024,
        "Circle CCTP": 2023,
        "Stargate V2": 2024,
        "LayerZero V2": 2024,
        "1inch": 2020,
        "Odos": 2023,
    }

    if not protocols_used:
        print("  No protocol usage data configured")
        print("  Add protocols to PROTOCOLS_USED list")
        return

    print()
    print("  PROTOCOL TIMELINE:")
    for proto in sorted(protocols_used, key=lambda p: PROTOCOL_DATES.get(p, 9999)):
        year = PROTOCOL_DATES.get(proto, "?")
        print("    {} ({})".format(proto, year))

    years = [PROTOCOL_DATES[p] for p in protocols_used if p in PROTOCOL_DATES]
    if years:
        earliest = min(years)
        latest = max(years)
        print()
        print("  EARLIEST PROTOCOL: {} ({})".format(
            [p for p in protocols_used if PROTOCOL_DATES.get(p) == earliest][0], earliest))
        print("  LATEST PROTOCOL: {} ({})".format(
            [p for p in protocols_used if PROTOCOL_DATES.get(p) == latest][0], latest))
        print("  DeFi ACTIVE SINCE: at least {}".format(earliest))
        print("  KEEPS CURRENT: {}".format("YES" if latest >= 2024 else "NO"))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEEP BEHAVIORAL PROFILING — {}".format(CASE_NAME))
    print("The human behind the transactions")
    print("=" * 70)
    print("Time: {}".format(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")))

    # Try auto-collection first, fall back to manual
    txs = auto_collect_transactions()
    if not txs:
        txs = TRANSACTIONS

    if not txs:
        print()
        print("ERROR: No transaction data.")
        print("Either:")
        print("  1. Fill TRANSACTIONS list manually, or")
        print("  2. Set ETHERSCAN_API_KEY + ADDRESSES for auto-collection")
        print()
        print("Example manual entry:")
        print('  TRANSACTIONS = [')
        print('      (1739628227, "Deposit (Aave)", 596.0, "ETH"),')
        print('      (1739628275, "Approve (WETH)", 0, ""),')
        print('      (1739628335, "Shield (Railgun)", 594.51, "WETH"),')
        print('  ]')
        sys.exit(1)

    print()
    print("Analyzing {} transactions...".format(len(txs)))

    # Phase 6.1: Bot vs Human
    cv = analyze_bot_vs_human(txs)

    # Phase 6.2: Timezone
    analyze_timezone(txs)

    # Phase 6.3: Cognitive fingerprint
    analyze_cognitive_fingerprint(txs)

    # Phase 6.4: Operation tempo
    analyze_operation_tempo(txs)

    # Phase 6.5: Fermi estimation
    analyze_fermi(CLAIMS)

    # Phase 6.6: Attacker generation (configure per case)
    # Uncomment and fill in protocols used by the attacker:
    # analyze_attacker_generation([
    #     "Tornado Cash", "Railgun", "Chainflip", "CoW Protocol",
    #     "Aave V3", "Circle CCTP", "Stargate V2", "Odos",
    # ])

    print()
    print("=" * 70)
    print("PROFILING COMPLETE")
    print("=" * 70)

    # Evidence preservation summary
    log_path = _init_evidence_log()
    if log_path.exists():
        with open(log_path) as f:
            entries = f.readlines()
        print()
        print("EVIDENCE PRESERVATION:")
        print("  Log: {}".format(log_path))
        print("  API calls recorded: {}".format(len(entries)))
        if entries:
            last = json.loads(entries[-1])
            print("  Last hash: {}...".format(last["response_sha256"][:16]))
        print("  All responses SHA256-hashed for legal admissibility")

    print()
    print("Next: Integrate findings into reports/case_study_{}.md".format(CASE_NAME.lower()))
