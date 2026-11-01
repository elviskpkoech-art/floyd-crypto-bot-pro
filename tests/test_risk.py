
import pytest

from floyd.risk import (
    calculate_position_size,
    daily_loss_limit_reached,
    trading_allowed,
    calculate_atr_stop
)


def test_position_size():
    result = calculate_position_size(
        balance=1000,
        entry_price=100,
        stop_price=95,
        risk_fraction=0.005
    )

    assert result["risk_amount"] == pytest.approx(5)
    assert result["quantity"] == pytest.approx(1)
    assert result["notional_value"] == pytest.approx(100)


def test_daily_loss_limit_reached():
    assert daily_loss_limit_reached(
        starting_balance=1000,
        current_balance=980,
        max_loss_fraction=0.02
    )


def test_daily_loss_limit_not_reached():
    assert not daily_loss_limit_reached(
        starting_balance=1000,
        current_balance=990,
        max_loss_fraction=0.02
    )


def test_trading_blocked_after_daily_loss():
    assert not trading_allowed(1000, 980, 0.02)


def test_atr_buy_stop():
    stop = calculate_atr_stop(
        entry_price=100,
        atr_value=2,
        direction="BUY",
        multiplier=2
    )

    assert stop == pytest.approx(96)


def test_atr_sell_stop():
    stop = calculate_atr_stop(
        entry_price=100,
        atr_value=2,
        direction="SELL",
        multiplier=2
    )

    assert stop == pytest.approx(104)


def test_reject_zero_stop_distance():
    with pytest.raises(ValueError):
        calculate_position_size(
            balance=1000,
            entry_price=100,
            stop_price=100
        )


def test_reject_risk_above_one_percent():
    with pytest.raises(ValueError):
        calculate_position_size(
            balance=1000,
            entry_price=100,
            stop_price=95,
            risk_fraction=0.02
        )
