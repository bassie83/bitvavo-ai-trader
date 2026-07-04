import os

from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError

load_dotenv(".env")

_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def chat(prompt: str, model: str = "gpt-5.5") -> str:
    """
    Send a prompt to the configured AI provider.

    Returns a safe fallback JSON string if the provider is unavailable.
    """

    try:
        response = _client.responses.create(
            model=model,
            input=prompt,
        )

        return response.output_text.strip()

    except OpenAIError as error:
        print(f"⚠️ AI provider unavailable: {error}", flush=True)

        return """
{
    "summary": "AI provider unavailable.",
    "sentiment": "neutral",
    "impact": "LOW",
    "confidence": 0,
    "affected_assets": [],
    "reasoning": [
        "OpenAI API call failed.",
        "Atlas continues without news intelligence."
    ]
}
"""
