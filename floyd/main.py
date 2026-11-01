
import logging

from floyd.config import settings
from floyd.market_data import fetch_candles
from floyd.strategies import generate_signal
from floyd.paper import record_signal


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("FLOYD")


def run():
    """Run one complete paper-analysis cycle."""

    print("\n===================================")
    print("       FLOYD CRYPTO BOT PRO")
    print("===================================")

    print("MODE: PAPER TRADING")
    print("EXCHANGE:", settings.exchange.upper())
    print("PAIR:", settings.symbol)
    print("TIMEFRAME:", settings.timeframe)

    try:
        logger.info("Connecting to public market data...")

        candles = fetch_candles(
            exchange_name=settings.exchange,
            symbol=settings.symbol,
            timeframe=settings.timeframe,
            limit=settings.candle_limit
        )

        logger.info("Market data received: %s candles", len(candles))

        result = generate_signal(candles)

        print("\n========== MARKET ANALYSIS ==========")

        for key, value in result.items():
            print(f"{key.upper()}: {value}")

        record_signal(
            exchange=settings.exchange,
            symbol=settings.symbol,
            timeframe=settings.timeframe,
            result=result
        )

        print("\n========== PAPER TRADING ============")
        print("Signal recorded successfully.")
        print("REAL ORDERS: DISABLED")
        print("EXCHANGE FUNDS: NOT USED")

    except Exception as error:
        logger.exception("FLOYD encountered an error: %s", error)
        print("\nAnalysis failed. Check the error log.")


if __name__ == "__main__":
    run()
