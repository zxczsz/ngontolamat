from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from sessionMaker import sessionCli

START_MESSAGE = (
        'Hai!\n'
        'I can generate Session String **Pyrogram & Telethon** for your UserBot.\n\n'
    
        '**This requires :**\n- **API ID**\n- **API HASH**\n- **PHONE NUMBER**\n- **VERIFICATION**\n\nI suggest you to prepare the required items before using this Bot'
    
        '**Note** : I do not collect or log your login credentials/sessions.\n'
        'Bot By : @hilmay619\n\n'
        '**Now, choose the one you need**'
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
