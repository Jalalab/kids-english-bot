# bot/curriculum.py
# Simple lesson content for each level.
# Each item has a question and the accepted answers (lowercase).

CURRICULUM = {
    1: {
        "name": "Level 1: Words",
        "goal": "Single words: colors, animals, numbers",
        "items": [
            {"q": "What color is the sun?", "a": ["yellow"], "topic": "colors"},
            {"q": "What color is grass?", "a": ["green"], "topic": "colors"},
            {"q": "What color is the sky?", "a": ["blue"], "topic": "colors"},
            {"q": "What animal says meow?", "a": ["cat", "kitten"], "topic": "animals"},
            {"q": "What animal says woof?", "a": ["dog", "puppy"], "topic": "animals"},
            {"q": "What animal says moo?", "a": ["cow"], "topic": "animals"},
            {"q": "What number comes after one?", "a": ["two", "2"], "topic": "numbers"},
            {"q": "What number comes after two?", "a": ["three", "3"], "topic": "numbers"},
            {"q": "How many eyes do you have?", "a": ["two", "2"], "topic": "numbers"},
        ],
    },
    2: {
        "name": "Level 2: Tiny sentences",
        "goal": "Simple 3-4 word sentences, body parts, family",
        "items": [
            {"q": "Say it with me: I see a cat. What do you see?", "a": ["i see a cat", "see a cat"], "topic": "sentences"},
            {"q": "Finish it: I have two ___ (eyes or ears)?", "a": ["eyes", "ears"], "topic": "body"},
            {"q": "What do we use to hear? Say: I hear with my ___.", "a": ["ears", "ear"], "topic": "body"},
            {"q": "Who makes food at home? Mom or Dad? Say: I love my ___.", "a": ["mom", "dad", "mother", "father"], "topic": "family"},
            {"q": "Say: I like apples. What do you like?", "a": ["i like"], "topic": "sentences"},
            {"q": "Say: The dog is big. Is a dog big or small?", "a": ["big"], "topic": "opposites"},
        ],
    },
    3: {
        "name": "Level 3: Short questions and answers",
        "goal": "Answer short questions in a full sentence",
        "items": [
            {"q": "What do you like to eat?", "a": ["i like", "i eat", "i love"], "topic": "food"},
            {"q": "What is your favorite animal?", "a": ["my favorite", "i like", "i love"], "topic": "animals"},
            {"q": "What do you do in the morning?", "a": ["i wake", "i brush", "i eat", "i go"], "topic": "daily life"},
            {"q": "Where do you sleep?", "a": ["bed", "i sleep"], "topic": "home"},
            {"q": "What do you see in the sky?", "a": ["sun", "moon", "star", "cloud", "bird"], "topic": "nature"},
        ],
    },
}

MAX_LEVEL = 3


def get_item(level, index):
    """Return the lesson item at this index (wraps around)."""
    items = CURRICULUM[level]["items"]
    return items[index % len(items)]


def check_answer(item, child_text):
    """True if any accepted answer appears in what the child typed."""
    text = child_text.lower().strip()
    return any(ans in text for ans in item["a"])