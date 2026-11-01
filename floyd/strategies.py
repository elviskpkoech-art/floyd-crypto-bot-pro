
from floyd.indicators import ema, rsi, atr, adx


def generate_signal(df):
    """
    Analyze market data and generate a trading signal.

    Signals are informational only.
    No real orders are placed.
    """

    if len(df) < 60:
        return {
            "signal": "WAIT",
            "reason": "Insufficient market history"
        }

    data = df.copy()

    data["ema20"] = ema(data["close"], 20)
    data["ema50"] = ema(data["close"], 50)
    data["rsi"] = rsi(data["close"], 14)
    data["atr"] = atr(data, 14)
    data["adx"] = adx(data, 14)

    latest = data.iloc[-1]

    required = [
        "ema20",
        "ema50",
        "rsi",
        "atr",
        "adx"
    ]

    if latest[required].isna().any():
        return {
            "signal": "WAIT",
            "reason": "Indicators are not ready"
        }

    price = float(latest["close"])
    ema20 = float(latest["ema20"])
    ema50 = float(latest["ema50"])
    rsi_value = float(latest["rsi"])
    atr_value = float(latest["atr"])
    adx_value = float(latest["adx"])

    signal = "WAIT"
    reason = "No complete trading setup"

    # Bullish trend with positive momentum.
    if (
        ema20 > ema50
        and price > ema20
        and 50 < rsi_value < 70
        and adx_value >= 20
    ):
        signal = "BUY"
        reason = "Bullish trend and momentum confirmed"

    # Bearish trend with negative momentum.
    elif (
        ema20 < ema50
        and price < ema20
        and 30 < rsi_value < 50
        and adx_value >= 20
    ):
        signal = "SELL"
        reason = "Bearish trend and momentum confirmed"

    return {
        "signal": signal,
        "reason": reason,
        "price": price,
        "ema20": ema20,
        "ema50": ema50,
        "rsi": rsi_value,
        "atr": atr_value,
        "adx": adx_value,
        "timestamp": str(latest["timestamp"])
    }
