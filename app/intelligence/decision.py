def generate_market_insight(fear_greed: dict, has_open_position: bool) -> dict:
    value = fear_greed["value"]
    classification = fear_greed["classification"]

    if value <= 25:
        sentiment = "Extreme fear"
        bias = "Potential opportunity"
        message = (
            "De markt staat in Extreme Fear. Dit kan kansen geven, "
            "maar Atlas wacht op technische bevestiging voordat er gekocht wordt."
        )
    elif value <= 45:
        sentiment = "Fear"
        bias = "Cautious"
        message = (
            "De markt is voorzichtig. Atlas blijft terughoudend tenzij meerdere "
            "indicatoren bullish zijn."
        )
    elif value <= 55:
        sentiment = "Neutral"
        bias = "Neutral"
        message = "De markt is neutraal. Technische indicatoren geven nu de doorslag."
    elif value <= 75:
        sentiment = "Greed"
        bias = "Risk of overheating"
        message = (
            "De markt is optimistisch. Atlas let extra op tekenen van oververhitting."
        )
    else:
        sentiment = "Extreme greed"
        bias = "Correction risk"
        message = "De markt staat in Extreme Greed. Atlas is extra voorzichtig met nieuwe posities."

    if has_open_position:
        position_note = "Er is momenteel een open positie."
    else:
        position_note = "Er is momenteel geen open positie."

    return {
        "sentiment": sentiment,
        "bias": bias,
        "message": message,
        "position_note": position_note,
        "classification": classification,
        "value": value,
    }
