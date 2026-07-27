"""Admin Dashboard and Broadcast Commands."""

import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
import config
import database

logger = logging.getLogger(__name__)


async def admin_stats_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Display system and user metrics (Admin Only)."""
    user_id = update.effective_user.id
    if user_id != config.ADMIN_ID:
        await update.message.reply_text(
            "⛔ Access Denied: Admin privileges required."
        )
        return

    stats = database.get_admin_stats()

    active_list = "\n".join(
        [
            f"• @{row['username'] or row['user_id']}: {row['link_count']} links"
            for row in stats["active_users"]
        ]
    )

    stats_text = (
        "📊 **Admin Statistics Dashboard**\n\n"
        f"👥 **Total Registered Users:** {stats['total_users']}\n"
        f"🔗 **Total Links Shortened:** {stats['total_urls']}\n"
        f"📅 **Links Shortened Today:** {stats['today_urls']}\n\n"
        f"🏆 **Top Active Users:**\n{active_list if active_list else 'No data yet.'}"
    )

    await update.message.reply_text(stats_text, parse_mode="Markdown")


async def broadcast_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Broadcast message to all registered users (Admin Only)."""
    user_id = update.effective_user.id
    if user_id != config.ADMIN_ID:
        await update.message.reply_text("⛔ Access Denied.")
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a message to broadcast.\n\n"
            "Example: `/broadcast Hello users!`",
            parse_mode="Markdown",
        )
        return

    broadcast_text = " ".join(context.args)
    user_ids = database.get_all_user_ids()

    success, failed = 0, 0
    progress_msg = await update.message.reply_text("📢 Starting broadcast...")

    for target_id in user_ids:
        try:
            await context.bot.send_message(
                chat_id=target_id, text=broadcast_text
            )
            success += 1
            await asyncio.sleep(0.05)  # Avoid hitting Telegram global limits
        except Exception as e:
            logger.warning(
                f"Failed to send broadcast to user {target_id}: {e}"
            )
            failed += 1

    await progress_msg.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"• **Successful:** {success}\n"
        f"• **Failed/Blocked:** {failed}"
    )
