"""Command Handlers for /start, /help, and /about."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    if user:
        database.register_user(user.id, user.username)

    welcome_text = (
        f"👋 Welcome to ShorteningLinkBot, {user.first_name if user else 'there'}!\n\n"
        "I can instantly shorten long URLs into clean, shareable short links.\n\n"
        "✨ **Features:**\n"
        "• Shorten unlimited URLs\n"
        "• View your link history\n"
        "• Delete saved links anytime\n"
        "• Fast & reliable\n\n"
        "Simply send me any valid URL to begin!"
    )

    keyboard = [
        [InlineKeyboardButton("📂 My History", callback_data="history_view")],
        [
            InlineKeyboardButton("❓ Help", callback_data="help_view"),
            InlineKeyboardButton("ℹ️ About", callback_data="about_view"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = (
        "📖 **ShorteningLinkBot Help Guide**\n\n"
        "1️⃣ **Shorten a Link:** Send any URL starting with `http://` or `https://` directly in the chat.\n"
        "2️⃣ **View History:** Send /history to view your recent shortened links.\n"
        "3️⃣ **Delete History:** Send /delete to clear specific or all saved links.\n"
        "4️⃣ **Rate Limit:** Up to 10 shorten requests allowed per minute."
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            help_text, parse_mode="Markdown"
        )


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command."""
    about_text = (
        "ℹ️ **About ShorteningLinkBot**\n\n"
        "• **Version:** 1.0.0\n"
        "• **Framework:** python-telegram-bot v22+\n"
        "• **Hosted on:** Render Platform\n"
        "• **Developer:** @DeveloperPlaceholder\n\n"
        "Designed to streamline link sharing securely and quickly!"
    )
    if update.message:
        await update.message.reply_text(about_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            about_text, parse_mode="Markdown"
        )
