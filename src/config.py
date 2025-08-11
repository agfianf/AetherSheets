import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    # fmt: off
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    TAVILY_API_KEY: str = Field(..., description="Tavily API key for web search")
    GOOGLE_SHEET_ACCESS_CREDS: str = Field(..., description="Google Sheets access key JSON string")
    GOOGLE_SHEET_ACCESS_DICT: dict[str, Any] = Field(default_factory=dict, description="Parsed Google Sheets access key")
    # fmt: on

    @field_validator("GOOGLE_SHEET_ACCESS_DICT", mode="before")
    @classmethod
    def parse_google_sheet_access_key(cls, v: Any, info) -> dict[str, Any]:
        """Parse the GOOGLE_SHEET_ACCESS_CREDS JSON string into a dictionary."""
        if v and not isinstance(v, dict):
            return v

        # Get the raw GOOGLE_SHEET_ACCESS_CREDS value from the data being validated
        if hasattr(info, "data") and "GOOGLE_SHEET_ACCESS_CREDS" in info.data:
            access_key = info.data["GOOGLE_SHEET_ACCESS_CREDS"]
            if isinstance(access_key, str):
                try:
                    return json.loads(access_key)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in GOOGLE_SHEET_ACCESS_CREDS: {e}")
            elif isinstance(access_key, dict):
                return access_key

        return {}


settings = Settings()
