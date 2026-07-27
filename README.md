# 🔗 ShorteningLinkBot

A production-ready Telegram Bot built with Python (`python-telegram-bot` v22+) that instantly shortens links using free APIs, keeps history records, supports rate limiting, and offers admin controls.

---

## 🛠 Features
- **URL Shortening:** Converts long URLs instantly via TinyURL/is.gd APIs.
- **User History:** Track previously shortened links with date/time logs.
- **Rate Limiting:** Protects against spamming (10 requests/min limit).
- **Admin Control Panel:** Complete view of bot metrics and broadcast engine.
- **Render Ready:** Integrated Flask keep-alive web service for deployment as a Render Web Service.

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.12+
- Virtual Environment tool (`venv`)

### 1. Clone & Setup
```bash
git clone [https://github.com/YOUR_USERNAME/shorteninglinkbot.git](https://github.com/YOUR_USERNAME/shorteninglinkbot.git)
cd shorteninglinkbot

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
