import requests

FEAR_GREED_URL = "https://api.alternative.me/fng/"


def get_fear_greed() -> dict:
    response = requests.get(FEAR_GREED_URL, timeout=10)
    response.raise_for_status()

    data = response.json()["data"][0]

    value = int(data["value"])
    classification = data["value_classification"]

    if value <= 25:
        insight = (
            "Historisch gezien ontstaan tijdens Extreme Fear "
            "regelmatig goede instapkansen. Wacht op bevestiging "
            "van RSI, MACD en trend."
        )
    elif value <= 45:
        insight = (
            "De markt is voorzichtig. Nieuwe posities alleen "
            "openen wanneer meerdere indicatoren bullish zijn."
        )
    elif value <= 55:
        insight = (
            "Neutrale marktomstandigheden. Laat technische "
            "indicatoren de doorslag geven."
        )
    elif value <= 75:
        insight = (
            "Optimistische markt. Let op oververhitting en "
            "bevestig signalen zorgvuldig."
        )
    else:
        insight = (
            "Extreme Greed kan wijzen op euforie. Wees alert "
            "op mogelijke correcties."
        )

    return {
        "value": value,
        "classification": classification,
        "timestamp": data["timestamp"],
        "insight": insight,
    }
