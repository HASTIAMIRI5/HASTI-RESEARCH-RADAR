from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.research import generate_brief

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
        },
    )


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.post("/api/research/brief")
async def generate_research_brief(request: Request) -> JSONResponse:
    payload = await request.json()
    topic = payload.get("topic") or "AI-powered research workflows"
    focus_areas = payload.get("focus_areas") or [
        "market demand",
        "product differentiation",
        "competitive positioning",
    ]
    sources = payload.get("sources") or [
        "public market research",
        "user interviews",
        "pattern analysis",
    ]
    audience = payload.get("audience") or "founders and operators"
    goal = payload.get("goal") or "Build a clear research and action plan"

    result = generate_brief(topic=topic, focus_areas=focus_areas, sources=sources, audience=audience, goal=goal)
    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
