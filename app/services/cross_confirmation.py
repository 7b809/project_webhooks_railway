from datetime import datetime, timedelta, timezone
from app.db.mongo import db
from app.services.option_parser import parse_option_symbol


CONFIRMATION_WINDOW_MINUTES = 5


def check_cross_confirmation(payload: dict, indicator_map: dict):
    """
    Check if opposite strike alert exists within 5 minutes.
    Only LONG BUY logic.

    Returns:
        False → if no confirmation
        dict  → if confirmation found
    """

    symbol = payload.get("symbol")
    action = payload.get("action")
    timestamp = payload.get("timestamp")

    if not symbol or action is None or not timestamp:
        return False

    strike, option_type = parse_option_symbol(symbol)

    if not strike or not option_type:
        return False

    # -------------------------------------------------
    # ONLY LONG LOGIC VALIDATION
    #
    # Valid combinations:
    #
    # 1️⃣ CE Support Fall (0)  + PE Resistance Break (1)
    # 2️⃣ PE Support Fall (0)  + CE Resistance Break (1)
    #
    # Any other combination → ignore
    # -------------------------------------------------

    if action not in [0, 1]:
        return False

    opposite_type = "PE" if option_type == "CE" else "CE"
    opposite_action = 1 if action == 0 else 0

    # Time window calculation
    try:
        current_time = datetime.fromtimestamp(
            int(timestamp) / 1000,
            tz=timezone.utc
        )
    except Exception:
        return False

    window_start = current_time - timedelta(minutes=CONFIRMATION_WINDOW_MINUTES)

    # Collections to check (Support & Resistance alerts)
    collections_to_check = [
        indicator_map["1"]["collection"],  # Support collection
        indicator_map["2"]["collection"],  # Resistance collection
    ]

    for col_name in collections_to_check:
        collection = db[col_name]

        match = collection.find_one({
            "payload.symbol": {"$regex": strike + opposite_type + "$"},
            "payload.action": opposite_action,
            "_received_at": {
                "$gte": window_start,
                "$lte": current_time
            }
        })

        if match:

            # Final validation for strict LONG logic
            matched_action = match.get("payload", {}).get("action")
            matched_symbol = match.get("payload", {}).get("symbol")

            if not matched_symbol:
                continue

            # Ensure correct CE/PE pairing
            if not matched_symbol.endswith(opposite_type):
                continue

            # Validate logic pair strictly
            # One must be Support Fall (0)
            # Other must be Resistance Breakout (1)
            if sorted([action, matched_action]) == [0, 1]:

                return {
                    "current_payload": payload,
                    "matched_document": match
                }

    return False
