from fastapi import APIRouter, Request, HTTPException
from app.routes.dynamic_webhook import dynamic_webhook
import json
router = APIRouter()


@router.post("/webhook/gateway")
async def webhook_gateway(request: Request):
    """
    Gateway route that extracts indicator number
    from incoming JSON payload and forwards
    to dynamic webhook.
    """

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Extract num from payload
    num = payload.get("num")

    if not num:
        raise HTTPException(status_code=400, detail="Missing indicator number in payload")

    # IMPORTANT:
    # We must recreate request body because it was already consumed
    request._body = json.dumps(payload).encode()

    return await dynamic_webhook(str(num), request)
