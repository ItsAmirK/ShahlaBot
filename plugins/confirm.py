from pyrogram.types import Message
from pyrogram.filters import regex, user

from shahla import Shahla


@Shahla.on_message(regex("مدت زمان بازی:") & user(175844556))  # type: ignore
async def confirm(_, message: Message):
    await message.reply_text("/confirm")
