from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.db.mongo import sr_collection
from app.services.telegram import send_telegram, send_trade_telegram
from app.services.formatter import format_sr_alert, format_trade_alert
import json
import os

router = APIRouter()

FILTER_FILE = "filter_tags.json"


def load_filters():
    if not os.path.exists(FILTER_FILE):
        return {"support_flag": True, "resistance_flag": True}
    
    with open(FILTER_FILE, "r") as f:
        return json.load(f)


@router.post("/webhook/sr")
async def sr_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    alert_type = data.get("type")

    if not alert_type:
        raise HTTPException(status_code=400, detail="Missing type")

    # ==============================
    # BUILD DOCUMENT
    # ==============================
    document = {
        "ticker": data.get("ticker", "UNKNOWN"),
        "timeframe": data.get("timeframe", "-"),
        "type": alert_type,
        "price": data.get("price"),
        "support": data.get("support"),
        "resistance": data.get("resistance"),
        "support_time": data.get("SupportTime"),
        "resistance_time": data.get("ResistanceTime"),
        "alert_time": datetime.utcnow(),
        "raw": data
    }

    # ==============================
    # SAVE TO MONGO (ALWAYS SAVE)
    # ==============================
    sr_collection.insert_one(document)

    filters = load_filters()

    # ==============================
    # STRUCTURE ALERTS
    # ==============================
    if alert_type in ["SUPPORT_CREATED", "RESISTANCE_CREATED"]:

        send_support = (
            alert_type == "SUPPORT_CREATED"
            and filters.get("support_flag", False)
        )

        send_resistance = (
            alert_type == "RESISTANCE_CREATED"
            and filters.get("resistance_flag", False)
        )

        if send_support or send_resistance:
            message = format_sr_alert(document)
            send_telegram(message)

    # ==============================
    # TRADE ALERTS (BUY SIGNALS)
    # ==============================
    elif alert_type in ["BUY_SUPPORT_CONFIRMED", "BUY_RETEST_SUPPORT"]:

        message = format_trade_alert(document)

        # Send to TRADE BOT (NOT normal bot)
        send_trade_telegram(message)

    # ==============================
    # UNKNOWN TYPE (SAFE FALLBACK)
    # ==============================
    else:
        print(f"⚠️ Unknown alert type received: {alert_type}")

    return {"status": "saved_and_processed"}
