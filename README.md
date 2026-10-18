
# System Design: Jenny, English Learning Chatbot for Children (Under 7)

## 1. Goal

Teach English to children under 7 step by step, while noticing how the child
feels and not teaching in every message. Replies must arrive in under 2 seconds.

## 2. Design idea

**Rules decide, the LLM talks.**

- Rules handle what must be fast and predictable: mode detection, answer
  checking, level changes, and deciding when not to teach.
- The LLM does one job: write a short, friendly reply that follows the
  instructions the rules give it.

This keeps latency low (only one LLM call per message) and behavior predictable.

## 3. Components

| Component | File | Job |
|---|---|---|
| Chat UI | templates/index.html, static/ | Chat bubbles, quick-reply buttons, level and star display |
| Server | app.py | Receives the message, runs the pipeline, returns the reply |
| Mode detector | bot/modes.py | Chooses learn, chat, play or comfort; detects mood |
| Curriculum | bot/curriculum.py | L1, L2, L3 questions and accepted answers |
| Progress store | bot/progress.py | Per-session level, score, streaks, mistakes, history |
| Prompt builder | bot/prompts.py | Turns mode, level and history into LLM instructions |
| LLM client | bot/llm.py | Calls Groq with a timeout and uses a fallback reply on failure |

## 4. Data flow

1. The child types a message (or taps a quick-reply button).
2. The browser sends it to `POST /chat` with a random session id.
3. The mode detector chooses the mode from the message and recent history.
4. If the bot had asked a lesson question, the answer is checked and the score,
   streaks and level are updated.
5. In learn mode, the next lesson question is picked.
6. The prompt builder combines mode, mood, level, score, topics learned, recent
   mistakes and the last 6 messages.
7. One call is made to the LLM (timeout 1.2 s). If it fails, is empty or is
   slow, a pre-written fallback reply is used.
8. The reply, mode, level and score return to the browser.

## 5. Mode logic

| Mode | Triggered by | Bot behavior |
|---|---|---|
| comfort | Feeling words such as sad, scared, angry, "I can't" | Names the feeling, comforts, no teaching, no quiz |
| play | Words like play, game, song, riddle, or low-energy replies | Riddle, song line or game, no quiz |
| chat | The child talks about their life ("my dog is big"), or after 2 learning turns in a row | Friendly answer, may add one tiny new word |
| learn | Default | Reacts to the answer, then asks the next lesson question |

Comfort has the highest priority. The "after 2 learning turns" rule makes sure
the bot does not teach in every interaction.

## 6. Level progression

- **L1:** single words (colors, animals, numbers).
- **L2:** tiny 3 to 4 word sentences, body parts, family.
- **L3:** short questions answered in a full sentence.
- 5 correct answers in a row = level up. 3 wrong in a row = one level down
  (practice again with kind hints).

## 7. Social and emotional learning (SEL)

- Praises effort, not only correct answers.
- Names feelings ("It's okay to feel sad").
- Comfort mode never teaches or quizzes.
- A wrong answer gets a kind hint, never the word "wrong".
- Starts with "How are you feeling today?" and encourages curiosity.
- The system prompt forbids personal questions and scary or adult topics.

## 8. Context awareness

Each session stores level, score, topics learned, recent mistake topics, the
last mode and the last 6 messages. All of this goes into the prompt, so replies
adapt to the child's history.

## 9. Latency strategy

- Only one LLM call per message; mode detection uses rules (about 0 ms).
- Small model (`openai/gpt-oss-20b` on Groq), short replies, low reasoning effort.
- Connection reuse with a requests Session.
- Hard timeout of 1.2 s, then a fallback reply.
- Measured: about 660 to 850 ms per reply in manual tests (see section 12).

## 10. Technology choices and trade-offs

| Choice | Why | Trade-off |
|---|---|---|
| Flask + plain JS | Simple, no build step | Less polished UI than a framework |
| Rules for modes | Fast, predictable, explainable | Keywords can miss unusual phrases |
| Groq LLM | Very fast inference, free tier | Depends on an external service |
| In-memory sessions | Simple, no database | Sessions reset on restart; one worker only |
| Fallback replies | Bot never freezes | Fallback text is less natural |
| Render free plan | Live URL from GitHub in minutes | Cold start after idle |

## 11. Safety

- No personal information is requested.
- The system prompt limits replies to 2 short, kind sentences.
- No accounts and no data stored beyond the session in memory.


## 13. Limitations and future work

- Use a database (for example SQLite or Redis) for persistent sessions.
- Replace keyword mode detection with a small classifier.
- Add voice input and output for children who cannot type yet.
- Add a parent dashboard to view progress.
