# Hasti Research Radar

AI-powered personal assistant for research and brief generation.

Hasti Research Radar is a premium research workflow app that turns a topic into a clear brief, strategic findings, risk analysis, and an execution plan. It is designed to feel like a founder-grade research assistant and can be extended for real web sourcing, saved workspaces, and enterprise team collaboration.

## Features

- Premium landing page and product experience
- AI-powered research brief generation
- Audience and goal-driven prompt engineering
- Focus area and source mix configuration
- Saved brief history with SQLite persistence
- FastAPI + Jinja templates architecture
- Docker deployment support
- Solid test coverage for the core API

## Tech stack

- Python 3.12
- FastAPI
- Jinja2
- SQLite for local data persistence
- OpenAI-compatible API integration
- Docker

## Quick start

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

4. Start the app:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Open:
   ```text
   http://localhost:8000
   ```

## API

Health check:
```bash
curl http://localhost:8000/api/health
```

Generate a brief:
```bash
curl -X POST http://localhost:8000/api/research/brief \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI for venture research",
    "audience": "founders and investors",
    "goal": "Build a clear strategic roadmap",
    "focus_areas": ["market opportunity", "product differentiation", "execution risk"],
    "sources": ["public market research", "customer interviews", "industry analyst reports"]
  }'
```

## Project structure

```text
hasti-research-radar/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── research.py
│   │   └── storage.py
│   ├── static/
│   │   ├── app.js
│   │   └── styles.css
│   └── templates/
│       ├── dashboard.html
│       └── index.html
├── assets/
│   ├── hero-illustration.svg
│   └── logo.svg
├── data/
│   └── research_briefs.db
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── .python-version
```

## Docker

```bash
docker build -t hasti-research-radar .
docker run -p 8000:8000 hasti-research-radar
```

## Roadmap

- Real web search and source ingestion
- User authentication and authoring dashboard
- Team workspace collaboration
- Export to PDF and Markdown
- AI agent orchestration for multi-stage research
- Advanced analytics and trend dashboards

## License

MIT
