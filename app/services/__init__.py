from __future__ import annotations

import json
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

from app.config import settings


def _build_fallback_brief(topic: str, focus_areas: list[str], sources: list[str], audience: str, goal: str) -> dict[str, Any]:
    focus_text = ", ".join(focus_areas) if focus_areas else "market drivers, product quality, risks and execution"
    source_text = ", ".join(sources) if sources else "public sources, user interviews, platform signals"

    title = f"Research Brief: {topic}"
    return {
        "title": title,
        "executive_summary": (
            f"{topic} is a strategically relevant area with strong momentum and a need for disciplined execution. "
            f"The most important opportunities sit in {focus_text}, while key attention should be paid to adoption, trust, and operational efficiency."
        ),
        "key_findings": [
            f"The topic is likely to matter most for {audience} because the value chain is increasingly shaped by speed, clarity, and trust.",
            f"There is evidence of meaningful demand in {focus_text}, but adoption is likely to depend on measurable outcomes and product credibility.",
            f"The strongest path forward is to validate assumptions with {source_text} and align recommended actions to a realistic first-year operating plan."
        ],
        "risks": [
            "Weak differentiation from generic AI tooling or broad research content.",
            "Overreliance on a single data source or anecdotal user feedback.",
            "Poor product clarity leading to inconsistent value perception for the target audience."
        ],
        "recommendations": [
            "Define a narrow wedge for the first release and measure user value using explicit KPIs.",
            "Turn research signals into a repeatable content and decision workflow instead of one-off outputs.",
            "Build a feedback loop with customer interviews, usage data, and a concise monthly review process."
        ],
        "action_plan": [
            "Week 1: map the persona, workflow, and outcome requirements.",
            "Week 2: validate the core hypothesis against competitor and customer signals.",
            "Week 3: prototype a focused workflow and measure engagement, retention, and conversion.",
            "Week 4: refine the product narrative and shipping plan based on real evidence."
        ],
        "goal": goal,
        "audience": audience,
        "source_mix": source_text,
    }


def generate_brief(topic: str, focus_areas: list[str] | None = None, sources: list[str] | None = None, audience: str = "founders and operators", goal: str = "Build a clear research and action plan") -> dict[str, Any]:
    topic = (topic or "AI-powered research workflows").strip()
    focus_areas = focus_areas or ["market demand", "product differentiation", "competitive positioning"]
    sources = sources or ["public market research", "user interviews", "pattern analysis"]
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
                            "You are an expert strategy analyst. Return valid JSON only with fields: "
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
            return _build_fallback_brief(topic, focus_areas, sources, audience, goal)

    return _build_fallback_brief(topic, focus_areas, sources, audience, goal)

