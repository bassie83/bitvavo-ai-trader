def calculate_confidence(
    fear_greed: dict,
    has_open_position: bool,
    technical: dict,
) -> dict:
    score = 50
    factors = []

    value = fear_greed["value"]

    if value <= 25:
        score += 15
        factors.append("Extreme Fear ondersteunt mogelijke koopkansen.")
    elif value <= 45:
        score += 5
        factors.append("Fear geeft een voorzichtig positief contrarian signaal.")
    elif value <= 55:
        factors.append("Neutraal sentiment heeft weinig invloed.")
    elif value <= 75:
        score -= 5
        factors.append("Greed vraagt om extra voorzichtigheid.")
    else:
        score -= 15
        factors.append("Extreme Greed verhoogt correctierisico.")

    if has_open_position:
        score -= 10
        factors.append(
            "Er is al een open positie, dus nieuwe BUY voorzichtig beoordelen."
        )
    else:
        factors.append("Er is geen open positie.")

    technical_score = technical.get("score", 0)

    if technical_score >= 80:
        score += 20
        factors.append("Technische analyse is sterk bullish.")
    elif technical_score >= 60:
        score += 10
        factors.append("Technische analyse ondersteunt een BUY.")
    elif technical_score >= 40:
        factors.append("Technische analyse is neutraal.")
    else:
        score -= 10
        factors.append("Technische analyse is zwak.")

    score = max(0, min(100, score))

    return {
        "score": score,
        "factors": factors,
    }
