import json
from monitor import get_running_processes
from utils.slack_alert import send_slack_alert
from email_alerts import send_email_alert
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into environment variables

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

from attack_detector import load_attack_categories, detect_attack_type

categories = load_attack_categories()


def load_rules(path="rules/detection_rules.json"):
    with open(path) as f:
        return json.load(f)

def is_suspicious(proc, rules):
    severity = None
    reason = ""

    # High CPU usage
    if proc["cpu"] >= rules["cpu_threshold"]:
        if proc["cpu"] > 80:
            severity = "Critical"
        elif proc["cpu"] > 60:
            severity = "Medium"
        else:
            severity = "Low"
        reason = f"High CPU usage: {proc['cpu']}%"
        return True, reason, severity

    # Keyword-based detection
    cmdline = " ".join(proc.get("cmdline", []))
    for level, keywords in rules["banned_keywords"].items():
        for kw in keywords:
            if kw in cmdline:
                severity = level.capitalize()
                reason = f"Keyword '{kw}' found in command-line"
                return True, reason, severity

    return False, reason, severity


def run_detection():
    rules = load_rules()
    processes = get_running_processes()
    for proc in processes:
        suspicious, reason, severity = is_suspicious(proc, rules)
        if suspicious:
            cmdline = " ".join(proc.get("cmdline", []))
            attack_types = detect_attack_type(cmdline, categories)
            attack_str = ", ".join(attack_types)

            message = f"""
🚨 {severity} Threat Detected
• Name: {proc['name']}
• PID: {proc['pid']}
• CPU: {proc['cpu']}%
• Reason: {reason}
• Attack Type: {attack_str}
"""
            print(message)
            send_email_alert(f"{severity} Threat Detected", message, severity)
            send_slack_alert(message, SLACK_WEBHOOK)

if __name__ == "__main__":
    run_detection()
