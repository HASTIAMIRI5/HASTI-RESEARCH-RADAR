from __future__ import annotations

import json
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

from app.config import settings


def _ensure_list(value: Any, default: list[str]) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        cleaned = [part.strip() for part in value.split(",") if part.strip()]
        return cleaned or default
    return default


def _fallback_brief(topic: str, focus_areas: list[str], sources: list[str], audience: str, goal: str) -> dict[str, Any]:
    focus_text = ", ".join(focus_areas) if focus_areas else "product, demand, execution"
    source_text = ", ".join(sources) if sources else "customer interviews, external research, market evidence"

    return {
        "title": f"Research Brief: {topic}",
        "executive_summary": (
            f"{topic} is strategically important across modern product and go-to-market planning. "
            f"The strongest opportunities sit in {focus_text}, while the main constraints are likely to be clarity, trust, and disciplined execution."
        ),
        "key_findings": [
            f"The category appears relevant for {audience} because the decision maker is increasingly focused on measurable outcomes and operating leverage.",
            f"Demand and product-market fit are likely to benefit from stronger proof points, clearer positioning, and a sharper narrative around value delivery.",
            f"The right next moves are to test the strongest assumptions with {source_text}, quantify friction, and prioritize the highest-impact opportunity first."
        ],
        "risks": [
            "Weak product differentiation and generic messaging that fails to establish a clear wedge.",
            "Overreliance on a single data source or anecdotal validation rather than a repeatable evidence loop.",
            "Execution speed outpacing internal clarity, leading to inconsistent priorities and reduced confidence."
        ],
        "recommendations": [
            "Define a narrow target segment and articulate a crisp value proposition tied to measurable outcomes.",
            "Test the core concept with customer feedback, competitor analysis, and a lightweight validation loop.",
            "Convert insights into a 90-day roadmap with explicit hypotheses, metrics, and review checkpoints."
        ],
        "action_plan": [
            "Week 1: sharpen the user problem, segment, and success criteria.",
            "Week 2: evaluate market signals, competitor positioning, and target customer friction.",
            "Week 3: prototype the smallest viable workflow and collect structured user feedback.",
            "Week 4: critique the evidence, adjust the plan, and prioritize the next sprint."
        ],
        "goal": goal,
        "audience": audience,
        "source_mix": source_text,
    }


def generate_brief(topic: str, focus_areas: list[str] | None = None, sources: list[str] | None = None, audience: str = "founders and operators", goal: str = "Build a clear research and action plan") -> dict[str, Any]:
    topic = (topic or "AI-powered research workflows").strip()
    focus_areas = _ensure_list(focus_areas, ["market demand", "product differentiation", "execution risk"])
    sources = _ensure_list(sources, ["public market research", "customer interviews", "market patterns"])
    audience = audience or "founders and operators"
    goal = goal or "Build a clear research and action plan"

    if settings.OPENAI_API_KEY and OpenAI:
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior strategy analyst and research operator. Return valid JSON only with keys: "
                            "title, executive_summary, key_findings, risks, recommendations, action_plan, goal, audience, source_mix."
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps({
                            "topic": topic,
                            "focus_areas": focus_areas,
                            "sources": sources,
                            "audience": audience,
                            "goal": goal,
                        }),
                    },
                ],
                temperature=0.6,
            )
            content = response.choices[0].message.content or ""
            parsed = json.loads(content)
            return {
                "title": parsed.get("title", f"Research Brief: {topic}"),
                "executive_summary": parsed.get("executive_summary", ""),
                "key_findings": parsed.get("key_findings", []),
                "risks": parsed.get("risks", []),
                "recommendations": parsed.get("recommendations", []),
                "action_plan": parsed.get("action_plan", []),
                "goal": parsed.get("goal", goal),
                "audience": parsed.get("audience", audience),
                "source_mix": parsed.get("source_mix", ", ".join(sources)),
            }
        except Exception:
            return _fallback_brief(topic, focus_areas, sources, audience, goal)

    return _fallback_brief(topic, focus_areas, sources, audience, goal)
