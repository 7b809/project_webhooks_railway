import requests
import json

# 🔥 Your Railway webhook URL
URL = "https://signal-bridge101.up.railway.app/webhook/1"

# ✅ Sample Support & Resistance payload
payload = {
    "type": "SUPPORT_CREATED",
    "ticker": "NIFTY",
    "timeframe": "5m",
    "price": 22450,
    "support": 22430,
    "resistance": 22510,
    "support_time": "14:02:11",
    "resistance_time": "13:48:05",
    "pivot_id": "PIVOT_123",
    "bar_index": 456
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(URL, json=payload, headers=headers, timeout=10)

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
