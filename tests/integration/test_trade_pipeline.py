from app.risk.manager import RiskManager
from app.risk.models import RiskContext


def test_trade_pipeline_allows_when_risk_passes():
    manager = RiskManager()

    decision = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=False,
            daily_loss=0.0,
            max_daily_loss=100.0,
            cooldown_active=False,
            position_size=50.0,
            max_position_size=50.0,
        )
    )

    assert decision.allowed is True
    assert decision.reason == "All risk checks passed."


def test_trade_pipeline_blocks_when_risk_fails():
    manager = RiskManager()

    decision = manager.evaluate(
        RiskContext(
            paper_trading=True,
            has_open_position=True,
            daily_loss=0.0,
            max_daily_loss=100.0,
            cooldown_active=False,
            position_size=50.0,
            max_position_size=50.0,
        )
    )

    assert decision.allowed is False
    assert decision.reason == "An open position already exists."
