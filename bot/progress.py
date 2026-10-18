# bot/progress.py
# Remembers each child's progress for the current session (in memory).

from bot.curriculum import MAX_LEVEL, get_item

LEVEL_UP_STREAK = 5    # correct answers in a row to go up
LEVEL_DOWN_STREAK = 3  # wrong answers in a row to go down

SESSIONS = {}  # session_id -> Progress


class Progress:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.correct_streak = 0
        self.wrong_streak = 0
        self.item_index = 0
        self.current_item = None      # the lesson question being asked now
        self.topics_covered = []
        self.recent_mistakes = []     # last few wrong topics
        self.history = []             # last 6 messages
        self.last_mode = "learn"
        self.learn_streak = 0         # learning turns in a row
        self.last_was_question = False
        self.turns = 0
        self.level_changed = None     # "up", "down" or None (for this turn)

    def add_message(self, role, text):
        self.history.append({"role": role, "text": text})
        self.history = self.history[-6:]

    def next_question(self):
        """Pick the next lesson question for the current level."""
        self.current_item = get_item(self.level, self.item_index)
        self.item_index += 1
        return self.current_item

    def record_answer(self, correct):
        """Update score, streaks and level after the child answers."""
        self.level_changed = None
        topic = self.current_item["topic"] if self.current_item else None

        if correct:
            self.score += 1
            self.correct_streak += 1
            self.wrong_streak = 0
            if topic and topic not in self.topics_covered:
                self.topics_covered.append(topic)
            if self.correct_streak >= LEVEL_UP_STREAK and self.level < MAX_LEVEL:
                self.level += 1
                self.correct_streak = 0
                self.item_index = 0
                self.level_changed = "up"
        else:
            self.wrong_streak += 1
            self.correct_streak = 0
            if topic:
                self.recent_mistakes.append(topic)
                self.recent_mistakes = self.recent_mistakes[-3:]
            if self.wrong_streak >= LEVEL_DOWN_STREAK and self.level > 1:
                self.level -= 1
                self.wrong_streak = 0
                self.item_index = 0
                self.level_changed = "down"

    def update_mode(self, mode):
        """Track the mode so we don't teach every turn."""
        self.last_mode = mode
        if mode == "learn":
            self.learn_streak += 1
        else:
            self.learn_streak = 0
        self.turns += 1


def get_progress(session_id):
    """Get (or create) the progress for this session."""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = Progress()
    return SESSIONS[session_id]