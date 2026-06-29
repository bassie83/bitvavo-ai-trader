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
