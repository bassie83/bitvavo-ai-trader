from app.risk.models import RiskDecision, RiskContext
from app.risk.rules import (
    check_open_position,
    check_paper_trading,
)


class RiskManager:
    """
    Centrale coördinator voor alle risicocontroles.
    """

    def evaluate(self, context: RiskContext) -> RiskDecision:
        """
        Voert alle risicocontroles uit.
        """

        decision = check_paper_trading(context.paper_trading)
        if not decision.allowed:
            return decision

        decision = check_open_position(context.has_open_position)
        if not decision.allowed:
            return decision

        return RiskDecision(
            allowed=True,
            reason="All risk checks passed.",
        )
