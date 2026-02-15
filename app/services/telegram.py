import time
import requests
from app.config import settings


def _send_message(bot_token: str, chat_id: str, message: str, retries: int = 3, timeout: int = 5) -> bool:
    if not bot_token or not chat_id:
        print("❌ Telegram credentials missing")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
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

        time.sleep(1)

    print("❌ Telegram message failed after retries")
    return False


# ==============================
# NORMAL SUPPORT / RESISTANCE BOT
# ==============================
def send_telegram(message: str, retries: int = 3, timeout: int = 5) -> bool:
    return _send_message(
        bot_token=settings.TELEGRAM_BOT_TOKEN,
        chat_id=settings.TELEGRAM_CHAT_ID,
        message=message,
        retries=retries,
        timeout=timeout
    )


# ==============================
# TRADE / BUY SIGNAL BOT
# ==============================
def send_trade_telegram(message: str, retries: int = 3, timeout: int = 5) -> bool:
    return _send_message(
        bot_token=settings.TRADE_TELEGRAM_BOT_TOKEN,
        chat_id=settings.TRADE_TELEGRAM_CHAT_ID,
        message=message,
        retries=retries,
        timeout=timeout
    )
