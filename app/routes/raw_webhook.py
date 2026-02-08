from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.db.mongo import raw_collection
from app.services.telegram import send_telegram
from app.services.formatter import format_raw_alert

router = APIRouter()

@router.post("/webhook/raw")
async def raw_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    document = {
        "_received_at": datetime.utcnow().isoformat(),
        "payload": payload
    }

    # 💾 Save EVERYTHING
    raw_collection.insert_one(document)

    # 📩 Send to Telegram
    message = format_raw_alert(document)
    send_telegram(message)

    return {
        "status": "raw_saved_and_sent"
    }
