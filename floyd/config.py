
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    exchange: str = os.getenv("EXCHANGE", "binance").lower()
    symbol: str = os.getenv("SYMBOL", "BTC/USDT")
    timeframe: str = os.getenv("TIMEFRAME", "1h")
    candle_limit: int = int(os.getenv("CANDLE_LIMIT", "200"))

    # Risk controls
    risk_per_trade: float = float(
        os.getenv("RISK_PER_TRADE", "0.005")
    )
    max_daily_loss: float = float(
        os.getenv("MAX_DAILY_LOSS", "0.02")
    )

    # Paper trading only
    paper_balance: float = float(
        os.getenv("PAPER_BALANCE", "1000")
    )

settings = Settings()

if settings.exchange not in ("binance", "bybit"):
    raise ValueError("Exchange must be binance or bybit")

if not 0 < settings.risk_per_trade <= 0.01:
    raise ValueError("Risk per trade must be above 0 and at most 1%")

if not 0 < settings.max_daily_loss <= 0.05:
    raise ValueError("Daily loss limit must be above 0 and at most 5%")

if settings.candle_limit < 60:
    raise ValueError("Candle limit must be at least 60")
