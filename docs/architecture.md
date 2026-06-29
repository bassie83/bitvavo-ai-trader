# Project Atlas Architecture

## Doel

Project Atlas is een professionele AI-ondersteunde tradingbot.

Het systeem wordt eerst volledig gebouwd en getest in paper trading.

Live trading wordt pas als laatste toegevoegd.

---

## Kernprincipes

- Quality First
- Security First
- Paper Trading First
- Risk Manager beslist altijd
- Bitvavo API pas als laatste

---

## Hoofdmodules

Market Collector

↓

Database

↓

Indicator Engine

↓

Signal Engine

↓

Risk Manager

↓

Paper Trading Engine

↓

Portfolio Manager

↓

Telegram

↓

Dashboard

↓

AI Engine

---

## Moduleverantwoordelijkheden

### Market Collector
- Haalt marktdata op.
- Slaat data op.

### Indicator Engine
- SMA
- EMA
- RSI
- MACD
- Bollinger (later)
- ATR (later)

### Signal Engine
- BUY
- SELL
- HOLD

### Risk Manager
- Positiegrootte
- Dagverlies
- Cooldown
- Kill Switch

### Paper Trading Engine
- Simuleert trades.

### Portfolio Manager
- Houdt portefeuille en rendement bij.

### Dashboard
- Toont de status van de bot.

### AI Engine
- Analyseert nieuws en sentiment.

---

## Veiligheidsregel

Live trading blijft uitgeschakeld totdat alle voorgaande sprints succesvol zijn afgerond.
