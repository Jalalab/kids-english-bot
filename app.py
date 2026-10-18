# app.py
# The Flask server. It connects all the parts together.

import os
import time
from flask import Flask, request, jsonify, render_template

from bot.modes import detect_mode, detect_mood
from bot.curriculum import check_answer
from bot.progress import get_progress
from bot.prompts import SYSTEM_PROMPT, build_prompt
from bot.llm import get_reply

app = Flask(__name__)

GREETING = "Hi! I'm Jenny 😊 How are you feeling today?"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    start = time.time()
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default")
    text = (data.get("message") or "").strip()

    p = get_progress(session_id)

    # Empty message = start of the chat, so just say hello
    if not text:
        p.add_message("Jenny", GREETING)
        return jsonify({"reply": GREETING, "mode": "greeting", "level": p.level,
                        "score": p.score, "source": "fixed", "ms": 0})

    # 1. Rules: what does the child need right now?
    mode = detect_mode(text, p.last_was_question, p.learn_streak)
    mood = detect_mood(text)

    # 2. Check the answer if we had asked a lesson question
    feedback = None
    p.level_changed = None
    if p.last_was_question and p.current_item and mode not in ("comfort", "play"):
        correct = check_answer(p.current_item, text)
        feedback = "correct" if correct else "wrong"
        p.record_answer(correct)

    # 3. Pick the next lesson question (only in learn mode)
    next_q = None
    if mode == "learn":
        next_q = p.next_question()["q"]
        p.last_was_question = True
    else:
        p.last_was_question = False

    # 4. Build the prompt and ask the LLM (history = before this message)
    prompt = build_prompt(mode, mood, p.level, p.score, p.topics_covered,
                          p.recent_mistakes, p.history, text,
                          feedback, next_q, p.level_changed)
    result = get_reply(SYSTEM_PROMPT, prompt, mode, feedback, next_q, p.level_changed)

    # 5. Save to memory
    p.add_message("child", text)
    p.add_message("Jenny", result["text"])
    p.update_mode(mode)

    total_ms = int((time.time() - start) * 1000)
    print(f"[{mode}] level={p.level} source={result['source']} "
          f"llm={result['ms']}ms total={total_ms}ms error={result['error']}")

    return jsonify({"reply": result["text"], "mode": mode, "level": p.level,
                    "score": p.score, "source": result["source"], "ms": total_ms})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)