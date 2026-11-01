
import ccxt
import pandas as pd


SUPPORTED_EXCHANGES = {
    "binance": ccxt.binance,
    "bybit": ccxt.bybit,
}


def create_exchange(exchange_name):
    """Create a public market-data exchange connection."""

    exchange_name = exchange_name.lower()

    if exchange_name not in SUPPORTED_EXCHANGES:
        raise ValueError(
            f"Unsupported exchange: {exchange_name}"
        )

    exchange_class = SUPPORTED_EXCHANGES[exchange_name]

    return exchange_class({
        "enableRateLimit": True,
        "timeout": 20000,
    })


def fetch_candles(
    exchange_name,
    symbol="BTC/USDT",
    timeframe="1h",
    limit=200
):
    """Fetch OHLCV candles from Binance or Bybit."""

    exchange = create_exchange(exchange_name)

    try:
        exchange.load_markets()

        if symbol not in exchange.markets:
            raise ValueError(
                f"{symbol} is not listed on {exchange_name}"
            )

        candles = exchange.fetch_ohlcv(
            symbol,
            timeframe=timeframe,
            limit=limit
        )

        if not candles:
            raise RuntimeError("Exchange returned no candle data")

        df = pd.DataFrame(
            candles,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            unit="ms",
            utc=True
        )

        numeric_columns = [
            "open", "high", "low", "close", "volume"
        ]

        df[numeric_columns] = df[numeric_columns].apply(
            pd.to_numeric,
            errors="coerce"
        )

        df = df.dropna().reset_index(drop=True)

        if len(df) < 60:
            raise RuntimeError(
                "Insufficient market data for analysis"
            )

        return df

    finally:
        exchange.close()
