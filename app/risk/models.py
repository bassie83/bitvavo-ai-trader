from dataclasses import dataclass


@dataclass
class RiskDecision:
    """
    Resultaat van een risicoanalyse.
    """

    allowed: bool
    reason: str


@dataclass
class RiskContext:
    """
    Context die de Risk Manager nodig heeft om een beslissing te nemen.
    """

    paper_trading: bool
    has_open_position: bool = False
    daily_loss: float = 0.0
    max_daily_loss: float = 100.0
    cooldown_active: bool = False
    position_size: float = 0.0
    max_position_size: float = 1000.0
