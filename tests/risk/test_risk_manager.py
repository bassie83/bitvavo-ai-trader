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

def test_risk_manager_allows_when_daily_loss_below_limit():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
            daily_loss=50.0,
            max_daily_loss=100.0,
        )
    )

    assert result.allowed is True


def test_risk_manager_blocks_when_daily_loss_limit_reached():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
            daily_loss=100.0,
            max_daily_loss=100.0,
        )
    )

    assert result.allowed is False
    assert result.reason == "Maximum daily loss reached."


def test_risk_manager_allows_when_cooldown_inactive():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
            daily_loss=0.0,
            max_daily_loss=100.0,
            cooldown_active=False,
        )
    )

    assert result.allowed is True


def test_risk_manager_blocks_when_cooldown_active():
    manager = RiskManager()

    result = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
            daily_loss=0.0,
            max_daily_loss=100.0,
            cooldown_active=True,
        )
    )

    assert result.allowed is False
    assert result.reason == "Cooldown is active."
