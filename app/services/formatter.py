def format_trade_alert(data: dict) -> str:
    return f"""
🚀 <b>TRADE SIGNAL</b>

<b>Type:</b> {data.get("type")}
<b>Symbol:</b> {data.get("ticker")}
<b>Price:</b> {data.get("price")}

⏰ {data.get("alert_time")}
""".strip()

def format_sr_alert(data: dict) -> str:
    flag = "🟢 SUPPORT UPDATED" if data["support_flag"] == 1 else "🔴 RESISTANCE UPDATED"

    return f"""
📊 <b>Support & Resistance Alert</b>

{flag}

<b>Symbol:</b> {data.get("ticker")}
<b>Timeframe:</b> {data.get("timeframe", "-")}

<b>Support:</b> {data.get("support")}
<b>Resistance:</b> {data.get("resistance")}

<b>Support Time:</b> {data.get("support_time")}
<b>Resistance Time:</b> {data.get("resistance_time")}

⏰ {data.get("alert_time")}
""".strip()
    
def format_raw_alert(data: dict) -> str:
    payload = data.get("payload", {})

    formatted_payload = ""

    # Case 1: Payload is a dict
    if isinstance(payload, dict):
        lines = []

        for key, value in payload.items():
            # If value itself is multiline text
            if isinstance(value, str) and "\n" in value:
                lines.append(f"<b>{key}:</b>")
                for sub_line in value.split("\n"):
                    lines.append(f"  • {sub_line.strip()}")
            else:
                lines.append(f"<b>{key}:</b> {value}")

        formatted_payload = "\n".join(lines)

    # Case 2: Anything else (string, list, etc.)
    else:
        formatted_payload = str(payload)

    return f"""
📥 <b>Raw Webhook Alert</b>

<b>Received At:</b> {data.get("_received_at")}

<b>Payload Details:</b>
{formatted_payload}
""".strip()


def format_pure_raw_alert(data: dict) -> str:
    return f"""
📥 <b>Raw Webhook Alert</b>

<b>Received At:</b> {data.get("_received_at")}

<b>Payload:</b>
<pre>{data.get("payload")}</pre>
""".strip()

def format_dynamic_alert(document: dict) -> str:
    """
    Universal formatter for any indicator payload
    """

    indicator_name = document.get("indicator_name", "Indicator")
    received_at = document.get("_received_at")
    payload = document.get("payload", {})

    lines = []

    # If payload is dict → pretty format
    if isinstance(payload, dict):
        for key, value in payload.items():

            # Nested dict handling
            if isinstance(value, dict):
                lines.append(f"<b>{key}:</b>")
                for sub_key, sub_val in value.items():
                    lines.append(f"  • <b>{sub_key}:</b> {sub_val}")

            # List handling
            elif isinstance(value, list):
                lines.append(f"<b>{key}:</b>")
                for item in value:
                    lines.append(f"  • {item}")

            else:
                lines.append(f"<b>{key}:</b> {value}")

    else:
        lines.append(str(payload))

    formatted_payload = "\n\n".join(lines)

    return f"""
📢 <b>{indicator_name} Alert</b>

<b>Received At:</b> {received_at}

<b>Payload Details:</b>
{formatted_payload}
""".strip()

def format_cross_trade_alert(document: dict) -> str:
    """
    Advanced confirmed LONG trade formatter
    Shows CE & PE event details
    """

    payload = document.get("payload", {})
    matched_payload = document.get("matched_payload", {})

    symbol = payload.get("symbol", "-")
    price = payload.get("price", "-")
    date = payload.get("date", "-")
    time_ist = payload.get("time_ist", "-")

    # Identify which side is CE and PE
    if symbol.endswith("CE"):
        ce_payload = payload
        pe_payload = matched_payload
    else:
        ce_payload = matched_payload
        pe_payload = payload

    ce_action = "Support Fall (S Breakdown)" if ce_payload.get("action") == 0 else "Resistance Breakout"
    pe_action = "Support Fall (S Breakdown)" if pe_payload.get("action") == 0 else "Resistance Breakout"

    ce_time = ce_payload.get("time_ist", "-")
    pe_time = pe_payload.get("time_ist", "-")

    strike = symbol[-7:-2] if len(symbol) > 7 else "-"

    return f"""
🚀 <b>CONFIRMED LONG TRADE</b>

<b>Strike:</b> {strike}
<b>Entry Option:</b> {symbol}
<b>Entry Price:</b> {price}

━━━━━━━━━━━━━━━━━━
📊 <b>Confirmation Logic</b>

🟥 CE Event:
   • {ce_action}
   • Time: {ce_time}

🟢 PE Event:
   • {pe_action}
   • Time: {pe_time}

━━━━━━━━━━━━━━━━━━
🔥 CE - PE Cross Confirmation
📈 S/R Structure Break Validated

📅 {date}
⏰ {time_ist}
━━━━━━━━━━━━━━━━━━
""".strip()
