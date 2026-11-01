
import json
from pathlib import Path
from datetime import datetime, timezone


LEDGER = Path("data/paper_signals.jsonl")


def record_signal(exchange, symbol, timeframe, result):
    """Save a trading signal to the paper-trading ledger."""

    LEDGER.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "id": datetime.now(timezone.utc).isoformat(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "exchange": exchange,
        "symbol": symbol,
        "timeframe": timeframe,
        "signal": result.get("signal", "WAIT"),
        "reason": result.get("reason", ""),
        "price": result.get("price"),
        "indicators": {
            "ema20": result.get("ema20"),
            "ema50": result.get("ema50"),
            "rsi": result.get("rsi"),
            "atr": result.get("atr"),
            "adx": result.get("adx")
        },
        "mode": "PAPER_ONLY",
        "order_placed": False
    }

    with LEDGER.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

    return record


def get_signal_history(limit=50):
    """Retrieve the latest paper-trading signals."""

    if not LEDGER.exists():
        return []

    if limit <= 0:
        raise ValueError("Limit must be positive")

    with LEDGER.open("r", encoding="utf-8") as file:
        records = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    return records[-limit:]


def count_signals():
    """Count recorded signals by type."""

    history = get_signal_history(limit=100000)

    counts = {
        "BUY": 0,
        "SELL": 0,
        "WAIT": 0
    }

    for record in history:
        signal = record.get("signal")

        if signal in counts:
            counts[signal] += 1

    return counts
