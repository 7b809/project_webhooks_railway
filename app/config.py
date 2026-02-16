import os
from dotenv import load_dotenv

# Load .env for local development
# (Railway will use its own environment variables)
load_dotenv()


class Settings:
    # ==============================
    # CORE TELEGRAM SETTINGS
    # ==============================
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")

    # Optional default bots (if you still use them elsewhere)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TRADE_TELEGRAM_BOT_TOKEN: str = os.getenv("TRADE_TELEGRAM_BOT_TOKEN")
    TRADE_TELEGRAM_CHAT_ID: str = os.getenv("TRADE_TELEGRAM_CHAT_ID")

    # ==============================
    # MONGODB CONFIG
    # ==============================
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB")

    # ==============================
    # 🔥 DYNAMIC ENV FETCHER
    # ==============================
    @staticmethod
    def get_env(key: str):
        """
        Dynamically fetch any environment variable.
        Used for dynamic bot tokens.
        """
        return os.getenv(key)

    # ==============================
    # OPTIONAL: ENV VALIDATION
    # ==============================
    def validate(self):
        missing = []

        if not self.TELEGRAM_CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")

        if not self.MONGO_URI:
            missing.append("MONGO_URI")

        if not self.MONGO_DB:
            missing.append("MONGO_DB")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


settings = Settings()
