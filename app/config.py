from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Hasti Research Radar")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL: str = os.getenv("MODEL", "gpt-4o-mini")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SITE_URL: str = os.getenv("SITE_URL", "http://localhost:8000")


settings = Settings()
