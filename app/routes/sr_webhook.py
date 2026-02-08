from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.db.mongo import sr_collection
from app.services.telegram import send_telegram
from app.services.formatter import format_sr_alert

router = APIRouter()

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

    # 💾 Save to MongoDB
    sr_collection.insert_one(document)

    # 📩 Telegram
    message = format_sr_alert(document)
    send_telegram(message)

    return {"status": "saved_and_sent"}
