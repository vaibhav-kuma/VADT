import schedule
import time
from email_alerts import send_email_alert
from summary_utils import categorize_alerts, build_summary_email
from email_alerts import send_email_alert

def send_daily_summary():
    categorized = categorize_alerts()
    message = build_summary_email(categorized)
    send_email_alert(
        subject="🛡️ Daily Threat Summary Report",
        message=message,
        severity="Low"
    )

def generate_summary():
    with open("logs/alerts.log", "r") as f:
        content = f.read()
    send_email_alert(
        subject="🗓️ Daily Threat Summary",
        message=content[-5000:],  # Last ~100 alerts
        severity="Low"
    )

schedule.every().day.at("18:00").do(generate_summary)   # Daily 6 PM

while True:
    schedule.run_pending()
    time.sleep(60)
