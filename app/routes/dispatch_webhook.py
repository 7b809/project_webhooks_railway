from fastapi import APIRouter, Request, HTTPException
from app.routes.dynamic_webhook import dynamic_webhook

router = APIRouter()


@router.post("/webhook/gateway")
async def webhook_gateway(request: Request):
    """
    Gateway route that simply forwards request
    to dynamic webhook.
    """

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not payload.get("num"):
        raise HTTPException(status_code=400, detail="Missing indicator number in payload")

    # Directly call dynamic webhook
    return await dynamic_webhook(request)
