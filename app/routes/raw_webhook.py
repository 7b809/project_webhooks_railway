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

    # -----------------------------
    # 🔎 FILTER LOGIC
    # -----------------------------

    if isinstance(payload, dict):

        # If chat_id is present → apply filter
        if "chat_id" in payload:

            key_count = len(payload.keys())
            text = payload.get("text", "")

            # Condition:
            # 1. keys must be > 2
            # 2. text must contain BUY Signal
            if not (key_count > 2 and "BUY Signal" in text):
                return {"status": "ignored_filtered_signal"}

        # If chat_id NOT present → allow everything

    # -----------------------------
    # ✅ SAVE & SEND
    # -----------------------------

    document = {
        "_received_at": datetime.utcnow().isoformat(),
        "payload": payload
    }

    raw_collection.insert_one(document)

    message = format_raw_alert(document)
    send_telegram(message)

    return {
        "status": "raw_saved_and_sent"
    }
