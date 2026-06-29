from dataclasses import dataclass


@dataclass
class RiskDecision:
    """
    Resultaat van een risicoanalyse.
    """

    allowed: bool
    reason: str
