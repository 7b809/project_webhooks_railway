from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.db.mongo import sr_collection
from app.services.telegram import send_telegram
from app.services.formatter import format_sr_alert
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

    required = [
        "support_flag", "resistance_flag",
        "Support", "Resistance",
        "SupportTime", "ResistanceTime"
    ]

    for key in required:
        if key not in data:
            raise HTTPException(status_code=400, detail=f"Missing {key}")

    document = {
        "ticker": data.get("ticker", "UNKNOWN"),
        "timeframe": data.get("timeframe", "-"),
        "support_flag": data["support_flag"],
        "resistance_flag": data["resistance_flag"],
        "support": data["Support"],
        "resistance": data["Resistance"],
        "support_time": data["SupportTime"],
        "resistance_time": data["ResistanceTime"],
        "alert_time": datetime.utcnow(),
        "raw": data
    }

    # 💾 Save to MongoDB (Always Save)
    sr_collection.insert_one(document)

    # 🔍 Load Filters
    filters = load_filters()

    send_support = (
        data["support_flag"] is True and 
        filters.get("support_flag", False) is True
    )

    send_resistance = (
        data["resistance_flag"] is True and 
        filters.get("resistance_flag", False) is True
    )

    # 📩 Send Only Allowed Alerts
    if send_support or send_resistance:
        message = format_sr_alert(
            document,
            send_support=send_support,
            send_resistance=send_resistance
        )
        send_telegram(message)

    return {"status": "saved_and_filtered"}
