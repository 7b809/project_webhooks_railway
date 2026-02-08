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
    return f"""
📥 <b>Raw Webhook Alert</b>

<b>Received At:</b> {data.get("_received_at")}

<b>Payload:</b>
<pre>{data.get("payload")}</pre>
""".strip()
