import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO", "").split(",")
EMAIL_CC  = os.getenv("EMAIL_CC", "").split(",")
EMAIL_BCC = os.getenv("EMAIL_BCC", "").split(",")


def get_template(severity, message):
    color = {
        "Critical": "red",
        "Medium": "orange",
        "Low": "green"
    }.get(severity, "gray")

    return f"""
    <html>
      <body>
        <h2 style="color:{color};">🚨 {severity} Threat Detected</h2>
        <pre style="font-size: 16px;">{message}</pre>
      </body>
    </html>
    """

def send_email_alert(subject, message, severity="Medium"):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO

        html = get_template(severity, message)
        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()
        print(f"[✓] Email alert sent for {severity} threat.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")
