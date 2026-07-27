"""Command and Callback Handlers for deleting link history."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database


async def delete_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Prompt deletion options to user."""
    keyboard = [
        [
            InlineKeyboardButton(
                "⚠️ Delete All History", callback_data="confirm_delete_all"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🗑 **Delete History Options**\n\n"
        "To delete a specific link, use: `/delete <ID>`\n"
        "Or click below to clear your entire history.",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def delete_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Process callback actions for deleting history."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "confirm_delete_all":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔴 YES, Delete Everything", callback_data="do_delete_all"
                )
            ],
            [InlineKeyboardButton("🟢 Cancel", callback_data="cancel_delete")],
        ]
        await query.edit_message_text(
            "⚠️ **Are you absolutely sure?** This cannot be undone.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "do_delete_all":
        count = database.clear_user_history(user_id)
        await query.edit_message_text(
            f"✅ History cleared! Removed {count} link record(s)."
        )

    elif query.data == "cancel_delete":
        await query.edit_message_text("❌ Deletion process cancelled.")
