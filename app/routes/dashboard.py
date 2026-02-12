from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, time
from app.db.mongo import sr_collection, raw_collection

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    start_time: str = Query(None),   # "12:00"
    end_time: str = Query(None),     # "15:10"
    level_type: str = Query(None)    # "SUPPORT_CREATED" or "RESISTANCE_CREATED"
):
    filtered_levels = []

    if start_time and end_time and level_type:

        start = datetime.strptime(start_time, "%H:%M").time()
        end = datetime.strptime(end_time, "%H:%M").time()

        raw_data = list(raw_collection.find().sort("_received_at", -1))

        ticker_map = {}

        for row in raw_data:
            payload = row.get("payload", {})
            event_type = payload.get("type")

            if event_type != level_type:
                continue

            time_str = payload.get("time_ist")
            if not time_str:
                continue

            event_time = datetime.strptime(time_str, "%H:%M:%S").time()

            if start <= event_time <= end:
                ticker = payload.get("ticker")

                # Because sorted descending, first match = latest
                if ticker not in ticker_map:
                    ticker_map[ticker] = {
                        "ticker": ticker,
                        "price": payload.get("price"),
                        "created_at": time_str,
                        "pivot_id": payload.get("pivot_id"),
                    }

        filtered_levels = list(ticker_map.values())

    # Default SR table
    sr_data = list(sr_collection.find().sort("alert_time", -1).limit(200))
    raw_data = list(raw_collection.find().sort("_received_at", -1).limit(200))

    for i, row in enumerate(sr_data, start=1):
        row["serial"] = i

    for i, row in enumerate(raw_data, start=1):
        row["serial"] = i

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sr_data": sr_data,
            "raw_data": raw_data,
            "filtered_levels": filtered_levels
        }
    )
