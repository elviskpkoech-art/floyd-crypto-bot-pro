
import pandas as pd


def ema(series: pd.Series, period: int = 20):
    """Calculate Exponential Moving Average."""
    return series.ewm(
        span=period,
        adjust=False
    ).mean()


def rsi(series: pd.Series, period: int = 14):
    """Calculate Relative Strength Index."""
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, float("nan"))

    result = 100 - (100 / (1 + rs))

    # Handle uninterrupted upward movement.
    result = result.mask(
        (avg_loss == 0) & (avg_gain > 0),
        100
    )

    return result


def atr(df: pd.DataFrame, period: int = 14):
    """Calculate Average True Range."""
    previous_close = df["close"].shift(1)

    true_ranges = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - previous_close).abs(),
            (df["low"] - previous_close).abs()
        ],
        axis=1
    )

    true_range = true_ranges.max(axis=1)

    return true_range.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()


def adx(df: pd.DataFrame, period: int = 14):
    """Calculate Average Directional Index."""
    high = df["high"]
    low = df["low"]

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where(
        (up_move > down_move) & (up_move > 0),
        0.0
    )

    minus_dm = down_move.where(
        (down_move > up_move) & (down_move > 0),
        0.0
    )

    previous_close = df["close"].shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs()
        ],
        axis=1
    ).max(axis=1)

    atr_value = tr.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    plus_di = 100 * (
        plus_dm.ewm(alpha=1 / period, adjust=False).mean()
        / atr_value.replace(0, float("nan"))
    )

    minus_di = 100 * (
        minus_dm.ewm(alpha=1 / period, adjust=False).mean()
        / atr_value.replace(0, float("nan"))
    )

    dx = (
        100 * (plus_di - minus_di).abs()
        / (plus_di + minus_di).replace(0, float("nan"))
    )

    return dx.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()
