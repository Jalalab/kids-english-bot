# Jenny: English Learning Chatbot for Children (Under 7)

A simple web chatbot that teaches English to young children step by step.
It notices how the child feels and switches between learning, chatting,
playing and comforting, so it does not teach in every message.

**Live demo:** https://kids-english-bot.onrender.com
(Free hosting sleeps when idle, so the first load can take 30-60 seconds.)

## Features

- **3 levels:** L1 single words, L2 tiny sentences, L3 short questions and answers.
  5 correct answers in a row = level up. 3 wrong in a row = one level down.
- **Mode detection (rules):** learn, chat, play, comfort. After 2 learning turns
  in a row, the bot takes a break from teaching.
- **Social and emotional learning:** praises effort, names feelings, offers comfort
  without teaching when the child is upset, encourages curiosity.
- **Context aware:** each reply uses the child's level, score, topics learned,
  recent mistakes and the last 6 messages.
- **Fast:** one LLM call per message. A pre-written fallback reply is used if the
  LLM fails or takes longer than 1.2 seconds.

## Tech stack

Python, Flask, plain HTML/CSS/JavaScript, Groq API (openai/gpt-oss-20b),
Gunicorn, Render.

## Project structure

```
app.py              Flask server and /chat route
bot/modes.py        mode and mood detection
bot/curriculum.py   L1/L2/L3 lesson content
bot/progress.py     per-child memory, levels, score
bot/prompts.py      builds the LLM prompt
bot/llm.py          LLM call, timeout and fallback
templates/          chat page
static/             CSS and JavaScript
docs/               system design and architecture diagram
```

## Run locally

1. Install Python 3.10 or newer.
2. Clone the repo and open the folder:
```
   git clone https://github.com/Jalalab/kids-english-bot.git
   cd kids-english-bot
```
3. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
```
   (Mac/Linux: `source venv/bin/activate`)
4. Install packages:
```
   pip install -r requirements.txt
```
5. Get a free API key at console.groq.com, then create a file named `.env`:
```
   LLM_API_KEY=your_key_here
```
6. Run the app and open http://localhost:5000:
```
   python app.py
```

## Deploy on Render

1. Push the repo to GitHub.
2. On render.com choose **New + > Web Service** and connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --workers 1 --threads 4 --timeout 30`
5. Plan: Free.
6. Add the environment variable `LLM_API_KEY` with your Groq key.
7. Click **Create Web Service**.

One worker is used on purpose: child sessions are stored in memory.

## Limitations

- Sessions are in memory, so they reset when the server restarts.
- Mode detection uses keywords, so unusual phrases may be missed.
- Free hosting has cold starts.
