# bot/prompts.py
# Builds the instructions we send to the LLM.

SYSTEM_PROMPT = """You are Jenny, a kind and playful English teacher for children under 7.

Rules:
- Reply in at most 2 SHORT sentences. Use very simple words.
- You may use 1 or 2 emojis.
- Be warm, patient and encouraging. Praise effort, not only correct answers.
- Never ask for personal information (full name, address, school, phone).
- Never use scary, rude or grown-up topics.
- Follow the MODE given in each message exactly.
"""

MODE_RULES = {
    "learn": "LEARN mode: react to the child's answer, then ask the lesson question given below. Keep it fun.",
    "chat": "CHAT mode: answer what the child said in a friendly way. Do NOT quiz. You may teach ONE tiny new English word naturally.",
    "play": "PLAY mode: be playful. Offer or give a tiny riddle, song line or game using simple English. Do NOT quiz.",
    "comfort": "COMFORT mode: be gentle. Name the feeling (for example: It's okay to feel sad). Offer comfort. Do NOT teach and do NOT ask a lesson question.",
}

LEVEL_NAMES = {
    1: "single words (colors, animals, numbers)",
    2: "tiny 3-4 word sentences",
    3: "short questions and full-sentence answers",
}


def build_prompt(mode, mood, level, score, topics, mistakes, history,
                 child_text, feedback, next_question, level_changed):
    """
    mode: learn / chat / play / comfort
    mood: upset / happy / bored / neutral
    feedback: "correct", "wrong" or None (was the child's answer right?)
    next_question: the lesson question to ask (only used in learn mode)
    level_changed: "up", "down" or None
    Returns the user prompt text.
    """
    lines = []
    lines.append(MODE_RULES[mode])
    lines.append(f"Child's mood: {mood}.")
    lines.append(f"Child's level: {level} - {LEVEL_NAMES[level]}. Score: {score}.")

    if topics:
        lines.append("Topics already learned: " + ", ".join(topics) + ".")
    if mistakes:
        lines.append("Topics the child found hard: " + ", ".join(mistakes) + ".")

    if mode == "learn":
        if feedback == "correct":
            lines.append("The child's last answer was CORRECT. Praise them.")
        elif feedback == "wrong":
            lines.append("The child's last answer was NOT right. Be kind, say it is okay, and give a tiny hint. Do not say 'wrong'.")
        if level_changed == "up":
               lines.append("The child just moved UP a level! Celebrate it.")
        elif level_changed == "down":
            lines.append("We are going back one level to practice. Say it is okay and fun to practice.")
        if next_question:
            lines.append(f'You MUST end your reply with this exact question, word for word: "{next_question}"')

    if history:
        lines.append("Recent conversation:")
        for m in history:
            who = "Child" if m["role"] == "child" else "Jenny"
            lines.append(f"{who}: {m['text']}")

    lines.append(f"Child just said: {child_text}")
    lines.append("Now write Jenny's reply (max 2 short sentences).")
    return "\n".join(lines)