// === 📥 Update backend/exporter.py to warn if .env is missing ===
import csv, json, smtplib, ssl, os, sys
from email.message import EmailMessage
import requests
from dotenv import load_dotenv, find_dotenv

# Load .env and warn if missing
if not find_dotenv():
    print("[⚠️ WARNING] .env file not found! Defaulting to system environment variables.")
else:
    load_dotenv()

SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")


def export_to_csv():
    with open('logs/alerts.json') as infile:
        data = json.load(infile)
    with open('exports/alerts.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def send_to_splunk(alert):
    headers = {"Authorization": f"Splunk {SPLUNK_TOKEN}"}
    payload = {"event": alert, "sourcetype": "threat_detection"}
    try:
        response = requests.post(SPLUNK_HEC_URL, headers=headers, json=payload, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"[SPLUNK ERROR] {e}")


def send_email(alert):
    subject = f"[{alert['severity'].upper()}] Threat Alert: {alert['process']}"
    body = (
        f"🔒 Threat Detected:\n"
        f"Time: {alert['timestamp']}\n"
        f"Process: {alert['process']}\n"
        f"Severity: {alert['severity']}\n"
        f"Type: {', '.join(alert['attack_type'])}\n"
        f"MITRE TTP: {', '.join(alert['ttp'])}\n"
    )

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
