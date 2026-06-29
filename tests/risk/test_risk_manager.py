from app.risk.manager import RiskManager
from app.risk.models import RiskContext


def test_risk_manager_allows_trade():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
        )
    )

    assert result.allowed is True


def test_risk_manager_blocks_open_position():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=True,
        )
    )

    assert result.allowed is False
    assert result.reason == "An open position already exists."


def test_risk_manager_blocks_when_paper_trading_disabled():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=False,
            has_open_position=False,
        )
    )

    assert result.allowed is False
    assert result.reason == "Paper trading is disabled."
