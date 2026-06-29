# Risk Manager Design

## Project Atlas

Version 0.2.0 (Design)

---

# Doel

De Risk Manager bepaalt of een trade uitgevoerd mag worden.

De Signal Engine mag nooit zelfstandig een trade uitvoeren.

Elke BUY- of SELL-beslissing wordt eerst beoordeeld door de Risk Manager.

---

# Filosofie

Een gemiste kans is acceptabel.

Een onnodig risico is dat niet.

De Risk Manager is daarom altijd conservatief.

---

# Beslisvolgorde

## Stap 1

Is Paper Trading actief?

JA → verder

NEE → alleen Live Trading als expliciet toegestaan.

---

## Stap 2

Is de marktdata geldig?

Controle:

- recente prijsdata
- voldoende historie
- geen ontbrekende waarden

---

## Stap 3

Bestaat er al een open positie?

Zo ja:

- geen dubbele positie openen

---

## Stap 4

Maximale positiegrootte

Controle:

- maximaal toegestaan bedrag

---

## Stap 5

Dagverlies

Controle:

Is maximaal dagverlies bereikt?

JA

Trade blokkeren.

---

## Stap 6

Cooldown

Na verlies:

geen nieuwe trade gedurende ingestelde periode.

---

## Stap 7

Kill Switch

Trade blokkeren bij:

- database fout
- exchange fout
- ontbrekende marktdata
- interne fout

---

## Stap 8

Trade toestaan

Alle controles succesvol?

Dan mag de Paper Trading Engine de trade uitvoeren.

---

# Logging

Elke beslissing wordt opgeslagen.

Voorbeelden:

ALLOW

BLOCK

COOLDOWN

MAX LOSS

INVALID DATA

OPEN POSITION

---

# Telegram

Belangrijke blokkades worden gemeld.

Bijvoorbeeld:

Dagverlies bereikt.

Trading gepauzeerd.

---

# Toekomst

Later toevoegen:

- volatiliteitscontrole
- ATR-filter
- spreadcontrole
- volumecontrole
- AI-risicoscore

---

# Ontwerpregel

De Risk Manager kent geen indicatoren.

Hij kijkt uitsluitend naar risico.

Indicatoren bepalen het signaal.

De Risk Manager bepaalt of dat signaal uitgevoerd mag worden.
