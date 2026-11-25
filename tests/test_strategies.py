
from app.strategies.production_strategy import (
    YieldStrategy,
    WastageStrategy
)


def test_yield_strategy():
    strategy = YieldStrategy()

    result = strategy.calculate(800, 710, 90)

    assert result == 88.75


def test_wastage_strategy():
    strategy = WastageStrategy()

    result = strategy.calculate(800, 710, 90)

    assert result == 11.25


def test_yield_strategy_with_zero_input():
    strategy = YieldStrategy()

    result = strategy.calculate(0, 0, 0)

    assert result == 0


def test_wastage_strategy_with_zero_input():
    strategy = WastageStrategy()

    result = strategy.calculate(0, 0, 0)

    assert result == 0
