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
