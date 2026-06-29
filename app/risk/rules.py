from app.risk.models import RiskDecision


def check_paper_trading(enabled: bool) -> RiskDecision:
    """
    Controleert of paper trading is ingeschakeld.
    """

    if enabled:
        return RiskDecision(
            allowed=True,
            reason="Paper trading is enabled.",
        )

    return RiskDecision(
        allowed=False,
        reason="Paper trading is disabled.",
    )


def check_open_position(has_open_position: bool) -> RiskDecision:
    """
    Blokkeert een nieuwe trade als er al een open positie bestaat.
    """

    if has_open_position:
        return RiskDecision(
            allowed=False,
            reason="An open position already exists.",
        )

    return RiskDecision(
        allowed=True,
        reason="No open position.",
    )
