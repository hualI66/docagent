import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    PORT: int = int(os.getenv("PORT", "5000"))

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")