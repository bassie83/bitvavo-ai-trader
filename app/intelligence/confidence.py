def calculate_confidence(
    fear_greed: dict,
    has_open_position: bool,
    technical: dict,
) -> dict:
    base_score = 50
    factors = []

    value = fear_greed["value"]

    if value <= 25:
        fear_greed_score = 15
        factors.append("Extreme Fear ondersteunt mogelijke koopkansen.")
    elif value <= 45:
        fear_greed_score = 5
        factors.append("Fear geeft een voorzichtig positief contrarian signaal.")
    elif value <= 55:
        fear_greed_score = 0
        factors.append("Neutraal sentiment heeft weinig invloed.")
    elif value <= 75:
        fear_greed_score = -5
        factors.append("Greed vraagt om extra voorzichtigheid.")
    else:
        fear_greed_score = -15
        factors.append("Extreme Greed verhoogt correctierisico.")

    if has_open_position:
        open_position_score = -10
        factors.append(
            "Er is al een open positie, dus nieuwe BUY voorzichtig beoordelen."
        )
    else:
        open_position_score = 0
        factors.append("Er is geen open positie.")

    technical_score_value = technical.get("score", 0)

    if technical_score_value >= 80:
        technical_score = 20
        factors.append("Technische analyse is sterk bullish.")
    elif technical_score_value >= 60:
        technical_score = 10
        factors.append("Technische analyse ondersteunt een BUY.")
    elif technical_score_value >= 40:
        technical_score = 0
        factors.append("Technische analyse is neutraal.")
    else:
        technical_score = -10
        factors.append("Technische analyse is zwak.")

    score = base_score + fear_greed_score + open_position_score + technical_score
    score = max(0, min(100, score))

    if score >= 80:
        level = "HIGH"
    elif score >= 60:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "factors": factors,
        "breakdown": [
            {
                "name": "Fear & Greed",
                "description": fear_greed["classification"],
                "impact": f"{fear_greed_score:+d}",
            },
            {
                "name": "Technical Analysis",
                "description": f"{technical_score_value}/100",
                "impact": f"{technical_score:+d}",
            },
            {
                "name": "Open Position",
                "description": "Ja" if has_open_position else "Nee",
                "impact": f"{open_position_score:+d}",
            },
        ],
    }
