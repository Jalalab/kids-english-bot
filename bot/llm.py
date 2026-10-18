# bot/llm.py
# Calls the LLM (Groq) with a short timeout. If it fails or is slow,
# a ready-made fallback reply is used so the bot never freezes.

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
TIMEOUT_SECONDS = 1.2

_session = requests.Session()  # reuses the connection = faster


def fallback_reply(mode, feedback=None, next_question=None, level_changed=None):
    """Pre-written reply used when the LLM is slow or fails."""
    if mode == "comfort":
        return "It's okay to feel that way. 💛 I'm right here with you. Want to hear a happy song?"
    if mode == "play":
        return "Let's play! 🎵 Twinkle, twinkle, little star. Can you sing with me?"
    if mode == "chat":
        return "That sounds nice! 😊 Tell me more!"

    # learn mode
    parts = []
    if level_changed == "up":
        parts.append("Wow, you moved up a level! 🎉")
    elif level_changed == "down":
        parts.append("Let's practice a bit more, it's fun! 😊")
    elif feedback == "correct":
        parts.append("Great job! 🌟")
    elif feedback == "wrong":
        parts.append("Nice try! It's okay. 💛")
    else:
        parts.append("Let's learn! 😊")
    if next_question:
        parts.append(next_question)
    return " ".join(parts)


def get_reply(system_prompt, user_prompt, mode, feedback=None,
              next_question=None, level_changed=None):
    """Returns a dict: text, source ('llm' or 'fallback'), ms, error."""
    start = time.time()
    api_key = os.getenv("LLM_API_KEY")

    try:
        if not api_key:
            raise ValueError("LLM_API_KEY is missing")

        response = _session.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 300,
                "reasoning_effort": "low",
                "temperature": 0.7,
            },
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        text = (response.json()["choices"][0]["message"].get("content") or "").strip()
        if not text:
            raise ValueError("LLM returned an empty reply")
        return {"text": text, "source": "llm",
                "ms": int((time.time() - start) * 1000), "error": None}

    except Exception as e:
        return {"text": fallback_reply(mode, feedback, next_question, level_changed),
                "source": "fallback",
                "ms": int((time.time() - start) * 1000), "error": str(e)}