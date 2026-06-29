from app.risk.models import RiskDecision
from app.risk.rules import check_paper_trading


class RiskManager:
    """
    Centrale coördinator voor alle risicocontroles.
    """

    def evaluate(self, paper_trading: bool) -> RiskDecision:
        """
        Voert alle risicocontroles uit.
        """

        decision = check_paper_trading(paper_trading)

        if not decision.allowed:
            return decision

        return RiskDecision(
            allowed=True,
            reason="All risk checks passed.",
        )
