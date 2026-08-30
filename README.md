# 🌿 Plant Doctor AI

I built this because my mom kept sending me blurry WhatsApp photos of random plants asking "yeh kya hai, isko paani kitna dena hai?" — so I figured, why not let an AI answer that instead of me.

Plant Doctor AI identifies plants from a photo (or just a name, typed in English, Urdu, or Roman Urdu) and gives you a full care guide — watering, sunlight, soil, common diseases, all of it — generated on the spot.

**[Live App →](#)** *(link goes here once deployed)*

---

## What it actually does

- Take a photo or upload one — it'll tell you what plant it is
- Not sure it got it right? It shows you the top 3 guesses so you can pick
- Or skip the photo entirely and just type the name — "gulab", "rose", "گلاب" all work
- Once it knows the plant, it generates a proper care guide: water, sunlight, soil, fertilizer, pruning, diseases, whether it's safe around pets, all of it
- You can download the guide as a text file to keep
- Keeps a small history of what you've searched so you're not repeating yourself

---

## How it's built

Two APIs doing the heavy lifting:
- **PlantNet** takes a photo and tells you what species it probably is (with a confidence score)
- **Groq** (running an open-source LLM) does two jobs — it turns "gulab" or "منی پلانٹ" into a proper plant name, and it writes the actual care guide once it knows what plant it's dealing with

Everything's tied together in Streamlit for the interface.

```
Photo  → PlantNet (identify) ─┐
                                ├──→ Groq (care guide) → Displayed on screen
Text   → Groq (identify) ──────┘
```

---

## Stack

- **Streamlit** for the whole frontend — no separate backend server, keeps things simple
- **Python** for everything else
- **PlantNet API** — free tier, plant ID from images
- **Groq API** — free tier, fast LLM inference for text generation
- `requests` for the API calls, `python-dotenv` for keeping API keys out of the code, `Pillow` for image handling

I went with Streamlit over a full React/FastAPI setup mainly because the target user (my mom, basically) just needs to open a link and use it — no app store, no install, works on a phone browser fine.

---

## Project layout

```
plant-doctor-ai/
├── app.py            # everything UI-related — screens, styling, navigation
├── api.py            # talks to PlantNet + Groq
├── utils.py          # cleans up the messy API responses into something usable
├── prompts.py        # the actual prompts sent to Groq
├── config.py         # loads API keys from .env
├── requirements.txt
├── .env              # your API keys go here — never committed
└── screenshots/
```

I kept the API-calling code (`api.py`) separate from the UI code (`app.py`) on purpose — when Groq deprecated the model I was originally using halfway through building this, I only had to change one line in `config.py` instead of hunting through the whole codebase.

---

## Running it yourself

```bash
git clone https://github.com/YOUR_USERNAME/plant-doctor-ai.git
cd plant-doctor-ai
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

You'll need two free API keys:
- PlantNet: https://my.plantnet.org
- Groq: https://console.groq.com

Drop them into a `.env` file:
```
PLANTNET_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Then:
```bash
streamlit run app.py
```

---

## What's not built yet (but planned)

- Disease/pest detection from photos, not just identification
- Watering reminders
- Full Urdu interface, not just Urdu search input
- Nicer PDF export instead of plain text

---

## Why I built it this way

This started as a portfolio project for AI internship applications — I specifically didn't want it to look like a tutorial project, so the focus was on things that actually come up in real AI engineering work: handling flaky APIs gracefully, dealing with a model getting deprecated mid-project, prompt engineering that actually returns parseable JSON, and keeping the code structured enough that changing one piece doesn't break three others.

---

## License

MIT — do whatever you want with it.