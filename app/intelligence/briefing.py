def generate_daily_briefing(
    fear_greed: dict,
    technical: dict,
    confidence: dict,
    has_open_position: bool,
) -> dict:
    position_text = (
        "Er is momenteel een open positie."
        if has_open_position
        else "Er is momenteel geen open positie."
    )
    if confidence["score"] >= 80:
        advice = "Atlas ziet een sterk signaal. Een BUY kan worden overwogen als de trend bevestigt."
    elif confidence["score"] >= 60:
        advice = (
            "Atlas adviseert om de markt te volgen en te wachten op extra bevestiging."
        )
    else:
        advice = "Atlas adviseert momenteel geen nieuwe positie te openen."
    market_text = (
        f"De markt bevindt zich momenteel in "
        f"{fear_greed['classification']} ({fear_greed['value']})."
    )

    technical_text = (
        f"De technische analyse geeft een score van "
        f"{technical['score']}/100 met advies {technical['advice']}."
    )

    confidence_text = (
        f"De confidence score is {confidence['score']}% " f"({confidence['level']})."
    )

    message = (
        f"{market_text}\n\n"
        f"{technical_text}\n\n"
        f"{confidence_text}\n\n"
        f"{position_text}\n\n"
        f"👉 Advies: {advice}"
    )

    return {
        "title": "Atlas Daily Briefing",
        "message": message,
    }
