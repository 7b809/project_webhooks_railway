import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # ==============================
    # TELEGRAM - NORMAL ALERT BOT
    # ==============================
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")

    # ==============================
    # TELEGRAM - TRADE SIGNAL BOT
    # ==============================
    TRADE_TELEGRAM_BOT_TOKEN: str = os.getenv("TRADE_TELEGRAM_BOT_TOKEN")
    TRADE_TELEGRAM_CHAT_ID: str = os.getenv("TRADE_TELEGRAM_CHAT_ID")

    # ==============================
    # MONGODB CONFIG
    # ==============================
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB: str = os.getenv("MONGO_DB")

    # ==============================
    # OPTIONAL: ENV VALIDATION
    # ==============================
    def validate(self):
        missing = []

        if not self.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not self.TELEGRAM_CHAT_ID:
            missing.append("TELEGRAM_CHAT_ID")
        if not self.MONGO_URI:
            missing.append("MONGO_URI")
        if not self.MONGO_DB:
            missing.append("MONGO_DB")

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")


settings = Settings()
