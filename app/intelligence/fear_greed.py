import requests

FEAR_GREED_URL = "https://api.alternative.me/fng/"


def get_fear_greed() -> dict:
    """
    Haalt de actuele Fear & Greed Index op.
    """

    response = requests.get(FEAR_GREED_URL, timeout=10)
    response.raise_for_status()

    data = response.json()["data"][0]

    return {
        "value": int(data["value"]),
        "classification": data["value_classification"],
        "timestamp": data["timestamp"],
    }
