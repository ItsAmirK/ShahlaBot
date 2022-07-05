from datetime import datetime, timedelta
from pyrogram.types import Message, ChatPermissions
from pyrogram.filters import command, group

from models.group_admin import Permissions
import services.database_helpers as db_helpers
from shahla import Shahla, async_injector
from services.reporter import Reporter
from services.database import Database
from models.user_warnings import UserWarning
from models.configuration import Configuration


MUTE_MESSAGE_FMT = (
    "User {target_fn} has been muted "
    "By: {admin_fn}\n"
    "Reason: {reason}\n"
)


@Shahla.on_message(command("mute") & group)  # type: ignore
@async_injector
async def on_warn_requested(
    shahla: Shahla,
    message: Message,
    config: Configuration,
    reporter: Reporter,
    database: Database,
):
#    warnings = database.user_warnings
    admins = database.group_admins

    if not message.from_user:
        return

    target_user, others = await shahla.resolve_target_user_and_others_from_command(
        message
    )
    if not target_user:
        await message.reply_text(
            "Please reply to a user or use the command in the format `/mute @username`."
        )
        return

    if not any(others):
        await message.reply_text(
            "Please reply to a user or use the command in the format `/mute @username reason`."
        )
        return

    sender_id = message.from_user.id
    admin = db_helpers.get_group_admin_with_permission(
        database, sender_id, Permissions.CanMute
    )

    if not admin:
        await message.reply_text("You are not allowed to mute users.")
        return

    # admin can mute users ...
    if target_user.id == sender_id:
        await message.reply_text("You can't mute yourself.")
        return

    if target_user in config.super_admins:
        await message.reply_text("You can't mute a super admin.")
        return

    # check if target is not an admin
    if admins.exists(dict(user_chat_id=target_user.id)):
        await message.reply_text("You can't mute an admin.")
        return

    # check if there's a reason in command
    reason = " ".join(others)

    text = MUTE_MESSAGE_FMT.format(
        target_fn=target_user.first_name,
        admin_fn=message.from_user.first_name,
        reason=reason,
        )
    await shahla.restrict_chat_member(
    chat_id=message.chat.id,
    user_id=target_user.id,
    permissions = ChatPermissions(can_send_message=False)
)
    await message.reply_text(text)
    await reporter.report("muted", text)
