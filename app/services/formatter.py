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
