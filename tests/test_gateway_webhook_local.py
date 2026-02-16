import requests


def send_gateway_test(
    indicator_num: str = "1",
    base_url: str = "http://127.0.0.1:8000"
):
    """
    Sends test payload to /webhook/gateway
    with num included inside JSON body.
    """

    url = f"{base_url}/webhook/gateway"

    payload = {
        "num": indicator_num,  # 🔥 num inside payload
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

    try:
        print(f"\n🚀 Sending request to: {url}")
        print("Payload:", payload)

        response = requests.post(url, json=payload, timeout=10)

        print("Status Code:", response.status_code)

        try:
            print("Response JSON:", response.json())
        except Exception:
            print("Response Text:", response.text)

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)


if __name__ == "__main__":
    send_gateway_test(base_url="https://signal-bridge101.up.railway.app", indicator_num="1")