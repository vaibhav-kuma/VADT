import requests

def send_slack_alert(message, webhook_url):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"[Slack Error] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[Slack Exception] {e}")
