from datetime import datetime, time
from app.db.mongo import raw_collection
from app.services.telegram import send_telegram


def send_final_support_summary():

    start = time(12, 0)
    end = time(15, 5)

    raw_data = raw_collection.find().sort("_received_at", -1)

    ticker_support = {}

    for row in raw_data:
        payload = row.get("payload", {})
        event_type = payload.get("type")
        ticker = payload.get("ticker")
        time_str = payload.get("time_ist")

        if not ticker or not time_str:
            continue

        event_time = datetime.strptime(time_str, "%H:%M:%S").time()

        if not (start <= event_time <= end):
            continue

        if event_type == "SUPPORT_CREATED":
            if ticker not in ticker_support:
                ticker_support[ticker] = {
                    "support_price": payload.get("price"),
                    "support_time": time_str,
                    "valid": True
                }

        if event_type in ["SUPPORT_CREATED", "RESISTANCE_CREATED"]:
            if ticker in ticker_support:
                # If new event after saved support → invalidate
                ticker_support[ticker]["valid"] = False

    # Build final table
    lines = []
    for ticker, data in ticker_support.items():
        if data["valid"]:
            lines.append(
                f"{ticker} | {data['support_price']} | {data['support_time']}"
            )

    if not lines:
        send_telegram("📊 3:05 PM Summary\nNo final support levels found.")
        return

    message = "📊 3:05 PM FINAL SUPPORT LEVELS\n\n"
    message += "Ticker | Price | Time\n"
    message += "-" * 35 + "\n"

    for line in lines:
        message += line + "\n"

    send_telegram(message)
