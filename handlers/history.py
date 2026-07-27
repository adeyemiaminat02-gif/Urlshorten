"""Command Handler for link history."""

from telegram import Update
from telegram.ext import ContextTypes
import database


async def history_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Display user's shortened link history."""
    user_id = update.effective_user.id
    records = database.get_user_history(user_id, limit=10)

    if not records:
        text = "📂 You haven't shortened any links yet!"
        if update.message:
            await update.message.reply_text(text)
        elif update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(text)
        return

    response = ["📜 **Your Last Shortened Links:**\n"]
    for row in records:
        entry = (
            f"🔹 **ID {row['id']}** | {row['created_at']}\n"
            f"   Original: {row['original_url']}\n"
            f"   Short: {row['short_url']}\n"
        )
        response.append(entry)

    response_text = "\n".join(response)

    if update.message:
        await update.message.reply_text(
            response_text, disable_web_page_preview=True, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            response_text, disable_web_page_preview=True, parse_mode="Markdown"
        )
