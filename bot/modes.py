# bot/modes.py
# Rule-based detection of what the child needs right now.
# Four modes: learn, chat, play, comfort

COMFORT_WORDS = [
    "sad", "scared", "afraid", "angry", "mad", "cry", "crying",
    "hurt", "lonely", "bad day", "i can't", "i cant", "dont want",
    "don't want", "hate", "tired", "sick", "miss mom", "miss dad",
]

PLAY_WORDS = [
    "play", "game", "song", "sing", "riddle", "joke", "story",
    "bored", "boring", "fun",
]

CHAT_WORDS = [
    "my dog", "my cat", "my mom", "my dad", "my friend", "my toy",
    "i went", "i have", "today", "yesterday", "school", "i like my",
]

LOW_ENERGY = ["ok", "okay", "hmm", "hm", "idk", "yes", "no", "k", "umm", "um", "..."]


def detect_mode(text, last_was_question, learn_streak):
    """
    Decide the mode for this turn.
    text: what the child typed
    last_was_question: True if the bot just asked a lesson question
    learn_streak: how many learning turns happened in a row
    Returns: "comfort", "play", "chat" or "learn"
    """
    t = text.lower().strip()

    # 1. Feelings come first. Comfort always wins.
    if any(w in t for w in COMFORT_WORDS):
        return "comfort"

    # 2. Child asks for fun
    if any(w in t for w in PLAY_WORDS):
        return "play"

    # 3. Very short or low-energy reply (and not an answer to a question)
    if t in LOW_ENERGY and not last_was_question:
        return "play"

    # 4. Child is telling us something about their life
    if any(w in t for w in CHAT_WORDS):
        return "chat"

    # 5. Do not teach every turn: after 2 learning turns, take a break
    if learn_streak >= 2:
        return "chat"

    # 6. Default
    return "learn"


def detect_mood(text):
    """Simple mood label, used to guide the tone of the reply."""
    t = text.lower()
    if any(w in t for w in COMFORT_WORDS):
        return "upset"
    if any(w in t for w in ["happy", "good", "great", "yay", "fun", "love"]):
        return "happy"
    if any(w in t for w in PLAY_WORDS[-3:]):
        return "bored"
    return "neutral"