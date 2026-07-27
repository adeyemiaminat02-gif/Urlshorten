"""Message Handler for URL shortening."""

import logging
from telegram import Update
from telegram.ext import ContextTypes
import database
import utils
from services.url_shortener import URLShortenerService

logger = logging.getLogger(__name__)


async def shorten_url_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Process incoming messages, validate URLs, and return shortened links."""
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    raw_text = update.message.text.strip()

    # Rate limiting guard
    if utils.is_rate_limited(user_id):
        await update.message.reply_text(
            "⚠️ Please slow down and try again shortly (Limit: 10 requests/min)."
        )
        return

    # Input validation guard
    if not utils.is_valid_url(raw_text):
        await update.message.reply_text(
            "❌ Invalid URL format. Please make sure your link includes `http://` or `https://`.",
            parse_mode="Markdown",
        )
        return

    status_msg = await update.message.reply_text("⏳ Shortening your link...")

    try:
        short_url = await URLShortenerService.shorten(raw_text)

        # Save to database
        database.save_url(user_id, raw_text, short_url)

        response_text = (
            "✅ **URL Shortened Successfully!**\n\n"
            f"**Original:**\n{raw_text}\n\n"
            f"**Short URL:**\n{short_url}"
        )

        await status_msg.edit_text(response_text, parse_mode="Markdown")
        logger.info(f"User {user_id} shortened URL successfully.")

    except Exception as e:
        logger.error(f"Error shortening URL for user {user_id}: {e}")
        await status_msg.edit_text(
            "⚠️ An error occurred while generating your shortened link. Please try again later."
        )
