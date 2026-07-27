"""Application Configuration Module."""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "bot_database.db")
URL_SHORTENER_API_KEY: str = os.getenv("URL_SHORTENER_API_KEY", "")
TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
PORT: int = int(os.getenv("PORT", "10000"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")
