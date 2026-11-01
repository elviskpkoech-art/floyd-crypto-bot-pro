
def calculate_position_size(
    balance,
    entry_price,
    stop_price,
    risk_fraction=0.005
):
    """
    Calculate position size based on account risk.

    Example:
    Balance: $1,000
    Risk: 0.5% = $5
    Entry: $100
    Stop: $95
    Quantity: 1 unit
    """

    if balance <= 0:
        raise ValueError("Balance must be positive")

    if entry_price <= 0:
        raise ValueError("Entry price must be positive")

    if stop_price <= 0:
        raise ValueError("Stop price must be positive")

    if not 0 < risk_fraction <= 0.01:
        raise ValueError("Risk must be above 0 and at most 1%")

    stop_distance = abs(entry_price - stop_price)

    if stop_distance <= 0:
        raise ValueError("Stop-loss distance must be positive")

    risk_amount = balance * risk_fraction

    quantity = risk_amount / stop_distance

    notional_value = quantity * entry_price

    return {
        "account_balance": balance,
        "risk_fraction": risk_fraction,
        "risk_amount": risk_amount,
        "entry_price": entry_price,
        "stop_price": stop_price,
        "stop_distance": stop_distance,
        "quantity": quantity,
        "notional_value": notional_value
    }


def daily_loss_limit_reached(
    starting_balance,
    current_balance,
    max_loss_fraction=0.02
):
    """Check whether the daily loss limit has been reached."""

    if starting_balance <= 0:
        raise ValueError("Starting balance must be positive")

    if not 0 < max_loss_fraction <= 0.05:
        raise ValueError("Daily loss limit must be above 0 and at most 5%")

    loss = max(0, starting_balance - current_balance)

    return loss >= starting_balance * max_loss_fraction


def trading_allowed(
    starting_balance,
    current_balance,
    max_loss_fraction=0.02
):
    """Return whether the daily risk limit permits trading."""

    return not daily_loss_limit_reached(
        starting_balance,
        current_balance,
        max_loss_fraction
    )


def calculate_atr_stop(
    entry_price,
    atr_value,
    direction="BUY",
    multiplier=2.0
):
    """Calculate a basic ATR-based stop-loss price."""

    if entry_price <= 0 or atr_value <= 0:
        raise ValueError("Price and ATR must be positive")

    if multiplier <= 0:
        raise ValueError("ATR multiplier must be positive")

    direction = direction.upper()

    if direction == "BUY":
        return entry_price - (atr_value * multiplier)

    if direction == "SELL":
        return entry_price + (atr_value * multiplier)

    raise ValueError("Direction must be BUY or SELL")
