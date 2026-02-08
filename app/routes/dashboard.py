from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.mongo import sr_collection, raw_collection

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    sr_data = list(sr_collection.find().sort("alert_time", -1).limit(200))
    raw_data = list(raw_collection.find().sort("_received_at", -1).limit(200))

    # Add serial numbers
    for i, row in enumerate(sr_data, start=1):
        row["serial"] = i

    for i, row in enumerate(raw_data, start=1):
        row["serial"] = i

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sr_data": sr_data,
            "raw_data": raw_data
        }
    )
