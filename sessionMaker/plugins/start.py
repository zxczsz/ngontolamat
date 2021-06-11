from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from sessionMaker import sessionCli

START_MESSAGE = (
        '**I can generate Session String Pyrogram & Telethon for your UserBot.**  ✨.\n\n'
        '**Note :-** 🔰\n\n'
        '🚫 **I never collect your login credentials/sessions !**  🚫'
    )

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text='Pyrogram', callback_data='sele_pyrogram')],
    [InlineKeyboardButton(text='Telethon', callback_data='sele_telethon')]]
)

@sessionCli.on_message(filters.command('start'))
async def start(sessionCli, message):
    await message.reply(
        text=START_MESSAGE,
        reply_markup=KEYBOARD,
        disable_web_page_preview=True
    )
