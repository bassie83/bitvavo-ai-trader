from app.risk.models import RiskDecision, RiskContext
from app.risk.rules import (
    check_daily_loss,
    check_open_position,
    check_paper_trading,
    check_cooldown,
    check_position_size,
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

        decision = check_daily_loss(
            context.daily_loss,
            context.max_daily_loss,
        )
        if not decision.allowed:
            return decision

        decision = check_cooldown(context.cooldown_active)
        if not decision.allowed:
            return decision

        decision = check_position_size(
            context.position_size,
            context.max_position_size,
        )
        if not decision.allowed:
            return decision

        return RiskDecision(
            allowed=True,
            reason="All risk checks passed.",
        )
