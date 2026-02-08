import time
import requests
from app.config import settings

def send_telegram(message: str, retries: int = 3, timeout: int = 5) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("❌ Telegram credentials missing")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=timeout)

            if response.status_code == 200:
                return True

            print(
                f"⚠️ Telegram error (attempt {attempt}): "
                f"{response.status_code} - {response.text}"
            )

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Telegram exception (attempt {attempt}): {e}")

        # Small backoff before retry
        time.sleep(1)

    print("❌ Telegram message failed after retries")
    return False
