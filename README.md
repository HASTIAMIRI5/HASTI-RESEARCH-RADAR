# Hasti Research Radar

AI-powered personal assistant for research and brief generation.

A polished web app that helps you generate research briefs, identify signals, summarize findings, and plan next actions from a single topic.

## Features

- Smart research brief generation
- Topic and audience targeting
- Signal extraction and recommendations
- Clean dashboard UI
- Optional OpenAI integration
- FastAPI backend with Jinja templates
- Docker-ready deployment

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Open http://localhost:8000

## Environment variables

- `OPENAI_API_KEY` - optional; enables GPT-powered generation
- `APP_NAME` - display name for the app
- `APP_VERSION` - app version

## Example prompt

> "Analyze the impact of AI on startup customer acquisition. Focus on product, competition, and execution risks for a founder in 2026."

## Project structure

```text
hasti-research-radar/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── research.py
│   ├── static/
│   │   ├── app.js
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
│   └── __init__.py
├── assets/
│   ├── logo.svg
│   └── hero-illustration.svg
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── .python-version
```

## Deployment

Docker:
```bash
docker build -t hasti-research-radar .
docker run -p 8000:8000 hasti-research-radar
```

## License

MIT
