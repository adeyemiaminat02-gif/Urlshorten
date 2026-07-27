"""Main entry point for Bot & Web Server health checks."""

import logging
import asyncio
import threading
from flask import Flask
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import config
import database
from handlers.start import start_handler, help_handler, about_handler
from handlers.shorten import shorten_url_handler
from handlers.history import history_handler
from handlers.delete import delete_command_handler, delete_callback_handler
from handlers.admin import admin_stats_handler, broadcast_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Lightweight Web Server for Render Health Check
app = Flask(__name__)


@app.route("/")
def health_check():
    """Health check endpoint required for web service deployment."""
    return "Bot is running online!", 200


def run_flask():
    """Run Flask application inside a separate thread."""
    app.run(host="0.0.0.0", port=config.PORT)


def main() -> None:
    """Initialize database and start the Telegram Bot application."""
    # 1. Initialize SQLite Database
    database.init_db()

    # 2. Spin up health check endpoint thread for Render
    threading.Thread(target=run_flask, daemon=True).start()

    # 3. Create Telegram Bot Application
    application = (
        Application.builder().token(config.BOT_TOKEN).build()
    )

    # Command Handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("about", about_handler))
    application.add_handler(CommandHandler("history", history_handler))
    application.add_handler(CommandHandler("delete", delete_command_handler))
    application.add_handler(CommandHandler("admin", admin_stats_handler))
    application.add_handler(CommandHandler("broadcast", broadcast_handler))

    # Callback Query Handlers
    application.add_handler(
        CallbackQueryHandler(help_handler, pattern="^help_view$")
    )
    application.add_handler(
        CallbackQueryHandler(about_handler, pattern="^about_view$")
    )
    application.add_handler(
        CallbackQueryHandler(history_handler, pattern="^history_view$")
    )
    application.add_handler(
        CallbackQueryHandler(delete_callback_handler, pattern="^.*delete.*$")
    )

    # Text Message Handler for URL Shortening
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, shorten_url_handler
        )
    )

    # Start Polling
    logger.info("Bot successfully initialized. Starting long polling...")
    application.run_polling()


if __name__ == "__main__":
    main()
