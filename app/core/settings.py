import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


ATTENTION_TEXT = """⚠️ Attention! Joined user with overlow reputation! ⚠️

📊 Reputation: <i>{0}</i> 🌟

🔗 First name: <u>{1}</u>
🔗 Last name: <u>{2}</u>
🔖 Username: {3}
🤖 Is bot: <b>{4}</b>

🆔 <code>{5}</code>"""


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    bot_id: int
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    db_echo: bool
    attention_text: str = ATTENTION_TEXT

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings(
    bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
    bot_id=int(os.environ.get("BOT_ID", "0")),
    db_host=os.environ.get("POSTGRES_HOST", "postgres"),
    db_port=int(os.environ.get("POSTGRES_PORT", "5432")),
    db_name=os.environ.get("POSTGRES_DB", "reputations_bot"),
    db_user=os.environ.get("POSTGRES_USER", "postgres"),
    db_password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
    db_echo=os.environ.get("SQLALCHEMY_ECHO", "false").lower()
    in {"1", "true", "yes", "on"},
)
