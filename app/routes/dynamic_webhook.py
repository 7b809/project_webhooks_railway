from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.config import settings
from app.db.mongo import db  # ✅ reuse existing mongo connection
from app.services.telegram import _send_message
from app.services.formatter import format_dynamic_alert  # ✅ dynamic formatter
import json
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

INDICATOR_MAP_FILE = "app/config/indicator_map.json"


def load_indicator_map():
    if not os.path.exists(INDICATOR_MAP_FILE):
        raise Exception("indicator_map.json not found")

    with open(INDICATOR_MAP_FILE, "r") as f:
        return json.load(f)


@router.post("/webhook/{indicator_num}")
async def dynamic_webhook(indicator_num: str, request: Request):

    # ===============================
    # PARSE JSON
    # ===============================
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # ===============================
    # LOAD INDICATOR MAP
    # ===============================
    indicator_map = load_indicator_map()

    if indicator_num not in indicator_map:
        raise HTTPException(status_code=404, detail="Invalid indicator number")

    indicator_config = indicator_map[indicator_num]

    collection_name = indicator_config["collection"]
    bot_token_env = indicator_config["bot_token_env"]

    # ===============================
    # SAVE TO CORRECT COLLECTION
    # ===============================
    collection = db[collection_name]

    document = {
        "_received_at": datetime.utcnow().isoformat(),
        "indicator_num": indicator_num,
        "indicator_name": indicator_config.get("indicator_name", "Indicator"),
        "payload": payload
    }

    collection.insert_one(document)

    # ===============================
    # SEND TELEGRAM MESSAGE
    # ===============================
    bot_token = indicator_config.get(bot_token_env) 
    bot_token = os.getenv(bot_token) 
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token:
        print(f"❌ Bot token missing for indicator {indicator_num}")
        return {
            "status": "saved_but_no_bot_token",
            "indicator": indicator_config.get("indicator_name")
        }

    # ✅ Use universal dynamic formatter
    message = format_dynamic_alert(document)
    _send_message(
        bot_token=bot_token,
        chat_id=chat_id,
        message=message
    )

    return {
        "status": "saved_and_sent",
        "indicator": indicator_config.get("indicator_name")
    }
