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

def check_daily_loss(
    daily_loss: float,
    max_daily_loss: float,
) -> RiskDecision:
    """
    Blokkeert nieuwe trades als de maximale dagverlieslimiet is bereikt.
    """

    if daily_loss >= max_daily_loss:
        return RiskDecision(
            allowed=False,
            reason="Maximum daily loss reached.",
        )

    return RiskDecision(
        allowed=True,
        reason="Daily loss within limit.",
    )


def check_cooldown(cooldown_active: bool) -> RiskDecision:
    """
    Blokkeert nieuwe trades als cooldown actief is.
    """

    if cooldown_active:
        return RiskDecision(
            allowed=False,
            reason="Cooldown is active.",
        )

    return RiskDecision(
        allowed=True,
        reason="Cooldown inactive.",
    )
