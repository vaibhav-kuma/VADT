from flask import Flask, render_template
import os
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def parse_logs():
    alerts = []
    reasons = []
    severities = []
    if os.path.exists("../logs/alerts.log"):
        with open("../logs/alerts.log") as f:
            for line in f:
                alerts.append(line.strip())
                if "Reason:" in line:
                    parts = line.split("Reason: ")
                    if len(parts) > 1:
                        reasons.append(parts[1])
                if "Threat Detected" in line:
                    if "Critical" in line:
                        severities.append("Critical")
                    elif "Medium" in line:
                        severities.append("Medium")
                    elif "Low" in line:
                        severities.append("Low")
    return alerts[::-1], reasons, severities

def generate_severity_chart(severities):
    count = Counter(severities)
    labels, values = zip(*count.items()) if count else ([], [])
    
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=['red', 'orange', 'green'])
    ax.set_title('Threat Severity Distribution')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode()
    buf.close()
    plt.close(fig)
    return chart


def generate_chart(reasons):
    count = Counter(reasons)
    labels, values = zip(*count.most_common()) if count else ([], [])
    
    fig, ax = plt.subplots()
    ax.barh(labels, values, color='salmon')
    ax.set_title('Most Common Threat Reasons')
    plt.tight_layout()

    # Convert plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode()
    buf.close()
    plt.close(fig)
    return chart


@app.route('/')
def index():
    alerts, reasons, severities = parse_logs()
    reason_chart = generate_chart(reasons)
    severity_chart = generate_severity_chart(severities)
    return render_template("index.html", alerts=alerts, chart=reason_chart, severity_chart=severity_chart)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
