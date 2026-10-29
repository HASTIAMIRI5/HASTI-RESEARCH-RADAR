from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.config import settings
from app.services.research import generate_brief
from app.services.storage import get_brief, init_db, list_recent_briefs, save_brief

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered research and brief generation SaaS for founders, analysts, and teams.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.on_event("startup")
async def startup_event() -> None:
    init_db()


class ResearchBriefRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="The subject to research")
    audience: str = Field(default="founders and operators", min_length=2)
    goal: str = Field(default="Build a clear research and action plan", min_length=2)
    focus_areas: list[str] = Field(default_factory=lambda: ["market demand", "competitive landscape", "execution risks"])
    sources: list[str] = Field(default_factory=lambda: ["public research", "customer interviews", "market patterns"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
        },
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    briefs = list_recent_briefs(limit=8)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "briefs": briefs,
        },
    )


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/api/briefs")
async def get_briefs() -> list[dict[str, Any]]:
    return list_recent_briefs(limit=20)


@app.get("/api/briefs/{brief_id}")
async def get_brief_by_id(brief_id: int) -> dict[str, Any]:
    item = get_brief(brief_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brief not found")
    return item


@app.post("/api/research/brief")
async def generate_research_brief(payload: ResearchBriefRequest) -> JSONResponse:
    result = generate_brief(
        topic=payload.topic,
        focus_areas=payload.focus_areas,
        sources=payload.sources,
        audience=payload.audience,
        goal=payload.goal,
    )

    saved_id = save_brief(
        {
            "title": result.get("title", f"Research Brief: {payload.topic}"),
            "topic": payload.topic,
            "goal": payload.goal,
            "audience": payload.audience,
            "source_mix": result.get("source_mix", ", ".join(payload.sources)),
            "brief": json.dumps(result),
        }
    )
    result["id"] = saved_id
    return JSONResponse(content=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
