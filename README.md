# VADT

# 🛡️ Threat Detection Dashboard

A full-stack cybersecurity tool for real-time process monitoring, threat detection, MITRE ATT\&CK tagging, email/Splunk alerts, and data visualization using React, Flask, and MongoDB.

---

## 🚀 Features

* 🔍 Real-time detection of suspicious processes
* 📈 Dashboard with visualizations (attack type & severity)
* 🧠 MITRE ATT\&CK & TTP categorization
* 📤 Email & Splunk alerting
* 💾 MongoDB storage and CSV exporting
* 🔐 Secrets managed via `.env`
* 🐳 Docker support

---

## 📁 Project Structure

```
threat-dashboard/
├── backend/              # Flask API, detector, exporter
│   ├── app.py
│   ├── detector.py
│   ├── exporter.py
│   ├── attack_categories.json
│   ├── requirements.txt
├── frontend/             # React dashboard UI
│   ├── src/App.jsx
│   ├── package.json
├── logs/                 # Logs directory (auto-generated)
│   └── alerts.json
├── exports/              # CSV exports
├── .env                  # Secrets & config (DO NOT COMMIT)
├── Dockerfile
├── .gitignore
```

---

## 🧪 Setup Instructions

### ✅ Requirements

* Python 3.10+
* Node.js 18+
* MongoDB (local or Atlas)
* Docker (optional)

### 1️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Frontend Setup

```bash
cd ../frontend
npm install
npm run build
```

### 3️⃣ MongoDB Setup

* Set up MongoDB locally or via Atlas
* Create a database `threat_dashboard` with collection `alerts`

### 4️⃣ Configure `.env`

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
EMAIL_SENDER=your@example.com
EMAIL_PASSWORD=yourpassword
EMAIL_RECIPIENT=recipient@example.com
SPLUNK_HEC_URL=https://splunk.example.com:8088/services/collector
SPLUNK_TOKEN=your_token
MONGO_URI=mongodb://localhost:27017
MONGO_DB=threat_dashboard
MONGO_COLLECTION=alerts
```

### 5️⃣ Run the App

#### Flask API

```bash
cd backend
source venv/bin/activate
python app.py
```

#### Detector Engine

```bash
python detector.py
```

---

## 🌐 Access Dashboard

Visit: `http://localhost:5000`

---

## 📤 Exporting & Alerts

* CSV: `exports/alerts.csv`
* Splunk: via HTTP Event Collector
* Email: via SMTP credentials in `.env`

---

## 🐳 Docker Usage

```bash
docker build -t threat-dashboard .
docker run --env-file .env -p 5000:5000 threat-dashboard
```

---

## 🔐 Security Best Practices

* Never commit `.env`
* Use app-specific passwords for email
* Monitor access logs and email/Splunk errors

---

## 📬 Contributions & License

Feel free to fork and contribute! Open-sourced under [MIT License](LICENSE).

---

## 👨‍💻 Author

Built by \VAIBHAV KUMAR — Cybersecurity Engineer & Developer
