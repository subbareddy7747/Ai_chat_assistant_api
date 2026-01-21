import requests
from app.core.config import LLM_API_KEY, LLM_MODEL
import logging
import os

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"




logger = logging.getLogger(__name__)




def call_llm(message: str) -> str:
    """
    Calls a real LLM API and returns a response.
    Raises Exception on failure (handled by route).
    """
    api_key = os.getenv("LLM_API_KEY")
    logger.error(f"LLM_API_KEY present? {bool(api_key)}")
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        "temperature": 0.7,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=15)

    if response.status_code != 200:
        raise RuntimeError("LLM API call failed")

    data = response.json()

    return data["choices"][0]["message"]["content"]
