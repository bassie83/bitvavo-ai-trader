# Sprint 5 - Integration Plan

## Doel

De Signal Engine, Risk Manager en Paper Trading Executor koppelen tot één gecontroleerde trading-flow.

---

## Huidige flow

/trade/{market}/paper

1. Genereert momentum-signaal.
2. Als signaal HOLD is, geen trade.
3. Bij BUY/SELL voert direct paper trade uit.

---

## Nieuwe flow

/trade/{market}/paper

1. Genereert combined signal.
2. Als signaal HOLD is, geen trade.
3. Bouwt RiskContext.
4. RiskManager beoordeelt de trade.
5. Als risk decision BLOCK is, geen trade.
6. Als risk decision ALLOW is, voert Paper Trading Executor uit.
7. Response toont signal, risk decision en trade-resultaat.

---

## RiskContext v1

Voor Sprint 5 gebruiken we:

- paper_trading
- has_open_position
- daily_loss
- max_daily_loss
- cooldown_active
- position_size
- max_position_size

---

## Bewuste vereenvoudigingen

In Sprint 5 gebruiken we tijdelijk vaste waarden voor:

- has_open_position = False
- daily_loss = 0.0
- cooldown_active = False

Deze worden later gekoppeld aan database/portfolio-logica.

---

## Definition of Done

- /trade/{market}/paper gebruikt combined signal.
- Risk Manager wordt altijd aangeroepen vóór een paper trade.
- HOLD voert geen trade uit.
- BLOCK voert geen trade uit.
- ALLOW kan paper trade uitvoeren.
- Docker start gezond.
- Pytest blijft groen.
- Git status is schoon.
