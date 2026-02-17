import time
import requests
from app.config import settings


default_chat_id = settings.TELEGRAM_CHAT_ID


def _send_message(bot_token: str, chat_id: str, message: str,
                  retries: int = 3, timeout: int = 5) -> bool:

    if not bot_token:
        print("❌ Telegram bot token missing")
        return False

    # Always ensure we have at least default
    primary_chat_id = chat_id or default_chat_id

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def attempt_send(target_chat_id: str) -> bool:
        payload = {
            "chat_id": target_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        for attempt in range(1, retries + 1):
            try:
                response = requests.post(url, json=payload, timeout=timeout)

                if response.status_code == 200:
                    return True

                print(
                    f"⚠️ Telegram error (attempt {attempt}) "
                    f"[chat_id={target_chat_id}]: "
                    f"{response.status_code} - {response.text}"
                )

                # If chat not found → break immediately
                if response.status_code == 400 and "chat not found" in response.text:
                    return False

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Telegram exception (attempt {attempt}): {e}")

            time.sleep(1)

        return False

    # 🔹 First attempt → primary chat
    success = attempt_send(primary_chat_id)

    # 🔹 If failed and not already using default → fallback
    if not success and primary_chat_id != default_chat_id:
        print("🔁 Falling back to default chat ID...")
        success = attempt_send(default_chat_id)

    if not success:
        print("❌ Telegram message failed after retries")

    return success


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
